# forms.py
from django import forms
from .models import Trajet, Reservation, Publication, MessagePrive

class TrajetForm(forms.ModelForm):
    class Meta:
        model = Trajet
        fields = ['depart', 'destination', 'date_depart', 'heure_depart', 'places_disponibles', 'prix', 'description']
        widgets = {
            'date_depart': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_depart': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'depart': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'places_disponibles': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nombre_passagers']  # ne mettre QUE les champs du modèle ici
        widgets = {
            'nombre_passagers': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,  # optionnel, tu peux aussi mettre max dynamique
            }),
        }

    # Si tu veux ajouter un champ infos_complementaires non présent dans le modèle :
    infos_complementaires = forms.CharField(
        label="Informations complémentaires",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    )
        

class MessageForm(forms.ModelForm):
    class Meta:
        model = MessagePrive
        fields = ['destinataire', 'contenu']
        widgets = {
            'destinataire': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'contenu': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On désactive aussi le champ pour que Django ne le prenne pas en compte à la validation
        self.fields['destinataire'].disabled = True

        
class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['titre', 'contenu', 'trajet']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'trajet': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            # Limiter la liste des trajets aux trajets du conducteur connecté
            self.fields['trajet'].queryset = self.user.trajets_conduits.all()
        else:
            self.fields['trajet'].queryset = Publication.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        trajet = cleaned_data.get('trajet')

        if trajet and self.user and trajet.conducteur != self.user:
            raise forms.ValidationError("Vous ne pouvez sélectionner que vos propres trajets.")
        return cleaned_data
