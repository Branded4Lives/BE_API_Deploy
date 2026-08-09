# Video Presentation Script

Target length: about 3 minutes. The video must stay under 5 minutes, and your face must be visible on camera.

## Open Before Recording

- Live API: `https://be-api-deploy.onrender.com`
- Swagger Docs: `https://be-api-deploy.onrender.com/docs`
- GitHub Repo: `https://github.com/Branded4Lives/BE_API_Deploy`
- GitHub Actions: latest passing `API CI/CD` workflow run

## Spoken Script

Hi, my name is Brandon, and this is my API Deployment and CI/CD Pipeline project.

This project is a Flask backend API for a mechanic shop. It manages customers, mechanics, inventory parts, and service tickets. A mechanic shop could use it to create users, track parts, create repair tickets, assign mechanics to tickets, and attach parts to those tickets.

At a high level, the app is built with Flask, SQLAlchemy, Marshmallow, and Swagger. The routes are organized into blueprints for customers, mechanics, inventory, and service tickets. SQLAlchemy handles the database, Marshmallow handles validation and serialization, and Swagger documents the available endpoints.

For deployment, the app is hosted on Render and connected to a Render PostgreSQL database. Sensitive values like the database URL and secret key are stored as environment variables instead of being hard-coded. The `.env` file is ignored by Git so secrets are not pushed to GitHub.

Render starts the production app with:

```text
gunicorn flask_app:app
```

That points Render to the Flask app inside `flask_app.py`, where `ProductionConfig` is passed into `create_app`.

Now I will show the deployed API. This is `https://be-api-deploy.onrender.com`, and the JSON response confirms the live service is running.

Next, I will open the Swagger docs at `/docs`. This page shows the API endpoints for customers, mechanics, inventory, and service tickets. For the demo, I will run one simple GET route, such as listing mechanics or inventory, to show the API responding through Swagger.

Now I will briefly show the GitHub repository. The important deployment files are `requirements.txt`, `config.py`, `flask_app.py`, and `.github/workflows/main.yaml`.

The GitHub Actions workflow has build, test, and deploy jobs. It installs dependencies, runs the unittest suite, and only triggers the Render deploy after the test job passes. The Render service ID and API key are stored as GitHub secrets.

That completes my project. The API is deployed on Render, connected to a hosted PostgreSQL database, documented with Swagger, and supported by a CI/CD pipeline through GitHub Actions.

## Fast Demo Checklist

Show these only. Do not explain every file or every route.

1. Live API root page
2. Swagger `/docs`
3. One simple GET route in Swagger
4. GitHub repo files
5. Latest passing GitHub Actions run

Do not show secret values from Render, GitHub, or `.env`.
