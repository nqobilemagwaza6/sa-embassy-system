# Visa Application Tracking System (Django + Vue + SQLite)

This project is a **Visa Application Tracking System** for South Africans to apply for visas and track progress transparently.

## Tech stack (only)
- **Backend**: Python **Django** + **Django REST Framework (DRF)**
- **Frontend**: **Vue.js (Vue CLI)** + **JavaScript** + **Vue Router**
- **Database**: **SQLite**
- **Styling**: **Bootstrap + CSS**
- **HTTP**: native **fetch()** (no Axios)

## Roles (important)
- **Registered users (default)**:
  - When users register, they are created as normal users (**not staff**, **not superuser**).
  - They can only see and manage **their own** visa applications.
- **Admin**:
  - Admin actions are allowed for **superusers only**.
  - The admin UI is the Vue page: `http://localhost:8080/admin` (or your dev port).

## Project structure
```
visa-system/
  backend/   # Django + DRF API
  frontend/  # Vue.js UI (Vue CLI)
  venv/      # Python virtual environment (local)
```

## Backend setup (Django)
From PowerShell:

```powershell
cd "sa-embassy-system\sa-embassy-system\visa-system\backend"
..\venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend runs on:
- `http://127.0.0.1:8000`

## Frontend setup (Vue)
From PowerShell:

```powershell
cd "sa-embassy-system\sa-embassy-system\visa-system\frontend"
npm install
npm run serve
```

Frontend runs on:
- Usually `http://localhost:8080` (your port may differ, e.g. `8082`)

## CORS (if your Vue port changes)
If Vue runs on a different port (example `8082`), add it in:
- `backend/backend/settings.py` → `CORS_ALLOWED_ORIGINS`

Then restart Django.

## Main API endpoints (DRF)
Auth:
- `POST /api/auth/register/` → create normal user + returns token
- `POST /api/auth/login/` → returns token

User applications:
- `GET /api/applications/` → list my applications
- `POST /api/applications/` → create application
- `GET /api/applications/<id>/status-events/` → status history
- `POST /api/applications/<id>/documents/` → upload document for an application

Notifications:
- `GET /api/notifications/` → list my notifications
- `PATCH /api/notifications/<id>/mark-read/` → mark notification read

Admin (superuser only):
- `PATCH /api/applications/<id>/admin-status/` → update status + comment + creates notification

## Pages (Vue Router)
- `/login`
- `/register`
- `/dashboard` (user dashboard)
- `/admin` (admin dashboard — superuser only)

## Status values used
- `PENDING`
- `UNDER_REVIEW`
- `APPROVED`
- `REJECTED`

