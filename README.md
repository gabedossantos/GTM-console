# JourneyLens GTM Console

JourneyLens is a demo GTM console that highlights AI-generated customer insights across accounts, interactions, and feedback loops. The project ships with a FastAPI backend, a Next.js frontend, and seeded CSV data so you can explore the experience locally without external services.


## 🔧 Tech Stack


## 📣 What’s Next?
A modern Go-To-Market (GTM) dashboard for customer intelligence. Visualize accounts, interactions, and feedback with a FastAPI backend and a Next.js frontend. Includes demo data for easy local exploration—no external dependencies required.

---

## Architecture

![Architecture Diagram](journeylens_architecture.png)

- **Backend:** FastAPI (Python), SQLite, SQLAlchemy
- **Frontend:** Next.js (React, TypeScript, TailwindCSS)
- **Data:** Seeded CSVs for accounts, contacts, interactions, and insights

---

## Run in 5 Minutes

1. **Clone & Setup**
  ```bash
  git clone https://github.com/gabedossantos/GTM-console.git
  cd GTM-console
  python3 -m venv .venv && source .venv/bin/activate
  pip install -r backend/requirements.txt
  cd frontend && npm install && cd ..
  ```
2. **Start Backend**
  ```bash
  uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
  ```
3. **Start Frontend**
  ```bash
  cd frontend && npm run dev
  ```
4. **Open**
  - Frontend: http://localhost:3000
  - API docs: http://localhost:8000/docs

---

## Seed Data

Demo data is loaded automatically from CSV files in the project root:
- `demo_accounts.csv`
- `demo_contacts.csv`
- `demo_interactions.csv`
- `demo_expected_insights.csv`

No manual migration or seeding required.

---

## Project Structure

```
backend/           # FastAPI app, models, API, services
frontend/          # Next.js app, UI components
*.csv              # Demo data
*.png, *.md        # Diagrams, docs
```

---

## Scripts

- **Backend install:** `pip install -r backend/requirements.txt`
- **Frontend install:** `cd frontend && npm install`
- **Backend run:** `uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000`
- **Frontend run:** `cd frontend && npm run dev`
- **Test backend:** `python -m pytest backend/tests`
- **Lint frontend:** `cd frontend && npm run lint`

---

## License

MIT

| Tool | Version |
| --- | --- |
| Python | 3.11+ (tested on 3.13) |
| Node.js | 18+ |
| npm | 9+ |

Everything else (SQLite database, CSV demo data) is already included in the repo.

---

## 🚀 Quick Start

### 1. Clone & Bootstrap

```bash
# clone the repository
cd /path/to/workspace

# create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install backend dependencies
pip install -r backend/requirements.txt

# install frontend dependencies
cd frontend
npm install
cd ..
```

> **Tip:** The repo already contains a `.venv/` folder if you checked it out from the furnished workspace. Activate it with `source .venv/bin/activate` instead of creating a new one.

### 2. Run the stack

Open two terminals:

**Backend**
```bash
cd "/Volumes/2TB/Code/public repos/GTM Console"
source .venv/bin/activate
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**
```bash
cd "/Volumes/2TB/Code/public repos/GTM Console/frontend"
npm run dev
```

The UI is served at <http://localhost:3000>. The API lives at <http://localhost:8000>, with interactive docs in <http://localhost:8000/docs>.

### 3. Seeded demo data

The FastAPI app seeds the SQLite database automatically on startup using the CSV files in the repository root. You’ll see accounts, contacts, interactions, and insights immediately after the server boots—no manual migrations required.

---

## 🔐 Authentication

All protected endpoints expect a bearer token. For local testing use the bundled demo token:

```
Authorization: Bearer demo-token
```

The frontend is pre-configured to send this token, so you only need it when calling the API manually (e.g., with curl or Postman).

---

## 🧪 Validation & Smoke Tests

### Backend

```bash
# from repo root with virtualenv activated
python -m pytest backend/tests
```

You can also run a quick smoke check against the running API:

```python
import httpx

BASE_URL = "http://127.0.0.1:8000"
ENDPOINTS = [
    ("/health", {}),
    ("/accounts", {"headers": {"Authorization": "Bearer demo-token"}}),
    ("/dashboard/csm", {"headers": {"Authorization": "Bearer demo-token"}}),
    ("/accounts/1/rag", {"headers": {"Authorization": "Bearer demo-token"}, "params": {"query": "Renewal status"}}),
]

with httpx.Client(base_url=BASE_URL, timeout=5.0) as client:
    for path, options in ENDPOINTS:
        res = client.get(path, **options)
        print(path, res.status_code)
```

### Frontend

```bash
cd frontend
npm run lint
npm run build
```

---

## 📁 Project Structure

```
backend/
  app/
    api/            # FastAPI routers & dependencies
    core/           # Settings & configuration
    services/       # Insight engine & CSV seed loaders
    models.py       # SQLAlchemy ORM definitions
    schemas.py      # Pydantic response models
    main.py         # FastAPI entry point + lifespan seeding
  tests/
    test_api.py     # Integration smoke tests
frontend/
  app/              # Next.js routes
  components/       # Dashboard UI widgets
  lib/              # API client utilities & query hooks
  public/
```

---

## 🛠️ Troubleshooting

| Issue | Fix |
| --- | --- |
| `sqlite3.OperationalError` on startup | Remove `backend_data/journeylens.db` and restart the backend to regenerate tables. |
| API requests return 401 | Ensure the `Authorization: Bearer demo-token` header is present. |
| Frontend can’t reach API | Verify the backend is running on port 8000 and CORS isn’t blocked (default settings allow localhost). |
| Node build fails due to missing deps | Re-run `npm install` inside `frontend/` and retry `npm run build`. |

---

## 📌 Useful Commands

```bash
# format & lint backend (optional extras)
ruff format backend/app
ruff check backend/app

# tear down background servers
# (press Ctrl+C in the terminals running uvicorn / npm run dev)
```

---

## 📣 What’s Next?

- Replace the heuristic insight engine with real LLM calls, or wire it to your existing conversation datasets.
- Deploy the stack (Docker, Railway, Vercel) once you’re happy with local validation.
- Extend the dashboard with role-based access or additional analytics panels.

Enjoy exploring JourneyLens! 🚀
