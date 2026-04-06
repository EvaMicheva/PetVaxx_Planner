from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from accounts.models import Profile
from pets.models import Pet, MedicalCondition
from vaccines.models import Vaccine, Species, RecommendationRule
from planner.models import Plan, Dose
from planner.utils import DoseGenerator
from datetime import date, timedelta

User = get_user_model()

class BaseVetVaxTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.regular_group, _ = Group.objects.get_or_create(name='Regular Users')
        cls.vet_group, _ = Group.objects.get_or_create(name='Vet Administrators')

        cls.species = Species.objects.create(code='dog', name='Dog')
        cls.vaccine = Vaccine.objects.create(name='Rabies', category='core')
        cls.vaccine.applicable_species.add(cls.species)

        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
        )
        Profile.objects.create(
            user=cls.user,
            first_name='Test',
            last_name='User',
            phone='123456789',
        )

        cls.vet_user = User.objects.create_user(
            username='vetuser',
            email='vet@example.com',
            password='vetpassword123',
        )
        Profile.objects.create(
            user=cls.vet_user,
            first_name='Vet',
            last_name='Admin',
            phone='987654321',
        )
        cls.vet_user.groups.add(cls.vet_group)

    def login_regular_user(self):
        self.client.force_login(self.user)

    def login_vet_user(self):
        self.client.force_login(self.vet_user)

    def create_pet(self, owner, name='Buddy', species='dog', birth_date=None, **extra_fields):
        defaults = {
            'user': owner,
            'name': name,
            'species': species,
            'birth_date': birth_date or date.today(),
        }
        defaults.update(extra_fields)
        return Pet.objects.create(**defaults)


class TestAccountsViews(BaseVetVaxTestCase):
    def test_user_registration_creates_profile(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'New',
            'last_name': 'Person',
            'phone': '555-555',
        })

        self.assertEqual(response.status_code, 302)

        new_user = User.objects.get(username='newuser')
        self.assertTrue(Profile.objects.filter(user=new_user).exists())

    def test_vet_registration_assigns_group_and_sets_flag(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newvet',
            'email': 'newvet@example.com',
            'password1': 'vetpassword123',
            'password2': 'vetpassword123',
            'first_name': 'Vet',
            'last_name': 'New',
            'phone': '555-111',
            'is_vet': True,
        })

        self.assertEqual(response.status_code, 302)

        new_vet = User.objects.get(username='newvet')
        self.assertTrue(new_vet.groups.filter(name='Vet Administrators').exists())
        self.assertTrue(new_vet.is_vet)

    def test_profile_update_view_updates_profile_data(self):
        self.login_regular_user()

        response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '000-000',
        })

        self.assertEqual(response.status_code, 302)

        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.first_name, 'Updated')
        self.assertEqual(self.user.profile.last_name, 'Name')
        self.assertEqual(self.user.profile.phone, '000-000')

    def test_login_redirects_to_home(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpassword123',
        })

        self.assertRedirects(response, reverse('planner:home'))


class TestPetViews(BaseVetVaxTestCase):
    def test_pet_creation_with_medical_conditions(self):
        condition = MedicalCondition.objects.create(name='Allergy')
        pet = self.create_pet(
            owner=self.user,
            name='Buddy',
            species='dog',
            birth_date=date.today() - timedelta(days=365),
        )

        pet.medical_conditions.add(condition)

        self.assertEqual(pet.medical_conditions.count(), 1)
        self.assertEqual(pet.medical_conditions.first(), condition)

    def test_pet_visibility_regular_user_sees_only_own_pets(self):
        self.create_pet(owner=self.user, name='UserPet', species='dog')
        self.create_pet(owner=self.vet_user, name='VetPet', species='cat')

        self.login_regular_user()
        response = self.client.get(reverse('pets:list'))

        self.assertContains(response, 'UserPet')
        self.assertNotContains(response, 'VetPet')

    def test_pet_visibility_vet_admin_sees_all_pets(self):
        self.create_pet(owner=self.user, name='UserPet', species='dog')
        self.create_pet(owner=self.vet_user, name='VetPet', species='cat')

        self.login_vet_user()
        response = self.client.get(reverse('pets:list'))

        self.assertContains(response, 'UserPet')
        self.assertContains(response, 'VetPet')

    def test_pet_delete_confirmation_page_loads(self):
        pet = self.create_pet(owner=self.user, name='Buddy', species='dog')

        self.login_regular_user()
        response = self.client.get(reverse('pets:delete', kwargs={'pk': pet.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pets/pet_confirm_delete.html')

    def test_quick_plan_vet_sees_all_pets_in_form_queryset(self):
        user_pet = self.create_pet(owner=self.user, name='UserPet', species='dog')

        self.login_vet_user()
        response = self.client.get(reverse('planner:quick_add'))

        form = response.context['form']
        self.assertIn(user_pet, form.fields['pet'].queryset)


class TestPlannerViews(BaseVetVaxTestCase):
    def test_plan_creation_generates_expected_future_dose(self):
        RecommendationRule.objects.create(
            vaccine=self.vaccine,
            species=self.species,
            dose_number=1,
            due_age_weeks=8,
        )

        pet = self.create_pet(
            owner=self.user,
            name='Buddy',
            species='dog',
            birth_date=date.today() - timedelta(weeks=6),
        )

        self.login_regular_user()
        response = self.client.post(reverse('planner:add'), {
            'pet': pet.pk,
            'plan_start_date': date.today(),
            'status': 'draft',
        })

        self.assertEqual(response.status_code, 302)

        plan = Plan.objects.get(pet=pet)
        self.assertEqual(plan.doses.count(), 1)

        dose = plan.doses.first()
        self.assertEqual(dose.vaccine, self.vaccine)
        self.assertEqual(dose.dose_number, 1)
        self.assertEqual(dose.due_date, pet.birth_date + timedelta(weeks=8))
        self.assertFalse(dose.is_booster)

    def test_quick_plan_creates_pet_and_plan(self):
        self.login_regular_user()

        response = self.client.post(reverse('planner:quick_add'), {
            'name': 'QuickPet',
            'species': 'dog',
            'birth_date': date.today(),
            'lifestyle': 'indoor',
            'travels_abroad': False,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pet.objects.filter(name='QuickPet', user=self.user).exists())
        self.assertTrue(Plan.objects.filter(pet__name='QuickPet').exists())

    def test_plan_list_filtering_by_status(self):
        pet = self.create_pet(owner=self.user, name='Buddy', species='dog')
        final_plan = Plan.objects.create(
            pet=pet,
            plan_start_date=date.today(),
            status='final',
        )
        Plan.objects.create(
            pet=pet,
            plan_start_date=date.today(),
            status='draft',
        )

        self.login_regular_user()
        response = self.client.get(reverse('planner:list'), {'status': 'final'})

        plans = response.context['plans']
        self.assertEqual(list(plans), [final_plan])

    def test_plan_delete_confirmation_page_loads(self):
        pet = self.create_pet(owner=self.user, name='Buddy', species='dog')
        plan = Plan.objects.create(
            pet=pet,
            plan_start_date=date.today(),
            status='draft',
        )

        self.login_regular_user()
        response = self.client.get(reverse('planner:delete', kwargs={'pk': plan.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planner/plan_confirm_delete.html')


class TestVaccinesApiAndCommon(BaseVetVaxTestCase):
    def test_vaccine_search_filter(self):
        Vaccine.objects.create(name='Parvo', category='core')

        response = self.client.get(reverse('vaccines:list'), {'search_query': 'Parvo'})

        self.assertContains(response, 'Parvo')
        self.assertNotContains(response, 'Rabies')

    def test_api_vaccine_list_returns_all_vaccines(self):
        response = self.client.get(reverse('vaccines:api_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), Vaccine.objects.count())

    def test_api_returns_json_content_type(self):
        response = self.client.get(reverse('vaccines:api_list'))

        self.assertIn('application/json', response['Content-Type'])

    def test_contact_form_invalid_email(self):
        response = self.client.post(reverse('common:contact'), {
            'name': 'Test',
            'email': 'invalid@spam.abc',
            'subject': 'Help',
            'message': 'Hello',
        })

        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Please use a valid business or personal email address.',
            form.errors['email'],
        )


class TestPermissionsAndAccess(BaseVetVaxTestCase):
    def test_anonymous_user_is_redirected_from_profile_page(self):
        response = self.client.get(reverse('accounts:profile'))

        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_is_redirected_from_quick_plan_page(self):
        response = self.client.get(reverse('planner:quick_add'))

        self.assertEqual(response.status_code, 302)

    def test_regular_user_cannot_open_other_users_pet_delete_page(self):
        other_pet = self.create_pet(owner=self.vet_user, name='VetPet', species='cat')

        self.login_regular_user()
        response = self.client.get(reverse('pets:delete', kwargs={'pk': other_pet.pk}))

        self.assertEqual(response.status_code, 403)

    def test_regular_user_cannot_delete_other_users_pet(self):
        other_pet = self.create_pet(owner=self.vet_user, name='VetPet', species='cat')

        self.login_regular_user()
        response = self.client.post(reverse('pets:delete', kwargs={'pk': other_pet.pk}))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Pet.objects.filter(pk=other_pet.pk).exists())

    def test_regular_user_cannot_delete_other_users_plan(self):
        other_pet = self.create_pet(owner=self.vet_user, name='VetPet', species='cat')
        other_plan = Plan.objects.create(
            pet=other_pet,
            plan_start_date=date.today(),
            status='draft',
        )

        self.login_regular_user()
        response = self.client.post(reverse('planner:delete', kwargs={'pk': other_plan.pk}))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Plan.objects.filter(pk=other_plan.pk).exists())

    def test_quick_plan_regular_user_sees_only_own_pets_in_form_queryset(self):
        own_pet = self.create_pet(owner=self.user, name='UserPet', species='dog')
        other_pet = self.create_pet(owner=self.vet_user, name='VetPet', species='cat')

        self.login_regular_user()
        response = self.client.get(reverse('planner:quick_add'))

        form = response.context['form']
        pet_queryset = form.fields['pet'].queryset

        self.assertIn(own_pet, pet_queryset)
        self.assertNotIn(other_pet, pet_queryset)


class TestDoseGeneratorService(BaseVetVaxTestCase):
    def test_generate_creates_one_future_non_booster_dose(self):
        RecommendationRule.objects.create(
            vaccine=self.vaccine,
            species=self.species,
            dose_number=1,
            due_age_weeks=8,
            repeat_every_months=None,
        )

        pet = self.create_pet(
            owner=self.user,
            name='Buddy',
            species='dog',
            birth_date=date.today() - timedelta(weeks=6),
        )
        plan = Plan.objects.create(
            pet=pet,
            plan_start_date=date.today(),
            status='draft',
        )

        generated_doses = DoseGenerator(plan).generate()

        self.assertEqual(len(generated_doses), 1)
        self.assertEqual(plan.doses.count(), 1)

        dose = plan.doses.get()
        self.assertEqual(dose.vaccine, self.vaccine)
        self.assertEqual(dose.dose_number, 1)
        self.assertEqual(dose.due_date, pet.birth_date + timedelta(weeks=8))
        self.assertFalse(dose.is_booster)

    def test_generate_skips_past_due_non_repeating_rule(self):
        RecommendationRule.objects.create(
            vaccine=self.vaccine,
            species=self.species,
            dose_number=1,
            due_age_weeks=8,
            repeat_every_months=None,
        )

        pet = self.create_pet(
            owner=self.user,
            name='OlderBuddy',
            species='dog',
            birth_date=date.today() - timedelta(weeks=10),
        )
        plan = Plan.objects.create(
            pet=pet,
            plan_start_date=date.today(),
            status='draft',
        )

        generated_doses = DoseGenerator(plan).generate()

        self.assertEqual(generated_doses, [])
        self.assertEqual(plan.doses.count(), 0)
        self.assertEqual(Dose.objects.filter(plan=plan).count(), 0)

