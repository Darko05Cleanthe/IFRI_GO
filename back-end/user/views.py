from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserUpdateForm, ProfileUpdateForm
from covoiturage.models import Trajet, Publication, MessagePrive, Reservation
from django.db.models import Q
from django.contrib.auth.models import Group
from django.db import IntegrityError





# Create your views here.

def connexion_view(request):
    # Fonction pour afficher la page de connexion
    if request.method == "POST":
        identifiant = request.POST.get('identifiant')  # email en réalité
        mot_de_passe = request.POST.get('password')    # le nom du champ dans le formulaire

        try:
            user_obj = User.objects.get(email=identifiant)
            user = authenticate(request, username=user_obj.username, password=mot_de_passe)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect.")

    return render(request, 'user/connexion.html')

def inscription_view(request):
    if request.method == "POST":
        # Récupération des champs du formulaire
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        # Vérification des champs requis
        if not all([nom, prenom, email, telephone, password, confirm_password, role]):
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'user/inscription.html')

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'user/inscription.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, 'user/inscription.html')

        # Génération d'un username unique
        username = generate_unique_username(email)

        try:
            # Création de l'utilisateur
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=prenom,
                last_name=nom
            )
        except IntegrityError:
            messages.error(request, "Une erreur est survenue lors de la création de l'utilisateur.")
            return render(request, 'user/inscription.html')

        # Création du profil
        profil, created = Profile.objects.get_or_create(
            user=user,
            defaults={'telephone': telephone, 'role': role}
        )
        if not created:
            profil.telephone = telephone
            profil.role = role
            profil.save()

        # Ajout au groupe correspondant au rôle
        if role == 'conducteur':
            group, _ = Group.objects.get_or_create(name='Conducteur')
        elif role == 'passager':
            group, _ = Group.objects.get_or_create(name='Passager')
        else:
            group = None

        if group:
            user.groups.add(group)

        messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
        return redirect('connexion')  # adapte ce nom à ta route

    return render(request, 'user/inscription.html')
    return render(request, 'user/inscription.html')

def bienvenue_view(request):
    # Fonction pour afficher la page d'acceuil
    return render(request, 'user/bienvenue.html')

from django.utils import timezone
from datetime import datetime, time

from django.utils import timezone
from django.db.models import Q

@login_required
def page_utilisateur_view(request):
    user = request.user

    trajets = Trajet.objects.filter(conducteur=user).order_by('-date_pub')
    publications = Publication.objects.filter(conducteur=user).order_by('-date_pub')
    messages_recus = MessagePrive.objects.filter(destinataire=user).order_by('-date_envoi')[:5]

    maintenant = timezone.now()

    # ✅ Réservations qui doivent s'afficher comme notifications
    nouvelles_reservations_qs = Reservation.objects.filter(
        Q(trajet__conducteur=user),
        Q(notification_vue=False) | Q(trajet__date_depart__gte=maintenant)
    ).order_by('-date_reservation')

    nouvelles_reservations = list(nouvelles_reservations_qs)  # 👈 Pour affichage

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

        if not trajets.exists():
            erreurs.append("Vous devez d'abord publier au moins un trajet avant de créer une publication.")

        if not erreurs:
            Publication.objects.create(
                titre=titre,
                contenu=contenu,
                conducteur=user,
                trajet=trajet
            )
            messages.success(request, "Publication créée avec succès.")
            return redirect('page_utilisateur')

    # ❌ Ne plus marquer comme vues automatiquement
    # nouvelles_reservations_qs.update(notification_vue=True)

    context = {
        'trajets': trajets,
        'publications': publications,
        'messages_recus': messages_recus,
        'nouvelles_reservations': nouvelles_reservations,
        'erreurs': erreurs,
        'form_data': form_data,
    }

    return render(request, 'user/page_utilisateur.html', context)


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('bienvenue')  # redirige vers la page d'accueil
    return render(request, 'user/logout.html')

@login_required
def home_view(request):
    return render(request, 'user/home.html')

@login_required
def profil_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('profil')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'user/profil.html', context)

def generate_unique_username(email):
    
    base_username = email.split('@')[0]
    username = base_username
    compteur = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}{compteur}"
        compteur += 1

    return username
