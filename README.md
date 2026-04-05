# VetVax Planner

VetVax Planner is a Django-based web application designed for managing veterinary vaccination schedules for pets. It helps pet owners track vaccination history and plan future doses based on species-specific recommendation rules.

### ⚠️ Disclaimer & Educational Purpose
This application was developed by a **Veterinary Technician** as a **mock model** for educational purposes to learn the Django web framework. 

- **Professional Advice**: This application **cannot and does not remove the need for a veterinarian**. Always consult with a qualified veterinarian for medical advice, diagnoses, or treatment for your pets.
- **Accuracy**: The vaccination schedules and recommendation logic are based on the **Stiko Vet (Ständige Impfkommission Veterinärmedizin) requirements in Germany as of 2026**. However, since this is a learning project, it should not be used as a primary source for medical decisions.

## Features

- **Pet Management**: Track pets, their species, birth dates, and lifestyle (indoor, outdoor, travel).
- **Vaccine Database**: Store information about different vaccines, categories (core vs. optional), and applicable species.
- **Recommendation Rules**: Define vaccination schedules based on age (weeks/months) and lifestyle requirements.
- **Vaccination Plans**: Create personalized vaccination plans for each pet.
- **Quick Plan Generator**: A unified tool to create a new pet and their full vaccination schedule in a single step, or quickly generate a plan for an existing pet.
- **Dose Tracking**: Schedule and track individual doses, including boosters.
- **Smart Filtering & Sorting**: Easily manage vaccination plans by status (Draft/Final) and sort by start date or creation date.
- **Automated Data Loading**: Quick setup with comprehensive sample fixtures.
- **Enhanced Admin Interface**: Manage all data easily through a customized Django admin.

## Prerequisites

- Python 3.10+
- PostgreSQL
- `make` (optional, for automation)

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd VetVax_Planner
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   The application requires several environment variables for security and database settings.
   - Copy the example `.env` file:
     ```bash
     cp .env.example .env
     ```
   - The default configuration uses **SQLite** for the easiest local setup ("without modifications"). If you prefer a different database (e.g., PostgreSQL), update the `DATABASES` dictionary in `VetVax_Planner/settings.py`.

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Load Sample Data**:
   The project includes a `Makefile` to quickly populate the database with species, vaccines, recommendation rules, pets, and sample vaccination plans.
   
   ```bash
   make load-all
   ```
   
   Alternatively, load fixtures individually:
   ```bash
   python manage.py loaddata vaccines/fixtures/petvaxx_seed_data_fixture.json
   python manage.py loaddata pets/fixtures/pets_data.json
   python manage.py loaddata planner/fixtures/plans_and_doses.json
   ```

7. **Create a Superuser** (to access `/admin/`):
   ```bash
   python manage.py createsuperuser
   ```

8. **Running the Application**:
   ```bash
   python manage.py runserver
   ```
   The application will be accessible at `http://127.0.0.1:8000/`.

## Project Requirements Checklist

- **Public & Private Sections**: Homepage and About are public; Pets and Plans require authentication.
- **User Extension**: Custom `User` model with `is_vet` boolean in `accounts/models.py`.
- **User Groups**: "Vet Administrators" and "Regular Users" created via migrations and assigned on registration.
- **5 Django Apps**: `accounts`, `pets`, `vaccines`, `planner`, `common`.
- **Database Architecture**: 5+ models, M2M (species/vaccines, pets/medical conditions), One-to-One (User/Profile), FK (Pet/User, Plan/Pet, Dose/Plan).
- **Forms & Validations**: 7+ forms with labels, placeholders, help texts, and custom clean methods.
- **Views**: 90% Class-Based Views (CBVs) with proper form handling and redirects.
- **Asynchronous Processing**: Simulated welcome email task using Python's `asyncio` in `accounts/views.py`.
- **API**: RESTful endpoint for vaccines using Django REST Framework.
- **Templates**: 15+ templates using inheritance, partials (`_navbar.html`, `_footer.html`), and custom filters (`planner_extras.py`).
- **Security**: Environment variables used for secrets; CSRF protection; Delete confirmation steps.
- **Tests**: 15+ automated tests in `tests_comprehensive.py`.

## Project Structure

- `pets/`: Pet profiles and lifestyle tracking.
- `vaccines/`: Vaccine definitions and recommendation logic.
- `planner/`: Management of vaccination plans and individual doses.
- `VetVax_Planner/`: Core Django project settings and configuration.

## 🚀 Project Highlights
- **5+ Django Apps:** `accounts`, `pets`, `vaccines`, `planner`, `common`.
- **Advanced Permissions:** Distinct roles for "Vet Administrators" (global view/manage) and "Regular Users" (personal data only).
- **RESTful API:** Developed with Django REST Framework, providing vaccine data endpoints.
- **Asynchronous Processing:** Built-in simulated email system using Python's `asyncio` on user registration.
- **Robust Validation:** Custom clean methods in 7+ forms (e.g., birth date validation, email domain checks).
- **Medical Tracking:** Supports Many-to-Many relationships for species-specific vaccines and pet medical conditions.
- **Comprehensive Testing:** Over 15 automated tests covering core business logic and user scenarios.

## 🚀 Future Roadmap
- **Medical History & Vaccine Records**: Implement a `VaccinationRecord` model to track actual shot dates and history.
- **Smart Restart Logic**: Automatically detect "expired" vaccines (like Lepto or FeLV) and generate a 2-dose "restart" schedule (4 weeks apart) if the last dose was too long ago.
- **Overdue Notifications**: Alert users when a booster is missed or a vaccination series needs to be restarted.
- **Enhanced UI**: Add a dashboard for quick overview of all pending vaccinations across all pets.
