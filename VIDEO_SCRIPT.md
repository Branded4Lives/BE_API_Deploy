# Video Presentation Script

Target length: 3 to 4 minutes. The assignment requires the video to stay under 5 minutes. Make sure your face is visible on camera while presenting.

## 1. Introduction

Hi, my name is Brandon, and this is my Mechanic Shop API Deployment project.

This project is a Flask backend API for a mechanic shop. It includes customers, mechanics, inventory, and service tickets, plus Swagger documentation, automated unittest coverage, Render deployment configuration, and a GitHub Actions CI/CD pipeline.

## 2. What The Project Does

The API manages the core data for a mechanic shop.

Customers and mechanics can be created and logged in. Mechanics can manage inventory parts and service tickets. Service tickets can be assigned to mechanics, have mechanics removed, and have inventory parts attached.

## 3. How It Works

The project uses Flask with the application factory pattern. Each major resource has its own blueprint folder with routes and Marshmallow schemas.

The app uses SQLAlchemy for the database. Locally it can run with SQLite, and in production it reads the Render PostgreSQL connection string from the `DATABASE_URL` environment variable.

The production entrypoint is `flask_app.py`, and Render starts it with `gunicorn flask_app:app`. Sensitive values like the database URL and secret key are stored as environment variables.

## 4. Quick Demo

First, I will open the deployed Render URL and show that the API responds.

Next, I will open `/docs` to show the Swagger UI. The docs show route categories, request bodies, response examples, and bearer-token security for protected routes.

Then I will demonstrate a simple workflow: create a customer, create a mechanic, log in as the mechanic, create an inventory part, create a service ticket, and assign a mechanic to that ticket.

I will also show the unittest command:

```text
python -m unittest discover tests
```

The tests cover every route and include negative tests like duplicate emails, invalid login, missing tokens, and missing resources.

## 5. CI/CD

The GitHub Actions workflow is in `.github/workflows/main.yaml`.

It installs dependencies and runs the unittest suite first. The deploy job depends on the test job, so Render deployment only triggers after tests pass.

The Render service ID and API key are stored as GitHub repository secrets.

## 6. Closing

That completes my API Deployment and CI/CD Pipeline project. The repository includes the production config, Render setup instructions, Swagger documentation, automated tests, and the CI/CD workflow.
