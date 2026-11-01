import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-secret-key")
db_url = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost/portfolio_db")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(255), nullable=False)
    project_url = db.Column(db.String(500))
    github_url = db.Column(db.String(500))
    image_url = db.Column(db.String(500))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route("/")
def index():
    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template("index.html", projects=projects)

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    if not name or not email or not message:
        flash("Please fill in all contact fields.", "error")
        return redirect(url_for("index") + "#contact")
    db.session.add(Message(name=name, email=email, message=message))
    db.session.commit()
    flash("Thanks! Your message has been saved.", "success")
    return redirect(url_for("index") + "#contact")

@app.route("/api/projects")
def api_projects():
    projects = Project.query.order_by(Project.id.desc()).all()
    return jsonify([{
        "id": p.id, "title": p.title, "description": p.description,
        "tech_stack": p.tech_stack, "project_url": p.project_url,
        "github_url": p.github_url, "image_url": p.image_url
    } for p in projects])

@app.cli.command("init-db")
def init_db():
    """Create database tables."""
    db.create_all()
    print("Database tables created.")

@app.cli.command("seed")
def seed():
    """Insert sample projects if the projects table is empty."""
    if Project.query.first():
        print("Projects already exist; skipping sample data.")
        return
    samples = [
        Project(title="Task Management App",
                description="A task manager to create, organize and track daily work.",
                tech_stack="Python, Flask, MySQL, HTML, CSS, JavaScript",
                github_url="https://github.com/yourusername/task-manager"),
        Project(title="E-commerce Website",
                description="A responsive shopping experience with product browsing and cart UI.",
                tech_stack="HTML, CSS, JavaScript, Flask",
                github_url="https://github.com/yourusername/ecommerce"),
        Project(title="Student Result Portal",
                description="A simple portal for viewing and managing student results.",
                tech_stack="Python, Flask, MySQL",
                github_url="https://github.com/yourusername/result-portal")
    ]
    db.session.add_all(samples)
    db.session.commit()
    print("Sample projects added.")

if __name__ == "__main__":
    app.run(debug=True)
