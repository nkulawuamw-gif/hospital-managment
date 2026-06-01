# Hospital Management System (HMS)

Enterprise-level hospital management system built with Django REST Framework.

## Tech Stack

- **Backend**: Django 5.1, DRF, PostgreSQL, Redis, Celery
- **Frontend**: Bootstrap 5, DataTables, Chart.js, jQuery
- **Deployment**: Docker, Nginx, Gunicorn

## Quick Start (Docker)

```bash
cp .env.example .env
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

## Quick Start (Local)

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
```

Create PostgreSQL database:
```bash
createdb hms_db
```

Run migrations:
```bash
python manage.py migrate
python manage.py runserver
```

## Seed Data

```bash
python scripts/seed_data.py
```

Default superuser: `admin@hospital.com` / `Admin@123`

## API Docs

- Swagger: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Schema: http://localhost:8000/api/schema/

## Modules

| Module | API Endpoint | Description |
|--------|-------------|-------------|
| Auth | `/api/auth/` | JWT login, user management |
| Patients | `/api/patients/` | Registration, profiles |
| Appointments | `/api/appointments/` | Scheduling, check-in/out |
| Doctors | `/api/doctors/` | Profiles, schedules |
| EMR | `/api/emr/` | Consultation notes, SOAP, ICD codes |
| Inpatient | `/api/inpatient/` | Wards, beds, admissions |
| Pharmacy | `/api/pharmacy/` | Medicines, prescriptions |
| Laboratory | `/api/laboratory/` | Tests, results |
| Billing | `/api/billing/` | Invoices, payments |
| Insurance | `/api/insurance/` | Companies, claims |
| Inventory | `/api/inventory/` | Supplies, purchase orders |
| HR | `/api/hr/` | Employees, attendance, leave |
| Reports | `/api/reports/` | PDF/CSV/Excel export |
| Notifications | `/api/notifications/` | In-app, email, SMS |
| Audit | `/api/audit/` | Activity logs |

## Architecture

```
hms/
├── hms/              # Django project config
├── apps/             # All application modules
│   ├── accounts/     # Users, roles, permissions
│   ├── patients/     # Patient management
│   ├── appointments/ # Appointment scheduling
│   ├── doctors/      # Doctor profiles, schedules
│   ├── emr/          # Electronic Medical Records
│   ├── inpatient/    # Wards, beds, admissions
│   ├── pharmacy/     # Medicines, prescriptions
│   ├── laboratory/   # Lab tests, results
│   ├── billing/      # Invoices, payments
│   ├── insurance/    # Insurance companies, claims
│   ├── inventory/    # Supplies, purchase orders
│   ├── hr/           # HR management
│   ├── reports/      # Report generation
│   ├── notifications/# Notifications system
│   └── audit/        # Audit trail
├── docker-compose.yml
├── Dockerfile
├── nginx/
└── scripts/
```
