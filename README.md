# TaskFlow — FastAPI Task Manager

A full-stack Task Manager with a FastAPI backend and a clean vanilla JS frontend.

## 🚀 Live Demo

> 🔗 [https://your-app.onrender.com](https://your-app.onrender.com) ← replace after deployment

- API Docs: `/docs`
- Health Check: `/health`

---

## 📁 Project Structure

```
task-manager/
├── backend/
│   ├── app/
│   │   ├── config.py          # App settings (pydantic-settings)
│   │   ├── database.py        # SQLAlchemy engine + session
│   │   ├── dependencies.py    # get_db, get_current_user
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── models/            # SQLAlchemy ORM models
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── routers/           # Route handlers
│   │   │   ├── auth.py
│   │   │   └── tasks.py
│   │   └── services/          # Business logic
│   │       ├── auth.py        # JWT, bcrypt
│   │       └── tasks.py       # CRUD operations
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   └── test_tasks.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── index.html             # Single-page vanilla JS UI
└── README.md
```

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` inside the `backend/` folder:

```bash
cp backend/.env.example backend/.env
```

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy DB URL | `sqlite:///./taskmanager.db` |
| `SECRET_KEY` | JWT signing secret | *(must change in prod)* |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifespan | `1440` (24h) |

---

## 🛠 Run Locally

### Prerequisites
- Python 3.11+
- pip

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Edit SECRET_KEY
uvicorn app.main:app --reload --port 8000
```

The app also serves the frontend at `http://localhost:8000/`.  
API docs: `http://localhost:8000/docs`

### Run Tests

```bash
cd backend
pytest tests/ -v
```

---

## 🐳 Docker

```bash
cd backend
docker build -t taskflow .
docker run -p 8000:8000 --env-file .env taskflow
```

---

## 🌐 Deploy to Render

1. Push the repo to GitHub (public)
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repo, set root directory to `backend/`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables in Render dashboard:
   - `SECRET_KEY` → a long random string
   - `DATABASE_URL` → `sqlite:///./taskmanager.db` (or Postgres URL)

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, returns JWT |

### Tasks (🔒 requires Bearer token)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/tasks/` | Create a task |
| GET | `/tasks/` | List tasks (paginated, filterable) |
| GET | `/tasks/{id}` | Get single task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

#### Query Params for `GET /tasks/`
- `?completed=true` — filter completed tasks
- `?completed=false` — filter pending tasks
- `?page=1&page_size=10` — pagination

---

## 🧪 Test Coverage

- User registration & duplicate checks
- Login with valid/invalid credentials
- Task CRUD (create, read, update, delete)
- Authorization — users can only access their own tasks
- Pagination correctness
- Completed filter

---

## ✅ Features

- [x] JWT Authentication (bcrypt password hashing)
- [x] Full task CRUD
- [x] User isolation (can't see others' tasks)
- [x] Pagination
- [x] Filter by `?completed=true/false`
- [x] pytest test suite
- [x] Dockerfile
- [x] Clean folder structure
- [x] Single-page frontend (no framework)
- [x] Swagger UI at `/docs`
