from django.contrib.auth.models import Group

def run():
    group_names = ['Conducteur', 'Passager']
    for name in group_names:
        group, created = Group.objects.get_or_create(name=name)
        if created:
            print(f"Groupe '{name}' créé.")
        else:
            print(f"Groupe '{name}' existe déjà.")
