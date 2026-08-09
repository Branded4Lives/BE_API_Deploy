# Video Presentation Script

Target length: 3 to 4 minutes. The video must stay under 5 minutes, and your face must be visible on camera while you present.

Before recording, have these ready:

- Deployed API URL: `https://YOUR-SERVICE.onrender.com`
- Swagger docs URL: `https://YOUR-SERVICE.onrender.com/docs`
- GitHub repository URL: `https://github.com/YOUR-USERNAME/YOUR-REPO`
- GitHub Actions page open to the latest passing workflow run

## 1. Introduction

Hi, my name is Brandon, and this is my API Deployment and CI/CD Pipeline project.

This project is a Flask backend API for a mechanic shop. It helps manage customers, mechanics, inventory parts, and service tickets. The final version is deployed on Render, uses a hosted PostgreSQL database, includes Swagger documentation, and has a GitHub Actions pipeline for testing and deployment.

## 2. What The Project Does

The API handles the main workflow for a mechanic shop.

Customers and mechanics can create accounts and log in. Mechanics can manage inventory parts, create service tickets, assign mechanics to those tickets, remove mechanics from tickets, and attach parts to tickets. Customers can also view their own service tickets through a protected route.

## 3. How It Works

At a high level, the project uses Flask with the application factory pattern. The app is organized into blueprints for customers, mechanics, inventory, service tickets, and documentation.

The database layer uses SQLAlchemy. For local development, the app can use SQLite. In production, it uses the hosted Render PostgreSQL database through the `DATABASE_URL` environment variable.

Sensitive settings are kept out of the code. The database URI and secret key are stored in environment variables, and the app reads them with Python's `os` package. The local `.env` file is listed in `.gitignore`, so those values are not pushed to GitHub.

For deployment, the old local app entrypoint was replaced with `flask_app.py`. That file imports `ProductionConfig` and passes it into `create_app`. Render starts the production app with:

```text
gunicorn flask_app:app
```

The deployment dependencies are frozen in `requirements.txt`, including `gunicorn` and `psycopg2`. I installed `python-dotenv` during setup, but removed it from `requirements.txt` after freezing, following the deployment instructions.

The production config also sets Swagger for the deployed API by using the live Render host and `https` as the scheme.

## 4. Quick Demo

First, I will open the deployed Render URL and show the root API response. This confirms the web service is live.

Next, I will open `/docs` to show the Swagger UI. The Swagger docs show the available endpoints, request bodies, response examples, and bearer-token security for protected routes.

Then I will demonstrate a short API workflow in Swagger: create a mechanic, log in as that mechanic, create an inventory part, create a service ticket, and assign the mechanic to that ticket.

I will also briefly show the GitHub repository and the project files that support deployment: `requirements.txt`, `config.py`, `flask_app.py`, and `.github/workflows/main.yaml`.

## 5. CI/CD Pipeline

The CI/CD workflow lives in `.github/workflows/main.yaml`.

The workflow runs when code is pushed to `main`, when a pull request targets `main`, or when I manually start it from GitHub Actions.

The pipeline has separate build, test, and deploy jobs. The build job installs dependencies and compiles the app. The test job runs:

```text
python -m unittest discover tests
```

The deploy job depends on the test job with `needs: test`, so Render deployment only runs after the tests pass. The Render service ID and Render API key are stored securely as GitHub repository secrets, not in the code.

## 6. Closing

That completes my API Deployment and CI/CD Pipeline project. The final submission includes the deployed Render service URL, the GitHub repository URL, and this video uploaded directly to Disco.
