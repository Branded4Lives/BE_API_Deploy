# Mechanic Shop API Deployment

Production-ready Flask API for a mechanic shop. The project includes Swagger documentation, unittest coverage, Render deployment configuration, and a GitHub Actions CI/CD pipeline.

## Features

- Flask application factory pattern
- Customer, mechanic, inventory, and service ticket blueprints
- Marshmallow request validation and response serialization
- Bearer-token protected customer and mechanic routes
- Swagger JSON at `/swagger.json`
- Swagger UI at `/docs`
- Local SQLite development database
- Render PostgreSQL production database support
- `gunicorn` production entrypoint through `flask_app.py`
- GitHub Actions build, test, and deploy workflow

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Marshmallow
- Flask-Swagger
- Flask-Swagger-UI
- python-jose
- gunicorn
- psycopg2-binary
- unittest

## Local Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file if needed. It is ignored by Git.

```bash
DATABASE_URL=sqlite:///be_api_deploy.db
SECRET_KEY=your-secret-key
SWAGGER_HOST=127.0.0.1:5000
SWAGGER_SCHEME=http
```

Run locally:

```bash
python run.py
```

Local Swagger UI:

```text
http://127.0.0.1:5000/docs
```

## Testing

Run the unittest suite:

```bash
python -m unittest discover tests
```

The tests cover customers, mechanics, inventory, service tickets, Swagger documentation, protected routes, and negative cases.

## Main Routes

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | API landing response |
| GET | `/swagger.json` | Swagger JSON spec |
| POST | `/customers/` | Create customer |
| POST | `/customers/login` | Customer login |
| GET | `/customers/` | Get customers |
| GET | `/customers/my-tickets` | Get current customer's service tickets |
| GET/PUT/DELETE | `/customers/<customer_id>` | Customer detail operations |
| POST | `/mechanics/` | Create mechanic |
| POST | `/mechanics/login` | Mechanic login |
| GET | `/mechanics/` | Get mechanics |
| GET/PUT/DELETE | `/mechanics/<mechanic_id>` | Mechanic detail operations |
| POST/GET | `/inventory/` | Create or list inventory |
| GET/PUT/DELETE | `/inventory/<part_id>` | Inventory detail operations |
| POST/GET | `/service-tickets/` | Create or list service tickets |
| GET/PUT/DELETE | `/service-tickets/<ticket_id>` | Service ticket detail operations |
| PUT | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign mechanic |
| PUT | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove mechanic |
| PUT | `/service-tickets/<ticket_id>/add-part/<part_id>` | Add inventory part |

## Render Deployment

1. Create a PostgreSQL database on Render.
2. Copy the database internal connection string.
3. Create a Render Web Service from this GitHub repository.
4. Set Auto Deploy to `Off` so GitHub Actions controls deployment after tests pass.
5. Use this build command:

```bash
pip install -r requirements.txt
```

6. Use this start command:

```bash
gunicorn flask_app:app
```

7. Add these Render environment variables:

```bash
DATABASE_URL=your-render-postgres-internal-url
SECRET_KEY=your-production-secret-key
SWAGGER_HOST=your-render-service-name.onrender.com
SWAGGER_SCHEME=https
```

The Swagger host should be only the base host, without `https://`.

## GitHub Actions CI/CD

The workflow lives at `.github/workflows/main.yaml`.

It runs the unittest suite on pull requests and pushes to `main`. On successful pushes to `main`, the deploy job triggers a Render deploy with the Render API.

Add these GitHub repository secrets:

```bash
RENDER_SERVICE_ID=your-render-service-id
RENDER_API_KEY=your-render-api-key
```

## Live API

Render URL: add your deployed Render URL here after deployment.

Swagger Docs: add your deployed `/docs` URL here after deployment.
