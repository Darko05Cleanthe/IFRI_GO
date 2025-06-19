# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import date, time
from django.core.exceptions import ValidationError
from django import forms


class Trajet(models.Model):
    conducteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trajets_conduits')
    depart = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    date_depart = models.DateField(default=date.today)  # valeur par défaut = aujourd’hui
    heure_depart = models.TimeField(default=time(12, 0))  # valeur par défaut = 12:00 midi
    places_disponibles = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    date_pub = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        datetime_str = f"{self.date_depart.strftime('%d/%m/%Y')} {self.heure_depart.strftime('%H:%M')}"
        return f"{self.depart} → {self.destination} le {datetime_str}"

class Reservation(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, related_name='reservations')
    passager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    nombre_passagers = models.PositiveIntegerField(default=1)
    date_reservation = models.DateTimeField(auto_now_add=True)
    
    statut = models.CharField(
        max_length=20,
        choices=[('en_attente', 'En attente'), ('confirmee', 'Confirmée'), ('annulee', 'Annulée')],
        default='en_attente'
    )

    # Nouveau champ pour la notification
    notification_vue = models.BooleanField(default=False)

    def __str__(self):
        return f"Réservation de {self.passager.username} pour {self.trajet}"



class MessagePrive(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_recus')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f"Message de {self.auteur.username} à {self.destinataire.username} le {self.date_envoi.strftime('%d/%m/%Y %H:%M')}"

class Publication(models.Model):
    conducteur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name="Conducteur"
    )
    trajet = models.ForeignKey(
        'Trajet',
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name="Trajet concerné"
    )
    titre = models.CharField(
        max_length=255,
        verbose_name="Titre de la publication"
    )
    contenu = models.TextField(
        verbose_name="Contenu de la publication"
    )
    date_pub = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de publication"
    )

    def clean(self):
        if self.conducteur != self.trajet.conducteur:
            raise ValidationError("Le conducteur de la publication doit être le conducteur du trajet.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Valide avant de sauvegarder
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Publication '{self.titre}' par {self.conducteur.username}"
    

class MessagePriveForm(forms.ModelForm):
    destinataire = forms.ModelChoiceField(
        queryset=User.objects.none(),  # Valeur par défaut, sera mise à jour dans __init__
        label="Choisir un destinataire",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    contenu = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    class Meta:
        model = MessagePrive
        fields = ['destinataire', 'contenu']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # On récupère user passé dans la vue
        super().__init__(*args, **kwargs)
        if user:
            self.fields['destinataire'].queryset = User.objects.exclude(id=user.id)
        else:
            self.fields['destinataire'].queryset = User.objects.all()
