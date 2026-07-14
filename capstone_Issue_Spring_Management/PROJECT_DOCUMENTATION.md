# Issue & Sprint Management System Documentation

## 1. Project Overview

The Issue & Sprint Management System is a full-stack web application for managing software projects, project members, issues, subtasks, comments, sprints, and dashboard metrics. It follows a simple agile workflow where administrators create and manage projects, members work on assigned project issues, and sprint boards help organize delivery.

The project is divided into two main applications:

- `backend`: REST API built with FastAPI and MongoDB.
- `frontend`: React application built with Vite, React Router, Axios, and modular CSS.

The backend exposes authentication, project, issue, sprint, comment, dashboard, and health endpoints. The frontend consumes those APIs and provides screens for login, registration, dashboard, project management, issue tracking, and sprint management.

## 2. Main Features

- User registration and login with JWT authentication.
- Role-based authorization for `ADMIN` and `MEMBER` users.
- Project creation, editing, soft deletion, and member assignment.
- Issue creation, search, filtering, assignment, subtasks, status updates, and soft deletion.
- Issue workflow validation with controlled status transitions.
- Comment creation, editing, listing, and soft deletion for issues.
- Sprint creation, issue assignment, sprint start, and sprint completion.
- Dashboard statistics for projects, issues, sprints, completion rate, and sprint progress.
- MongoDB persistence for production-like usage.
- In-memory database support for automated backend tests.

## 3. Technology Stack

### Backend

- Python
- FastAPI
- Pydantic
- MongoDB
- PyMongo
- python-dotenv
- python-jose
- bcrypt
- pytest
- FastAPI TestClient

### Frontend

- React 19
- Vite
- React Router DOM
- Axios
- React Hot Toast
- Tailwind CSS dependency present
- Modular CSS files
- Oxlint

## 4. Repository Structure

```text
capstone_Issue_Spring_Management/
  backend/
    app/
      api/                 API routers
      core/                configuration, security, roles, lifespan, logging
      database/            MongoDB and in-memory database setup
      dependencies/        authentication and role dependencies
      exceptions/          custom API exceptions and handlers
      repositories/        database access layer
      schemas/             Pydantic request and response schemas
      services/            business logic layer
      utils/               shared utility functions
      constants.py         validation limits
      main.py              FastAPI application entry point
    tests/                 backend pytest test suite
    package.json           contains a Node dependency for bson
  frontend/
    public/                static assets
    src/
      api/                 Axios instance
      assets/              React/Vite/hero assets
      components/          shared UI and feature components
      context/             auth context
      hooks/               custom hooks
      pages/               page-level route components
      routes/              route definitions
      services/            frontend API service wrappers
      style/               global styles
      App.jsx
      main.jsx
    package.json           frontend dependencies and scripts
    vite.config.js
```

## 5. Backend Architecture

The backend uses a layered structure:

```text
Router -> Service -> Repository -> Database
```

- Routers receive HTTP requests and declare authentication requirements.
- Services contain business rules, validations, permissions, and response construction.
- Repositories handle MongoDB queries and document serialization.
- Database modules configure either MongoDB or the test in-memory database.

### Application Entry Point

The FastAPI app is created in `backend/app/main.py` with the title `Issue & Sprint Management System` and version `1.0.0`.

Registered routers:

- `/health`
- `/auth`
- `/projects`
- `/issues`
- `/sprints`
- `/issues/{issue_id}/comments`
- `/comments/{comment_id}`
- `/dashboard`

CORS is currently configured with:

```python
allow_origins=["*"]
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

This is convenient for development, but production should use a restricted origin list.

## 6. Backend Configuration

Configuration is loaded from environment variables in `backend/app/core/config.py`.

| Variable | Default | Purpose |
|---|---:|---|
| `MONGO_URI` | empty string | MongoDB connection string |
| `DATABASE_NAME` | `issue_sprint_management` | MongoDB database name |
| `SECRET_KEY` | `change-this-secret` | JWT signing secret |
| `ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `180` | Access token lifetime |
| `USE_IN_MEMORY_DB` | not set | Set to `true` to force in-memory database |

Example `.env` for local backend development:

```env
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=issue_sprint_management
SECRET_KEY=replace-with-a-strong-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=180
```

## 7. Database Collections

The application uses these collections:

- `users`
- `projects`
- `issues`
- `sprints`
- `comments`

Most project, issue, sprint, and comment documents include audit fields:

```json
{
  "created_by": "admin@example.com",
  "updated_by": "admin@example.com",
  "created_at": "2026-07-14T00:00:00+00:00",
  "updated_at": "2026-07-14T00:00:00+00:00",
  "is_deleted": false
}
```

Soft deletion is used for projects, issues, and comments by setting `is_deleted` to `true`.

## 8. Authentication and Authorization

Authentication is handled through JWT bearer tokens. The frontend stores the token in `localStorage` under `authToken`, and stores the user under `currentUser`.

The Axios interceptor sends:

- `Authorization: Bearer <token>` when a token exists.
- `X-User-Email: <email>` for compatibility with tests and local calls.

The backend still supports `X-User-Email`, but the preferred authentication mechanism is the bearer token.

### Roles

The user schema accepts:

- `ADMIN`
- `MEMBER`
- `VIEWER`

The active authorization helpers are:

- `require_admin`: only allows `ADMIN`.
- `require_member`: allows `ADMIN` and `MEMBER`.

Although `VIEWER` exists in the schema and some service checks reference it, `require_member` blocks it from most routes. This means `VIEWER` is not currently usable through protected API routes.

### Password Rules

Registration passwords must:

- Be 8 to 30 characters.
- Not start or end with spaces.
- Include at least one uppercase letter.
- Include at least one lowercase letter.
- Include at least one number.
- Include at least one special character.

Passwords are hashed with `bcrypt` before storage.

## 9. Backend API Documentation

Base URL used by the frontend:

```text
http://localhost:8000
```

Interactive FastAPI docs are available when the backend is running:

```text
http://localhost:8000/docs
```

### Health

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/health` | No | Returns API running status |

Response:

```json
{
  "status": "Running",
  "message": "Issue & Sprint Management System API"
}
```

### Authentication

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | No | Register a user |
| `POST` | `/auth/login` | No | Login and receive JWT token |
| `GET` | `/auth/users?search=` | ADMIN or MEMBER | Search users with role `MEMBER` |

Register request:

```json
{
  "name": "Admin User",
  "email": "admin@example.com",
  "password": "Password@123",
  "role": "ADMIN"
}
```

Login request:

```json
{
  "email": "admin@example.com",
  "password": "Password@123"
}
```

Login response:

```json
{
  "message": "Login successful.",
  "access_token": "<jwt-token>",
  "token_type": "bearer",
  "user": {
    "name": "Admin User",
    "email": "admin@example.com",
    "role": "ADMIN"
  }
}
```

### Projects

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/projects` | ADMIN | Create project |
| `GET` | `/projects` | ADMIN only by service rule | Get all projects |
| `GET` | `/projects/{project_id}` | ADMIN or project member | Get project by ID |
| `PUT` | `/projects/{project_id}` | ADMIN | Update project |
| `DELETE` | `/projects/{project_id}` | ADMIN | Soft delete project |
| `POST` | `/projects/{project_id}/members` | ADMIN | Add member to project |
| `DELETE` | `/projects/{project_id}/members/{email}` | ADMIN | Remove member from project |
| `GET` | `/projects/assigned/me` | ADMIN or MEMBER | Get projects assigned to current user |

Create project request:

```json
{
  "name": "Issue Tracker",
  "description": "Project for managing internal product issues.",
  "project_key": "ISSUE",
  "members": [
    {
      "email": "member@example.com"
    }
  ]
}
```

Project validation:

- `name`: 3 to 50 characters.
- `description`: 5 to 500 characters.
- `project_key`: 2 to 10 characters, letters, numbers, and underscores only.
- `project_key` is normalized to uppercase.
- Member emails must belong to existing users.
- Duplicate project names, project keys, and member emails are rejected.

### Issues

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/issues` | ADMIN or MEMBER | Create issue |
| `GET` | `/issues` | ADMIN or MEMBER | Search/list issues |
| `GET` | `/issues/{issue_id}` | ADMIN or project member | Get issue by ID |
| `GET` | `/issues/project/{project_id}` | ADMIN or project member | Get project issues |
| `GET` | `/issues/assigned/me` | ADMIN or MEMBER | Get issues assigned to current user |
| `GET` | `/issues/{issue_id}/subtasks` | ADMIN or project member | Get subtasks |
| `PATCH` | `/issues/{issue_id}` | ADMIN, reporter, or assignee | Update editable issue fields |
| `PATCH` | `/issues/{issue_id}/status` | ADMIN or assignee | Update issue status |
| `DELETE` | `/issues/{issue_id}` | ADMIN or reporter | Soft delete issue |

Create issue request:

```json
{
  "title": "Login page validation error",
  "description": "The login form should show a validation message for empty password.",
  "project_id": "PROJECT_OBJECT_ID",
  "parent_id": null,
  "assignee_email": "member@example.com",
  "issue_type": "BUG",
  "priority": "High",
  "story_points": 3,
  "status": "TODO"
}
```

Issue validation:

- `title`: 3 to 100 characters.
- `description`: 5 to 1000 characters.
- `project_id`: required.
- `issue_type`: `TASK`, `BUG`, or `STORY`.
- `priority`: `Low`, `Medium`, or `High`.
- `story_points`: 0 to 100.
- `status`: `BACKLOG`, `TODO`, `IN_PROGRESS`, `REVIEW`, or `DONE`.
- Assignee must be a valid project member.
- Parent issue must exist and belong to the same project.

Issue keys are generated automatically as:

```text
<PROJECT_KEY>-<next-number>
```

Example:

```text
ISSUE-1
ISSUE-2
```

Search issue query parameters:

| Parameter | Description |
|---|---|
| `project_id` | Filter by project |
| `status` | Filter by issue status |
| `assignee` | Filter by assignee email |
| `search` | Case-insensitive search in title and description |
| `page` | Page number, default `1` |
| `limit` | Page size, default `10`, max `100` |
| `paginated` | When `true`, returns pagination metadata |

Paginated response shape:

```json
{
  "items": [],
  "page": 1,
  "limit": 10,
  "total": 0,
  "pages": 0
}
```

Editable issue fields:

- `title`
- `description`
- `assignee_email`
- `issue_type`
- `priority`
- `story_points`

Status transitions:

| Current Status | Allowed Next Status |
|---|---|
| `BACKLOG` | `TODO` |
| `TODO` | `IN_PROGRESS` |
| `IN_PROGRESS` | `REVIEW`, `TODO`, `DONE` |
| `REVIEW` | `DONE`, `IN_PROGRESS` |
| `DONE` | none |

### Sprints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/sprints` | ADMIN or project member | Create sprint |
| `GET` | `/sprints?project_id=` | ADMIN or project member | List sprints |
| `GET` | `/sprints/{sprint_id}` | ADMIN or project member | Get sprint |
| `POST` | `/sprints/{sprint_id}/issues` | ADMIN or project member | Add issue to sprint |
| `DELETE` | `/sprints/{sprint_id}/issues/{issue_id}` | ADMIN or project member | Remove issue from sprint |
| `PATCH` | `/sprints/{sprint_id}/start` | ADMIN or project member | Start sprint |
| `PATCH` | `/sprints/{sprint_id}/complete` | ADMIN or project member | Complete sprint |

Create sprint request:

```json
{
  "name": "Sprint 1",
  "project_id": "PROJECT_OBJECT_ID",
  "start_date": "2026-07-14",
  "end_date": "2026-07-28",
  "status": "planned"
}
```

Sprint validation and rules:

- `name`: 3 to 80 characters.
- `project_id`: required.
- `end_date` cannot be before `start_date`.
- `status`: `planned`, `active`, or `completed`.
- Issues can only be added if they belong to the sprint project.
- Completed issues cannot be added to a sprint.
- Issues cannot be added to a completed sprint.
- Only `planned` sprints can be started.
- Only `active` sprints can be completed.

Add issue request:

```json
{
  "issue_id": "ISSUE_OBJECT_ID"
}
```

### Comments

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/issues/{issue_id}/comments` | ADMIN or project member | Add comment |
| `GET` | `/issues/{issue_id}/comments` | ADMIN or project member | List issue comments |
| `PUT` | `/comments/{comment_id}` | ADMIN or comment author | Update comment |
| `DELETE` | `/comments/{comment_id}` | ADMIN or comment author | Soft delete comment |

Create or update comment request:

```json
{
  "body": "This issue is ready for review."
}
```

Comment validation:

- `body`: 1 to 1000 characters.
- Empty or whitespace-only comments are rejected.

### Dashboard

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/dashboard/stats` | ADMIN or MEMBER | Get dashboard metrics |

Response shape:

```json
{
  "projects": 2,
  "issues": 10,
  "open_issues": 7,
  "completed_issues": 3,
  "sprints": 4,
  "active_sprints": 1,
  "completed_sprints": 2,
  "sprint_progress": 50,
  "issue_completion": 30
}
```

For admins, stats include all non-deleted projects, issues, and sprints. For members, stats are scoped to projects where the current user is a member.

## 10. Error Handling

The backend maps custom exceptions to HTTP responses:

| Exception | Status Code |
|---|---:|
| `UnauthorizedException` | 401 |
| `ForbiddenException` | 403 |
| `NotFoundException` | 404 |
| `AlreadyExistsException` | 409 |
| `BadRequestException` | 400 |

Validation errors from Pydantic return `422 Unprocessable Entity`.

Typical error response:

```json
{
  "detail": "Project not found."
}
```

## 11. Frontend Architecture

The frontend is a Vite React application.

Important frontend modules:

- `src/api/axios.js`: configured Axios instance with API base URL and auth headers.
- `src/context/AuthContext.jsx`: stores login state, token, user, and logout logic.
- `src/routes/AppRoutes.jsx`: application routing.
- `src/services/*.js`: API wrapper classes.
- `src/pages/*`: page-level UI.
- `src/components/*`: reusable and feature-specific UI components.

### Frontend Routes

| Route | Component | Access |
|---|---|---|
| `/` | Redirects to `/dashboard` | Protected destination |
| `/login` | `Login` | Public |
| `/register` | `Register` | Public |
| `/dashboard` | `Dashboard` | Protected |
| `/projects` | `Projects` | Protected |
| `/issues` | `IssuesList` | Protected |
| `/sprints` | `SprintBoard` | Protected |

### Frontend Services

Authentication:

- `AuthService.register(registerData)`
- `AuthService.login(loginData)`
- `AuthService.searchMembers(search)`

Projects:

- `ProjectService.getProjects()`
- `ProjectService.getAssignedProjects()`
- `ProjectService.createProject(data)`
- `ProjectService.updateProject(id, data)`
- `ProjectService.deleteProject(id)`
- `ProjectService.addMember(projectId, email)`
- `ProjectService.removeMember(projectId, email)`

Issues and comments:

- `IssueService.getIssues(params)`
- `IssueService.createIssue(data)`
- `IssueService.updateIssue(issueId, data)`
- `IssueService.getSubtasks(issueId)`
- `IssueService.deleteIssue(issueId)`
- `IssueService.updateStatus(issueId, status)`
- `IssueService.getComments(issueId)`
- `IssueService.addComment(issueId, body)`
- `IssueService.updateComment(commentId, body)`
- `IssueService.deleteComment(commentId)`

Sprints:

- `SprintService.getSprints(projectId)`
- `SprintService.createSprint(data)`
- `SprintService.addIssue(sprintId, issueId)`
- `SprintService.removeIssue(sprintId, issueId)`
- `SprintService.startSprint(sprintId)`
- `SprintService.completeSprint(sprintId)`

Dashboard:

- `DashboardService.getStats()`

## 12. Local Setup Guide

### Prerequisites

- Python 3.10 or later recommended.
- Node.js and npm.
- MongoDB running locally or a MongoDB connection string.

### Backend Setup

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install backend Python dependencies. The repository currently does not include a `requirements.txt`, so install the dependencies used by imports:

```powershell
pip install fastapi uvicorn pymongo python-dotenv python-jose bcrypt pydantic email-validator pytest httpx
```

Create a `.env` file in `backend` or the working directory used to start the API:

```env
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=issue_sprint_management
SECRET_KEY=replace-with-a-strong-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=180
```

Start the backend:

```powershell
uvicorn app.main:application --reload --host 0.0.0.0 --port 8000
```

Open:

```text
http://localhost:8000/docs
```

### Frontend Setup

From the repository root:

```powershell
cd frontend
npm install
npm run dev
```

The Vite app usually runs at:

```text
http://localhost:5173
```

The frontend API base URL is hard-coded in `frontend/src/api/axios.js`:

```js
const baseurl = "http://localhost:8000";
```

If the backend runs elsewhere, update this value or move it to an environment variable such as `VITE_API_BASE_URL`.

## 13. Testing

Backend tests are stored in `backend/tests`.

The backend automatically uses an in-memory Mongo-like database when running under pytest, based on this condition in `backend/app/database/mongodb.py`:

```python
if "pytest" in sys.modules or os.getenv("USE_IN_MEMORY_DB") == "true":
    client = InMemoryClient()
    database = InMemoryDatabase()
```

Run tests from the backend directory:

```powershell
cd backend
pytest
```

Test coverage includes:

- Authentication and password hashing.
- Health endpoint.
- Project APIs and permissions.
- Issue APIs, validation, status transitions, and soft deletion.
- Sprint APIs and lifecycle behavior.
- Comment APIs and permissions.

Frontend linting:

```powershell
cd frontend
npm run lint
```

Frontend production build:

```powershell
cd frontend
npm run build
```

## 14. Business Rules Summary

### Project Rules

- Only admins can create, update, delete, and manage project members.
- Only admins can fetch the complete project list.
- Members can fetch projects assigned to them.
- Project names and project keys must be unique among non-deleted projects.
- Project members must be existing users.

### Issue Rules

- Admins and project members can create issues for a project.
- Assignees must be members of the issue project.
- Parent issues must belong to the same project.
- Members can only view issues in their projects or issues assigned to them.
- Only admins, reporters, or assignees can edit issue details.
- Only admins or assignees can update issue status.
- Only admins or reporters can delete issues.
- Status movement is limited by the configured transition table.

### Sprint Rules

- Admins and project members can create and access sprints for their projects.
- A sprint starts as `planned` by default.
- Only planned sprints can be started.
- Only active sprints can be completed.
- Completed sprints cannot receive new issues.
- Done issues cannot be added to sprints.
- Sprint issues must belong to the same project as the sprint.

### Comment Rules

- Admins and project members can read and create issue comments.
- Only admins or the comment author can update or delete a comment.
- Deleted comments are soft deleted.

## 15. Data Model Reference

### User

```json
{
  "_id": "ObjectId",
  "name": "Member User",
  "email": "member@example.com",
  "password": "bcrypt-hash",
  "role": "MEMBER"
}
```

### Project

```json
{
  "_id": "ObjectId",
  "name": "Issue Tracker",
  "description": "Project for managing internal product issues.",
  "project_key": "ISSUE",
  "members": [
    {
      "email": "member@example.com",
      "name": "Member User",
      "role": "MEMBER"
    }
  ],
  "created_by": "admin@example.com",
  "updated_by": "admin@example.com",
  "created_at": "datetime",
  "updated_at": "datetime",
  "is_deleted": false
}
```

### Issue

```json
{
  "_id": "ObjectId",
  "issue_key": "ISSUE-1",
  "title": "Login page validation error",
  "description": "The login form should show a validation message.",
  "project_id": "PROJECT_OBJECT_ID",
  "parent_id": null,
  "reporter_email": "admin@example.com",
  "assignee_email": "member@example.com",
  "issue_type": "BUG",
  "status": "TODO",
  "priority": "High",
  "story_points": 3,
  "created_by": "admin@example.com",
  "updated_by": "admin@example.com",
  "created_at": "datetime",
  "updated_at": "datetime",
  "is_deleted": false
}
```

### Sprint

```json
{
  "_id": "ObjectId",
  "name": "Sprint 1",
  "project_id": "PROJECT_OBJECT_ID",
  "start_date": "2026-07-14",
  "end_date": "2026-07-28",
  "status": "planned",
  "issue_ids": [
    "ISSUE_OBJECT_ID"
  ],
  "created_by": "admin@example.com",
  "updated_by": "admin@example.com",
  "created_at": "datetime",
  "updated_at": "datetime",
  "is_deleted": false
}
```

### Comment

```json
{
  "_id": "ObjectId",
  "issue_id": "ISSUE_OBJECT_ID",
  "body": "This issue is ready for review.",
  "author_email": "member@example.com",
  "created_by": "member@example.com",
  "updated_by": "member@example.com",
  "created_at": "datetime",
  "updated_at": "datetime",
  "is_deleted": false
}
```

## 16. Suggested User Flow

1. Register an admin user.
2. Register one or more member users.
3. Login as admin.
4. Create a project and assign members.
5. Create issues for the project.
6. Assign issues to members.
7. Create a sprint for the project.
8. Add project issues to the sprint.
9. Start the sprint.
10. Move issues through the allowed workflow.
11. Add comments during collaboration.
12. Complete the sprint.
13. Review dashboard statistics.

## 17. Known Gaps and Improvement Opportunities

- Add a backend `requirements.txt` or `pyproject.toml` so Python dependencies are reproducible.
- Move the frontend API base URL to a Vite environment variable.
- Restrict CORS origins before deployment.
- Replace default `SECRET_KEY` with a required secure production value.
- Clarify or remove the `VIEWER` role because protected route dependencies currently block it.
- Add indexes in MongoDB for frequently queried fields such as `email`, `project_key`, `project_id`, `assignee_email`, and `status`.
- Consider cascading behavior when deleting projects, such as handling related issues, sprints, and comments.
- Add frontend automated tests for protected routing, forms, and service integrations.
- Add API response models consistently across routers.
- Normalize route ordering for paths like `/issues/assigned/me` and `/issues/{issue_id}` to avoid path conflicts in future changes.

## 18. Quick Command Reference

Backend:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:application --reload --host 0.0.0.0 --port 8000
pytest
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
npm run lint
npm run build
```

Useful URLs:

```text
Backend API: http://localhost:8000
Swagger docs: http://localhost:8000/docs
Frontend app: http://localhost:5173
```
