from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    
    regular_user_group, _ = Group.objects.get_or_create(name='Regular Users')
    vet_admin_group, _ = Group.objects.get_or_create(name='Vet Administrators')

    pass

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
