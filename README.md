
# P.A.C.E. (Pasig Alumni Career & Employability System)

[![Next.js](https://img.shields.io/badge/Next.js-16.1-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.2-blue?style=flat-square&logo=react)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?style=flat-square&logo=supabase)](https://supabase.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)

---

## 📖 Executive Summary

The **Pasig Alumni Career & Employability System (P.A.C.E.)** is an enterprise-grade platform engineered to bridge the gap between educational institutions and the professional workforce. By leveraging data-driven insights and seamless connectivity, PACE empowers alumni from Pasig City with curated career opportunities, while providing administrators with robust tools for employability tracking and analytics.

## 🏗️ System Architecture

The solution adheres to a modern, decoupled microservices-ready architecture, ensuring scalability, maintainability, and performance.

### Core Components

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | **Next.js 16** (React 19) | Server-side rendering, responsive UI, and client-side interactivity. |
| **Backend API** | **FastAPI** (Python 3.10+) | High-performance RESTful API services and data processing. |
| **Database** | **PostgreSQL** (via Supabase) | Relational data persistence, Row Level Security (RLS), and specialized extensions. |
| **Authentication** | **Supabase Auth** | Secure identity management and session handling. |
| **Infrastructure** | **Docker** | Containerization for consistent development and deployment environments. |

## ⚙️ Development Workflow

### Prerequisites

Ensure the following tools are installed and configured in your local environment:

-   **Node.js** (v20 LTS or higher)
-   **Python** (v3.10 or higher)
-   **Docker Desktop** (Latest Stable Release)
-   **Git** (Version Control)

### Installation & Configuration

#### 1. Repository Setup

```bash
git clone https://github.com/KlyrhonMiko/pace
cd pace
```

#### 2. Environment Variables

Configure the application by creating a `.env.local` file in the project root. Secure credentials will be provided by the DevOps lead.

| Variable | Description |
| :--- | :--- |
| `NEXT_PUBLIC_SUPABASE_URL` | API Endpoint for the Supabase instance. |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Public API key for client-side operations. |
| `SUPABASE_SERVICE_ROLE_KEY` | Private key for server-side administrative access. |

#### 3. Application Initialization

**Option A: Containerized Development (Recommended)**

Launch the full stack ensuring environment consistency.

```bash
docker-compose up --build
```

**Option B: Manual Service Execution**

*Frontend Service:*

```bash
npm install
npm run dev
# Access via http://localhost:3000
```

*Backend Service:*

```bash
cd backend
python -m venv venv
# Activate Virtual Environment (Windows: .\venv\Scripts\activate | Unix: source venv/bin/activate)
pip install -r requirements.txt
uvicorn main:app --reload
# Access via http://localhost:8000
```

## � Deployment Strategy

-   **Frontend**: Continuous Deployment (CD) pipeline configured via **Vercel**.
-   **Backend**: Containerized deployment on **Render** utilizing Docker registry.

## 🤝 Contribution Standards

To maintain code quality and project integrity, please adhere to the following contribution guidelines:

1.  **Branching Strategy**: Use feature branches (`feature/component-name`) derived from `main`.
2.  **Commit Convention**: Follow [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat: user authentication`, `fix: hydration error`).
3.  **Code Review**: All Pull Requests (PRs) require peer review and approval before merging.
4.  **Linting**: Ensure `npm run lint` passes without errors.
