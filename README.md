# Hospital Management System

A Django web application for browsing doctors and departments, making appointment bookings, sending contact messages, and finding doctors by symptom keywords.

## Features

- User registration, login, and logout
- Doctor and department listings
- Appointment booking
- Contact form
- Symptom-based doctor recommendations at `/smart_recommendation/`
- Django admin for managing application data
- SQLite database and doctor image uploads

The recommendation feature matches text against a predefined list of symptom keywords and doctor specializations. It is not a diagnosis or a substitute for medical advice.

## Requirements

- Python compatible with the Django version in `requirements.txt`
- pip

## Run locally (Windows PowerShell)

From the project directory (the directory containing `manage.py`):

```powershell
py -m venv ..\env
..\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. The home page requires login; register at `/signup/` or create an administrator account:

```powershell
python manage.py createsuperuser
```

The Django admin is available at `/admin/`.

## Optional sample data

To create sample departments, doctors, and fictional bookings, run:

```powershell
python manage.py shell -c "import seed_clinic_data"
```

The script uses `get_or_create`, so running it again does not recreate matching records.

## Main URLs

| URL | Description |
| --- | --- |
| `/` | Login-protected home page |
| `/about/` | About page |
| `/doctors/` | Doctor directory |
| `/departments/` | Department directory |
| `/booking/` | Appointment booking form |
| `/contact/` | Contact form |
| `/signup/` | User registration |
| `/login/` | User login |
| `/logout/` | User logout |
| `/smart_recommendation/` | Symptom-based doctor search |
| `/admin/` | Django administration |

## Doctor recommendation from the Django shell

Run `python manage.py shell` from the directory containing `manage.py`, then:

```python
from home.recommendation import recommend_doctors

doctors = recommend_doctors("I have a skin rash and itching")
[
    (
        doctor.doctor_name,
        doctor.specialization,
        doctor.department_name.department_name,
    )
    for doctor in doctors
]
```

## Project layout

```text
hms/
├── hms/                 # Django project settings and root URLs
├── home/                # Application models, views, routes, and templates
├── media/               # Uploaded doctor images
├── manage.py
├── requirements.txt
└── seed_clinic_data.py  # Optional sample-data script
```

## Configuration and deployment

The default settings are for local development and use SQLite. Before deploying, configure a private `SECRET_KEY`, set `DEBUG = False`, configure `ALLOWED_HOSTS`, and review the database, static-file, media-file, and HTTPS settings. Do not use Django's development server as a production web server.
