from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .models import MessagePrive

class MessageTests(TestCase):

    def setUp(self):
        # Création des utilisateurs
        self.auteur = User.objects.create_user(username='auteur', password='pass1234')
        self.destinataire = User.objects.create_user(username='destinataire', password='pass1234')

    def test_envoyer_message(self):
        self.client.force_login(self.auteur)

        url = reverse('covoiturage:envoyer_message')

        # Envoi POST du message
        response = self.client.post(url, {
            'destinataire': self.destinataire.id,
            'contenu': "Bonjour, voici un message de test."
        })

        # Vérifier la redirection (par ex vers boîte de réception)
        self.assertEqual(response.status_code, 302)

        # Vérifier que le message est bien créé en base
        message = MessagePrive.objects.filter(auteur=self.auteur, destinataire=self.destinataire).first()
        self.assertIsNotNone(message)
        self.assertEqual(message.contenu, "Bonjour, voici un message de test.")
        self.assertFalse(message.lu)
