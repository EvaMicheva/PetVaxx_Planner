from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    regular_user_group, _ = Group.objects.get_or_create(name='Regular Users')
    vet_admin_group, _ = Group.objects.get_or_create(name='Vet Administrators')

    vaccine_ct = ContentType.objects.get(app_label='vaccines', model='vaccine')
    rule_ct = ContentType.objects.get(app_label='vaccines', model='recommendationrule')
    species_ct = ContentType.objects.get(app_label='vaccines', model='species')
    
    pet_ct = ContentType.objects.get(app_label='pets', model='pet')
    plan_ct = ContentType.objects.get(app_label='planner', model='plan')
    dose_ct = ContentType.objects.get(app_label='planner', model='dose')

    vet_permissions = Permission.objects.filter(
        content_type__in=[vaccine_ct, rule_ct, species_ct]
    )
    vet_admin_group.permissions.set(vet_permissions)


    regular_permissions = Permission.objects.filter(
        content_type__in=[pet_ct, plan_ct, dose_ct]
    )
    regular_user_group.permissions.set(regular_permissions)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
