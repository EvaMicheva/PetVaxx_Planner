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

## Installation

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

## Configuration

1. **Copy the example environment variables file**:
   ```bash
   cp .env.example .env
   ```

2. **Configure variables in `.env`**:
   - `SECRET_KEY`: Django secret key.
   - `DEBUG`: Set to `True` for development, `False` for production.
   - **PostgreSQL database details**: Update `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` to match your local setup.

## Database & Data Loading

1. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

2. **Load sample data (using Makefile)**:
   The project includes a `Makefile` to quickly populate the database with species, vaccines, recommendation rules, pets, and sample vaccination plans.
   
   ```bash
   make load-all
   ```
   
   Alternatively, you can load fixtures individually:
   - `make load-vaccines`: Loads vaccines and species-specific rules.
   - `make load-pets`: Loads example pets.
   - `make load-planner`: Loads sample vaccination plans and doses.

## Running the Application

```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`.
Access the admin interface at `http://127.0.0.1:8000/admin/` (requires creating a superuser via `python manage.py createsuperuser`).

## Project Structure

- `pets/`: Pet profiles and lifestyle tracking.
- `vaccines/`: Vaccine definitions and recommendation logic.
- `planner/`: Management of vaccination plans and individual doses.
- `VetVax_Planner/`: Core Django project settings and configuration.

## 🚀 Future Roadmap
- **Medical History & Vaccine Records**: Implement a `VaccinationRecord` model to track actual shot dates and history.
- **Smart Restart Logic**: Automatically detect "expired" vaccines (like Lepto or FeLV) and generate a 2-dose "restart" schedule (4 weeks apart) if the last dose was too long ago.
- **Overdue Notifications**: Alert users when a booster is missed or a vaccination series needs to be restarted.
- **Enhanced UI**: Add a dashboard for quick overview of all pending vaccinations across all pets.
