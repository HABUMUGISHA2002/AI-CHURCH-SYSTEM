# AI Church Assistant System

Professional full-stack starter for an AI-powered church management platform.

## Stack

- Frontend: React, Vite, Tailwind CSS, React Router, Axios
- Backend: Python Flask, Flask RESTful API, JWT, SQLAlchemy
- Database: MySQL
- AI and integrations: OpenAI API, Bible API, WhatsApp, Email, SMS

## Project Structure

```text
AI_CHURCH_ASSISTANT_SYSTEM/
  backend/
    app/
      api/
      models/
      services/
      utils/
    run.py
    requirements.txt
    .env.example
  frontend/
    src/
      api/
      components/
      context/
      layouts/
      pages/
      routes/
    package.json
    .env.example
```

## Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
flask --app run.py db init
flask --app run.py db migrate -m "initial schema"
flask --app run.py db upgrade
python run.py
```

Update `backend/.env` with your MySQL connection and API keys.

## Frontend Setup

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

## Hosting

Recommended production setup:

- One web service for this repository using the included `Dockerfile`.
- One managed MySQL database.
- Environment variables copied from `backend/.env.production.example`.

### Deploy Checklist

1. Push this project to GitHub.
2. Create a MySQL database on your hosting provider.
3. Create a web service from this repo and use Docker deploy/build.
4. Set these required web service environment variables:

```text
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=<long-random-secret>
JWT_SECRET_KEY=<long-random-secret>
DATABASE_URL=mysql+pymysql://USER:PASSWORD@HOST:PORT/DATABASE
FRONTEND_ORIGIN=https://your-live-domain
```

5. After the first deploy, run the database migration command on the web service:

```bash
flask --app run.py db upgrade
```

The deployed app serves the React frontend and Flask API from one public URL. API routes live under `/api`.

## Core Capabilities

- JWT authentication with role-based access control
- Member profiles, groups, ministries, and attendance
- AI Bible Q&A with conversation history
- AI sermon outline and full-sermon generation
- Event creation, calendars, and reminders
- Notifications over Email, WhatsApp, and SMS
- Analytics endpoints for attendance, members, events, sermons, and messages
- WhatsApp webhook endpoint for Bible questions and reminders

## Default Roles

- `admin`
- `pastor`
- `leader`
- `member`

## Notes

This repository is intentionally structured as a strong MVP foundation. External providers are wrapped behind service classes so real credentials and vendor-specific implementations can be added without changing API routes.
