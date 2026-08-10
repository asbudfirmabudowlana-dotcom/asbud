# BuildSmart AI

Production-oriented SaaS starter for construction companies. It contains a Next.js dashboard, FastAPI API, PostgreSQL, JWT authentication and workspace-scoped clients and projects.

## Run locally

1. Copy `.env.example` to `.env` and replace the development secrets.
2. Run `docker compose up --build`.
3. Open `http://localhost:3000` and create the first workspace from the registration screen.

The API documentation is available at `http://localhost:8000/docs`.

## Deploy on Railway

The repository now includes a root `Dockerfile` and `railway.toml`, so Railway starts the API and Polish web application as one service. Add a Railway PostgreSQL service and set `DATABASE_URL` in the app service to `${{Postgres.DATABASE_URL}}`. Then add `JWT_SECRET` and `OPENAI_API_KEY` as sealed variables. The step-by-step Polish guide is in [RAILWAY.md](RAILWAY.md).

## Layout

- `apps/web` — Next.js 15 application
- `apps/api` — FastAPI service and database migrations
- `docker-compose.yml` — local production-like runtime

## Security notes

The API enforces workspace isolation through the authenticated user's `company_id`. Change all placeholder secrets before deployment and use managed PostgreSQL, Redis and object storage in production.
