# APIForge -> Build, test, organize, and debug APIs from one powerful workspace.

A full-stack app for building and executing saved API requests inside shared workspaces.

- **Frontend:** React (Vite + Tailwind + Zustand)
- **Backend:** FastAPI (JWT auth + SQLAlchemy)

---

## Project structure

- `backend/` - FastAPI API + database models/services
- `frontend/` - React UI for authentication, workspaces, collections and request execution

---

## Features

- **Authentication** (JWT)
  - Register / Login
  - Protected routes using `Authorization: Bearer <token>`
- **Workspaces**
  - Create workspaces
  - Add members (owner-only)
  - List workspaces the user belongs to
- **Collections**
  - Collections belong to a workspace
  - List collections for a workspace
- **API Requests**
  - Save requests (method, URL, headers, query params, body)
  - Execute saved requests
  - Store and retrieve execution history
- **Environments**
  - Environment variables attached to a workspace

---

## Local development

### 1) Backend (FastAPI)

1. Create environment variables (recommended: `.env` inside `backend/`).
   The backend reads:
   - `DATABASE_URL`
   - `SECRET_KEY` (optional; fallback exists)
   - `ALGORITHM` (optional; default `HS256`)
   - `ACCESS_TOKEN_EXPIRE_MINUTES` (optional; default `60`)

2. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

3. Run the server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend routes include:

- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `GET/POST /workspaces/`
- `POST /collections/`
- `GET /collections/workspace/{workspace_id}`
- `POST /requests/` and `GET /requests/collection/{collection_id}`
- `POST /requests/{request_id}/execute`

> Note: The database schema is created automatically at startup (`Base.metadata.create_all(...)`).

---

### 2) Frontend (React)

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Set API URL (optional):

- `VITE_API_URL` in your environment.

If not set, the app expects relative paths and uses Vite proxy.

3. Run the dev server:

```bash
npm run dev
```

The Vite dev server proxies these paths to the backend:

- `/auth`, `/workspaces`, `/collections`, `/requests`, `/users`, `/environments` → `http://localhost:8000`

---

## How to use (quick walkthrough)

1. Register a user in the UI.
2. Log in and create/select a **workspace**.
3. Create a **collection** inside the workspace.
4. Save an **API request** (method + URL + optional JSON body/headers).
5. Click **Execute** to run the request and view the response + stored history.

---

## Authentication

- Login returns:
  - `access_token`
  - `token_type` (`bearer`)
- For protected endpoints, send:

```http
Authorization: Bearer <access_token>
```

The frontend automatically logs out on `401`.

---

## Notes / troubleshooting

- **CORS/Proxy:** During development, rely on the Vite proxy (configured in `frontend/vite.config.js`).
- **Database:** Ensure `DATABASE_URL` is valid for your SQLAlchemy setup.
- **JWT secret:** If you don’t provide `SECRET_KEY`, the backend uses a fallback value (not suitable for production).

---

## License

Add your license here.
