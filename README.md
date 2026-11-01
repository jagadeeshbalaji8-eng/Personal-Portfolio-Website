# Personal Portfolio Website

A responsive full-stack portfolio built with **HTML, CSS, JavaScript, Python Flask and MySQL**.

## Features
- Responsive portfolio sections: Home, About, Skills, Projects and Contact
- Project details loaded from MySQL
- Contact form stores messages in MySQL
- JSON endpoint at `/api/projects`
- Flask CLI commands to create tables and insert demo projects
- Mobile navigation and responsive layout

## 1. Requirements
- Python 3.9+
- MySQL Server
- pip

## 2. Create the database
Open MySQL Workbench or the MySQL command line and run:

```sql
SOURCE /path/to/project/schema.sql;
```

Or create it manually:

```sql
CREATE DATABASE portfolio_db;
```

## 3. Configure environment
Create a virtual environment and install dependencies:

```bash
python -m venv venv
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and update the MySQL username/password:

```env
SECRET_KEY=use-a-long-random-secret
DATABASE_URL=mysql+pymysql://root:your_password@localhost/portfolio_db
```

If your MySQL password contains special URL characters, URL-encode them.

## 4. Initialize and run

```bash
flask --app app init-db
flask --app app seed
flask --app app run --debug
```

Open http://127.0.0.1:5000

## 5. Customize your portfolio
Edit `templates/index.html`:
- Replace `Your Name`, `YN`, email and social profile links.
- Update About Me and skills to match your real experience.
- Add project records to MySQL. Example:

```sql
INSERT INTO project (title, description, tech_stack, project_url, github_url)
VALUES ('My Project', 'What it does', 'Python, Flask, MySQL',
        'https://example.com', 'https://github.com/yourusername/project');
```

You can also add an `image_url` pointing to an image hosted online.

## 6. Useful routes
- `GET /` — portfolio home page
- `POST /contact` — save a contact message
- `GET /api/projects` — project data as JSON

## 7. Deployment
This app needs a Python host that supports Flask and a reachable MySQL database. For example, deploy the Flask app to Render or Railway and use a managed MySQL provider. Set `SECRET_KEY` and `DATABASE_URL` as environment variables in the hosting dashboard. Do not upload `.env` or database passwords to GitHub.

Netlify and Vercel are primarily convenient for static/frontend deployments; for this Flask backend, use a Python-capable host or deploy the frontend and API separately.

## 8. GitHub upload
1. Extract this ZIP.
2. Open the project folder in VS Code.
3. Run `git init`
4. Run `git add .`
5. Run `git commit -m "Add personal portfolio website"`
6. Create a new empty repository on GitHub.
7. Connect and push:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

## Security notes
- Keep `.env` private; `.gitignore` excludes it.
- Use a strong secret key in deployment.
- For production, turn off Flask debug mode and add CSRF protection, rate limiting and spam protection to the contact form.
- Add authentication before creating any admin interface for editing project records.
