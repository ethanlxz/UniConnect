<!-- Centered logo + project title -->
<p align="center">
    <img src="Frontend/image/uniconnect.png" alt="UniConnect logo" width="200" />
</p>

<h1 align="center">UniConnect 🎓</h1>

<p align="center"><strong>Easy Assignment Group Finder Platform for University Students</strong></p>
<p align="center"><strong>(Final Year Project for MMU Diploma in IT)</strong></p>

<p align="center">UniConnect is a university-focused group assignment and collaboration platform designed to simplify how students form teams and manage project work. It lets students explore rich peer profiles, create or join suitable groups, and coordinate tasks seamlessly. At the same time, lecturers gain powerful tools to create classes, oversee group progress, and manage assignments through an integrated, easy-to-use admin interface.</p>

## 1. Why this project? 🎯

Group projects are a core part of university education, yet forming the right team remains one of the most persistent challenges on campus. Students often don’t know their classmates well enough to understand their skills, commitment levels, or working styles—leading to unbalanced groups, miscommunication, and uneven contributions. Lecturers, on the other hand, struggle to manage group formation fairly and efficiently across large cohorts, especially in increasingly digital learning environments.

UniConnect directly tackles this university-wide issue. Through an interactive card-based profile system, students can explore their peers’ strengths and preferences before joining a group, making collaboration more informed and intentional. Lecturers receive a clearer, more organized view of all groups and assignments, turning a traditionally chaotic university pain point into a structured and transparent process.

## 2. Project Objectives ✅

1. Streamline University Group Formation<br>
Simplify and speed up how students form project teams by providing clear, accessible information about their classmates’ skills, interests, and working styles.

2. Enable Informed, Compatible Team Matching<br>
Help students make better collaboration decisions through interactive, profile-based exploration that reduces mismatches and improves group dynamics.

3. Enhance Transparency and Visibility<br>
Offer rich, structured student profiles— including photos, skills, major, and availability—so peers can understand each other before joining a group.

4. Empower Lecturers With Better Oversight<br>
Provide lecturers with an organized, real-time view of group compositions and assignment progress, ensuring fairer and more efficient class management.

5. Reduce Administrative Burden<br>
Minimize the manual effort required for lecturers to create, adjust, and monitor groups across large cohorts or multiple classes.

6. Improve the Overall Group Project Experience<br>
Transform group work from a stressful, chaotic process into a smoother, more collaborative, and more meaningful part of university learning.

## 3. Target Users 🎯

- University students who need to form or join project groups and collaborate on assignments.
- Lecturers and instructors who create classes, manage students and groups, and monitor progress.


## 4. Key Features ✨

- Student & lecturer registration, login (JWT based), and profile management
- OTP-based email verification for registration/login flows
- Class creation, join, edit, remove student, and class listing endpoints
- Manual or automatic group formation (skill and availability-based matching)
- Task and assignment management for collaborative work
- Admin panel for lecturer-class and student oversight
- REST API built with Django REST Framework; frontend is static HTML/CSS/JS

For more detailed API docs (endpoints and example payloads), see `Backend/README.md` which contains an extensive list of available endpoints and example responses.


## 5. Technology Stack 🔧

- Backend: Django 5, Django REST Framework, Simple JWT (JWT auth)
- Frontend: Static HTML, CSS, JavaScript (served from `Frontend/html` or via any static host)
- Database: SQLite (default)
- Extras: CORS headers, Pillow (image handling), email via SMTP (configurable)


## 6. Quick start (development) — Local (SQLite)

1. Clone the repository:

```bash
git clone https://github.com/ethanlxz/UniConnect.git
cd UniConnect/Backend
```

2. (Recommended) Use the provided virtual environment or create a new one:

```bash
# Use the provided venv (if you want):
source myvenv/bin/activate

# Or create a new virtualenv:
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/` by default.


## 7. Using the frontend (static files)

The frontend is static HTML files in `Frontend/html`. You can open `Frontend/html/index.html` directly in a browser, or serve the folder with a simple static server (recommended for API integration):

```bash
cd Frontend/html
# Python 3 built-in simple server (serves on port 8000 by default)
python -m http.server 5501
```

The project's `settings.py` allows CORS from `http://localhost:5501` for local frontend testing.



## 8. Database (SQLite — default)

By default, UniConnect uses SQLite (file-based) for development. The project `settings.py` is already configured to use SQLite and no additional database setup is necessary for local development. You can use the project with the setup steps in Section 6, and run migrations as usual:

```bash
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver
```

If you plan to deploy this project to production, configure a production-ready database in your deployment environment and set environment variables accordingly. For development, SQLite is used by default and no additional configuration is required.


## 9. Environment variables & security ⚠️

- Currently the project contains a `SECRET_KEY` and SMTP credentials in `settings.py`. **Do not keep secret keys or production credentials in source control.**
- For production, move secrets into environment variables or use `.env` with a library such as `django-environ`.

Suggested environment variables:

- SECRET_KEY
- DATABASE_URL or DB_NAME/DB_USER/DB_PASS
- EMAIL_HOST_USER and EMAIL_HOST_PASSWORD


## 10. Running tests

From the backend folder run:

```bash
python manage.py test
```

## 11. Backend API Endpoints — Summary 📡

This project exposes a REST API for managing users, classes, and groups. Below is a quick summary of the most commonly used backend endpoints grouped by feature — see `Backend/README.md` for full payloads and example responses.

Base URL (development): `http://127.0.0.1:8000/`

Authentication: Login endpoints return JWT tokens (Simple JWT). Include the token in requests requiring authentication using an `Authorization` header, e.g.:

```
Authorization: Bearer <access_token>
Content-Type: application/json
```

A short list of endpoints (read `Backend/README.md` for full details):

- OTP (email verification)
    - POST /api/otp/send/ — Send an OTP to an email
    - POST /api/otp/resend/ — Resend OTP
    - POST /api/otp/verify/ — Verify OTP code

- Student APIs
    - POST /api/student/register/ — Register a new student
    - POST /api/student/login/ — Student login (returns JWT tokens)
    - GET /api/student/profile/<username>/ — Get student profile
    - PATCH /api/student/profile/<username>/ — Update student profile

- Lecturer APIs
    - POST /api/lecturer/register/ — Register a new lecturer
    - POST /api/lecturer/login/ — Lecturer login (returns JWT tokens)
    - GET /api/lecturer/profile/<lecturer_id>/ — Get lecturer profile
    - PATCH /api/lecturer/profile/<lecturer_id>/ — Update lecturer profile

- Classing (class management)
    - POST /classing/create/ — Create a class
    - POST /classing/join/ — Join a class using class code
    - PUT /classing/edit/ — Edit class info
    - DELETE /classing/delete/ — Delete a class
    - POST /classing/removeStudent/ — Remove a student from a class
    - POST /classing/lecturer/classes/ — List classes created by lecturer
    - POST /classing/student/classes/ — List classes a student joined
    - GET /classing/detail/?class_id=ID — Get class details
    - POST /classing/leave/ — Student leaves a class
    - GET /classing/studentDetail/?class_code=CODE — Get class/student details by code

- Grouping (group formation & management)
    - POST /grouping/send/ — Send a group request to another student
    - POST /grouping/respond/ — Accept or decline a group request
    - GET /grouping/requests?username=USER&class_code=CODE — List incoming requests
    - GET /grouping/list/?class_id=ID — List groups (final and temporary) for a class
    - GET /grouping/myGroups/?username=USER — List groups the user belongs to
    - POST /grouping/leave/ — Leave a temporary group
    - POST /grouping/finalTG/ — Finalize a temporary group to make it final
    - POST /grouping/changeLeader/ — Change the leader of a temporary group
    - POST /grouping/definalTG/ — Definalize a temporary group
    - POST /grouping/api/convert-to-group/ — Convert to existing final group and delete temporary
    - POST /grouping/removeMember/ — Remove a member from a temp group
    - POST /grouping/sendJoinRequest/ — Request to join another group's temporary/final group
    - POST /grouping/respondJoinRequest/ — Leader responds to a join request
    - GET /grouping/joinRequests?leader_username=...&class_code=... — List join requests for a leader

For a complete list of endpoints (payloads, example requests/responses, and additional resources such as class/group detail endpoints), see `Backend/README.md` which contains extended API documentation.

---

## 12. More information 🤝
See `Backend/README.md` for more details on endpoints.
