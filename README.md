# CarePoint – Doctor Appointment Booking System

A Python full-stack project built with Django, SQLite, HTML, CSS and JavaScript-ready templates.

## Important: No Django Admin
This project intentionally does not install `django.contrib.admin`, does not register an `/admin/` URL, and does not require the Django admin site. Patients and doctors use their own custom website dashboards.

## Features
- Patient and doctor registration/login
- Doctor profile and specialization
- Search/filter doctors by specialization
- Patient appointment booking
- Doctor approval, rejection and completion
- Patient cancellation and appointment history
- SQLite persistence
- Custom responsive frontend

## Windows / VS Code setup
Open a terminal in the folder containing `manage.py`:

```powershell
py -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```

If you use Command Prompt instead of PowerShell, activate with:
```cmd
venv\Scripts\activate.bat
```

Open http://127.0.0.1:8000/

## How to test
1. Choose Register and create a **Doctor** account. Add specialization, qualification, experience and fee.
2. Logout, create a **Patient** account.
3. Find Doctors → View details → Book appointment.
4. Logout and sign in as the doctor to approve/reject/complete the appointment.
5. Sign back in as the patient to see the updated status.

## Database
The `db.sqlite3` file is created after migrations and stores users, profiles and appointments. Do not delete it if you want to keep saved records.

## Useful terminal commands
```powershell
py manage.py runserver
py manage.py makemigrations
py manage.py migrate
py manage.py shell
py manage.py test
```

## Production note
This is a learning/development starter. Before deployment, set a strong secret key, set `DEBUG=False`, configure `ALLOWED_HOSTS`, HTTPS, secure cookies, backups, and a production database. Do not store real patient medical records or sensitive health information in an unreviewed student project.
