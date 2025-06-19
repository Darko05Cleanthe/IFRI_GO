from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trajet, Reservation, Publication, MessagePrive, MessagePriveForm 
from .forms import TrajetForm, ReservationForm, PublicationForm, MessageForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError



# Page qui liste tous les trajets disponibles
def liste_trajets_view(request):
    trajets = Trajet.objects.all().order_by('-date_depart')
    print(f"Nombre de trajets récupérés : {trajets.count()}")
    return render(request, 'covoiturage/liste_trajets.html', {'trajets': trajets})

# Créer un trajet (par un conducteur)
@login_required
def creer_trajet(request):
    if request.method == 'POST':
        form = TrajetForm(request.POST)
        if form.is_valid():
            trajet = form.save(commit=False)
            trajet.conducteur = request.user
            trajet.save()
            messages.success(request, "Trajet publié avec succès !")
            print(request._messages)
            return redirect('covoiturage:liste_trajets')
    else:
        form = TrajetForm()
    return render(request, 'covoiturage/creer_trajet.html', {'form': form})

# Réserver un trajet (par un passager)

@login_required
def reserver_trajet(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)

    # Empêcher le conducteur de réserver son propre trajet
    if trajet.conducteur == request.user:
        messages.error(request, "Vous ne pouvez pas réserver votre propre trajet.")
        return redirect('covoiturage:liste_trajets')  # adapte l'URL si besoin

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.passager = request.user
            reservation.trajet = trajet
            reservation.save()
            messages.success(request, "Réservation effectuée avec succès.")
            return redirect('covoiturage:confirmation_reservation', reservation_id=reservation.id)
    else:
        form = ReservationForm()

    context = {
        'form': form,
        'trajet': trajet,
    }
    return render(request, 'covoiturage/reserver_trajet.html', context)

# Créer une publication (libre)



@login_required
def creer_publication(request):
    user = request.user
    trajets = Trajet.objects.filter(conducteur=user).order_by('-date_pub')
    print(f"DEBUG: trajets count for user {user}: {trajets.count()}")

    if not trajets.exists():
        # Si aucun trajet, on ne peut pas créer de publication
        messages.error(request, "Vous devez d'abord publier au moins un trajet avant de créer une publication.")
        return redirect('page_utilisateur')

    erreurs = []
    form_data = {}

    if request.method == "POST":
        titre = request.POST.get('titre', '').strip()
        contenu = request.POST.get('contenu', '').strip()
        trajet_id = request.POST.get('trajet', '')

        form_data = {'titre': titre, 'contenu': contenu, 'trajet': trajet_id}

        if not titre:
            erreurs.append("Le titre est obligatoire.")
        if not contenu:
            erreurs.append("Le contenu est obligatoire.")
        if not trajet_id:
            erreurs.append("Veuillez sélectionner un trajet.")
        else:
            try:
                trajet = Trajet.objects.get(id=trajet_id, conducteur=user)
            except Trajet.DoesNotExist:
                erreurs.append("Le trajet sélectionné est invalide.")

        if not erreurs:
            try:
                Publication.objects.create(
                    titre=titre,
                    contenu=contenu,
                    conducteur=user,
                    trajet=trajet
                )
                messages.success(request, "Publication créée avec succès.")
                return redirect('page_utilisateur')
            except ValidationError as e:
                erreurs.extend(e.messages)

    context = {
        'trajets': trajets,
        'erreurs': erreurs,
        'form_data': form_data,
    }
    return render(request, 'covoiturage/creer_publication.html', context)


# Envoyer un message privé
@login_required
def envoyer_message(request, destinataire_id=None):
    destinataire = None
    if destinataire_id:
        destinataire = get_object_or_404(User, id=destinataire_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.auteur = request.user
            if destinataire:
                message.destinataire = destinataire
            else:
                # Si le formulaire contient un destinataire choisi manuellement
                message.destinataire = form.cleaned_data.get('destinataire')
            message.save()
            messages.success(request, "Message envoyé.")
            return redirect('covoiturage:boite_reception')
    else:
        if destinataire:
            form = MessageForm(initial={'destinataire': destinataire})
        else:
            form = MessageForm()

    return render(request, 'covoiturage/envoyer_message.html', {'form': form, 'destinataire': destinataire})


# Voir les messages reçus
@login_required
def boite_reception(request):
    messages_recus = MessagePrive.objects.filter(destinataire=request.user).order_by('-date_envoi')
    return render(request, 'covoiturage/boite_reception.html', {'messages_recus': messages_recus})


@login_required
def reserver_trajet(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)

    # ❌ Empêcher le conducteur de réserver son propre trajet
    if trajet.conducteur == request.user:
        messages.error(request, "Vous ne pouvez pas réserver votre propre trajet.")
        return redirect('page_utilisateur')  # Ou une autre page adaptée

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.passager = request.user
            reservation.trajet = trajet
            reservation.save()

            infos = form.cleaned_data.get('infos_complementaires')
            return redirect('covoiturage:confirmation_reservation', reservation_id=reservation.id)
    else:
        form = ReservationForm()

    return render(request, 'covoiturage/reserver_trajet.html', {'form': form, 'trajet': trajet})

@login_required
def confirmation_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, passager=request.user)
    return render(request, 'covoiturage/confirmation_reservation.html', {'reservation': reservation})


@login_required
def supprimer_trajet(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)

    if trajet.conducteur != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce trajet.")
        return redirect('covoiturage:liste_trajets')

    trajet.delete()
    messages.success(request, "Trajet supprimé avec succès.")
    return redirect('covoiturage:liste_trajets')

@login_required
def supprimer_publication(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    if publication.conducteur != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer cette publication.")
    if request.method == 'POST':
        publication.delete()
        return redirect('page_utilisateur')  
    # Si la méthode n'est pas POST, tu peux rediriger ou afficher une erreur
    return redirect('page_utilisateur')

def nouveau_message(request):
    if request.method == 'POST':
        form = MessagePriveForm(request.POST, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.auteur = request.user
            message.save()
            return redirect('covoiturage:boite_reception')
    else:
        form = MessagePriveForm(user=request.user)

    return render(request, 'covoiturage/envoyer_message.html', {'form': form})
