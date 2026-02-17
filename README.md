# VetVax Planner

VetVax Planner is a Django-based web application designed for managing veterinary vaccination schedules.

## Features (in development)
- Vaccination appointment management.
- Animal medical history tracking.
- Notifications for upcoming vaccinations.

## Prerequisites
- Python 3.x
- PostgreSQL

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd VetVax_Planner
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the example environment variables file:
   ```bash
   cp .env.example .env
   ```

2. Configure variables in `.env`:
   - `SECRET_KEY`: Django secret key.
   - `DEBUG`: Set to `True` for development, `False` for production.
   - PostgreSQL database details (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).

## Database

Ensure PostgreSQL is running and the database specified in `.env` is created. Then run the migrations:

```bash
python manage.py migrate
```

## Running the Application

```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`.
