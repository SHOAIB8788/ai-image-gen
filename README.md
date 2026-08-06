# Develop — AI Image Generator

A full-stack web app that turns text prompts into AI-generated images, with user accounts and a saved generation history — built with Flask and a custom darkroom-inspired interface.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-backend-black)
![SQLite](https://img.shields.io/badge/SQLite-database-lightgrey)

## Features

- **Text-to-image generation** — describe anything, get an AI-generated image back in seconds
- **User authentication** — secure register, login, and logout with hashed passwords
- **Generation history** — every image you create is saved to your account and shown in a sidebar for quick access
- **Custom interface** — a dark, amber-lit "darkroom" aesthetic with a print-developing animation on every generation
- **Responsive prompt bar** — chat-style input with an inline generate button and auto-resizing textarea

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite via Flask-SQLAlchemy |
| Auth | Flask-Login, Werkzeug password hashing |
| Image generation | Pollinations.ai API |
| Frontend | HTML, CSS, vanilla JavaScript |

## How It Works

1. User registers or logs in — session managed by Flask-Login
2. User types a prompt in the input bar and hits the arrow button (or Enter)
3. Flask backend sends the prompt to the Pollinations image API
4. The generated image URL is saved to the database, tied to the logged-in user
5. The image renders in the main view with a develop-style reveal animation
6. Past generations appear instantly in the left sidebar, and can be reopened with a click

## Project Structure
ai-image-gen/
├── app.py # Flask app, routes, auth logic
├── models.py # Database models (User, Generation)
├── requirements.txt
├── templates/
│ ├── index.html # Main dashboard
│ ├── login.html
│ └── register.html
└── static/
├── style.css # Main dashboard styling
├── auth.css # Login/register page styling
└── script.js # Frontend logic (fetch, history, animations)
## Running Locally

\`\`\`bash
# Clone the repository
git clone https://github.com/your-username/ai-image-gen.git
cd ai-image-gen

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
\`\`\`

Then open `http://127.0.0.1:5000` in your browser.

## Future Improvements

- Ability to delete individual history items
- Downloadable image gallery / bulk export
- Support for multiple image styles or aspect ratios
- Deploy to a live hosting platform

## Author

Built by [SHOAIB8788] as a learning project to practice full-stack development — Flask backend, REST API integration, authentication, and frontend design.