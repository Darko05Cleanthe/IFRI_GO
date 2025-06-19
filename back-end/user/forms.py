from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telephone', 'role', 'image']
        widgets = {
            'telephone': forms.TextInput(attrs={'placeholder': 'Téléphone'}),
            'role': forms.Select(),
            'image': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = "Changer l'image de profil"

