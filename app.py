import os
import requests
from dotenv import load_dotenv
load_dotenv()
from urllib.parse import quote
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Generation

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------- AUTH ROUTES ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            flash("That username is already taken.")
            return redirect(url_for("register"))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ---------- MAIN APP ROUTES ----------

@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
@login_required
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        encoded_prompt = quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"

        response = requests.get(image_url, timeout=60)

        if response.status_code == 200:
            new_gen = Generation(
                user_id=current_user.id,
                prompt=prompt,
                image_url=image_url
            )
            db.session.add(new_gen)
            db.session.commit()

            return jsonify({"image_url": image_url})
        else:
            return jsonify({"error": "Image generation failed"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history")
@login_required
def get_history():
    generations = Generation.query.filter_by(user_id=current_user.id).order_by(Generation.created_at.desc()).all()
    history_list = [
        {"prompt": g.prompt, "image_url": g.image_url}
        for g in generations
    ]
    return jsonify(history_list)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)