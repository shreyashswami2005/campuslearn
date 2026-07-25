# CampusLearn

College learning platform (Django). **Students** use the site; **teachers** use `/admin/`.

## Local setup (Windows)

```powershell
cd "c:\xampp\htdocs\pharma shop\college_lms"
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_courses
python manage.py runserver
```

Open http://127.0.0.1:8000/

### Demo accounts (after seed)

| Role | Username | Password | URL |
|------|----------|----------|-----|
| Teacher | `teacher` | `teacher123` | `/admin/` |
| Student | `student` | `student123` | `/` |

## Deploy on Vercel (student + teacher, one site)

Vercel cannot keep SQLite files. Use a free cloud Postgres (Neon, Supabase, or Vercel Storage → Postgres).

### 1. Push this project to GitHub

Create a GitHub repo and upload the **`college_lms`** folder contents (or set Vercel Root Directory to `college_lms` if the repo is the parent folder).

### 2. Create a Postgres database

Example with [Neon](https://neon.tech): create a project → copy the connection string (`DATABASE_URL`).

### 3. Import on Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repo
3. **Root Directory**: `college_lms` (if the repo contains that folder)
4. Framework: Django (auto-detected via `manage.py`)
5. Add **Environment Variables** (Production + Preview):

| Name | Value |
|------|--------|
| `SECRET_KEY` | long random string |
| `DEBUG` | `False` |
| `DATABASE_URL` | your Postgres URL |

6. Deploy

### 4. After first deploy

On your machine (with `DATABASE_URL` in `.env.local`):

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_courses
python manage.py createsuperuser
```

Or use Vercel CLI:

```bash
cd college_lms
npx vercel login
npx vercel link
npx vercel env pull .env.local
python manage.py migrate
python manage.py seed_courses
```

### 5. Open the live site

- Students: `https://YOUR-PROJECT.vercel.app/`
- Teachers: `https://YOUR-PROJECT.vercel.app/admin/`

Same login system for both roles (`is_staff` users can open admin).

## Project layout

```
college_lms/
  config/          # settings, wsgi (Vercel entry)
  accounts/        # auth, dashboard, profile
  courses/         # courses, results, attendance
  build.py         # runs migrate on Vercel build
  vercel.json
  requirements.txt
```

## Notes

- Local DB: SQLite. Production DB: Postgres via `DATABASE_URL`.
- Static files are collected automatically by Vercel when `STATIC_ROOT` is set.
