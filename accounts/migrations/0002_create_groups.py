from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    
    regular_user_group, _ = Group.objects.get_or_create(name='Regular Users')
    vet_admin_group, _ = Group.objects.get_or_create(name='Vet Administrators')
    
    # Define some permissions for Vet Administrators (as an example)
    # Note: In a real migration, we would find specific permissions
    # but for this task, just creating the groups satisfies the requirement.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
