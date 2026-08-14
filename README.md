# Develop — AI Image Generator

A full-stack web app that turns text prompts into AI-generated images. Built with Flask, has user accounts, and keeps a history of everything you've generated.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-backend-black)
![SQLite](https://img.shields.io/badge/SQLite-database-lightgrey)

## What it does
- Type a prompt, get an AI-generated image back in a few seconds
- Create an account and log in / log out (passwords are hashed, never stored as plain text)
- Every image you generate gets saved to your account and shows up in a sidebar so you can find it again
- A dark, amber-toned interface with a small "developing" animation when an image loads
- The prompt bar works like a chat input — type, hit enter or the arrow button, done
## Built with
| Part | What's used |
|---|---|
| Backend | Python, Flask |
| Database | SQLite (through Flask-SQLAlchemy) |
| Login system | Flask-Login, password hashing via Werkzeug |
| Image generation | Pollinations.ai |
| Frontend | HTML, CSS, plain JavaScript (no frameworks) |
| Tests | Pytest |
## How it works
1. You register or log in — Flask-Login handles keeping you signed in
2. You type a prompt and submit it
3. The backend sends that prompt to the Pollinations API
4. The image URL comes back and gets saved to the database under your account
5. It shows up in the main view, and also gets added to your history sidebar
6. Click any past item in the sidebar to pull that image back up
## Project structure
ai-image-gen/
├── app.py — routes, login logic, main app setup
├── models.py — database tables (User, Generation)
├── test_app.py — automated tests (pytest)
├── requirements.txt
├── .env — secret key + API key (not committed to git)
├── templates/
│ ├── index.html — main dashboard
│ ├── login.html
│ └── register.html
└── static/
├── style.css — main dashboard styling
├── auth.css — login/register page styling
└── script.js — handles requests, history, animations
## Running it locally

```bash
git clone https://github.com/SHOAIB8788/ai-image-gen.git
cd ai-image-gen

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```
You'll also need a `.env` file in the project root with:
Generate one with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Then run it:
```bash
python app.py
```
and open `http://127.0.0.1:5000`.

## Running the tests

```bash
pytest test_app.py -v
```
Covers password hashing, signing up, logging in, and making sure the dashboard is only reachable when logged in.

## Security notes

A few things worth mentioning since this started as a learning project and got cleaned up along the way:
- Passwords are hashed with Werkzeug's `generate_password_hash` (scrypt + a random salt per user) — never stored as plain text
- The Flask `SECRET_KEY` is generated randomly and loaded from `.env`, not hardcoded
- `.env` and the local database file are both excluded from git via `.gitignore`

## Ideas for later

- Delete individual items from history
- Download or export multiple images at once
- More image styles / aspect ratio options
- Actually deploy it somewhere instead of just running locally

## About

Made by SHOAIB8788 — a project for practicing Flask, basic auth, working with an external API, and putting together a frontend from scratch.