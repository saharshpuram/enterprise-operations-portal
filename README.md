# Enterprise Operations Portal

Hands-on engineering training: Vue 3 + TypeScript + PrimeVue, Node.js + Express + TypeScript, PostgreSQL + Prisma, Docker Compose, GitHub and AWS.

## Run locally

Requires Docker Desktop with Docker Compose.

```bash
git clone https://github.com/saharshpuram/enterprise-operations-portal.git
cd enterprise-operations-portal
git switch feat/initial-app-scaffold
docker compose up --build
```

- Frontend: http://localhost:5173
- API: http://localhost:3000/api/incidents
- Health: http://localhost:3000/health

Database schema and fictional sample incidents are initialized automatically.

## Day 1 task

Trace the incidents API call from `frontend/src/App.vue` through `backend/src/server.ts` and `backend/prisma/schema.prisma`. Identify why the response includes the assignee's name but not their department.

## Workflow

Create feature branches from main, open pull requests, review, and merge only after verification. Never push training changes directly to main.

## Scope

This is a local-development learning scaffold, not production-ready. Before production deployment add authentication, authorization, tests, secure configuration, controlled migrations, and deployment checks. Database credentials in Compose are for local use only.
