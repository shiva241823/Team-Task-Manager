# Team Task Manager

Team Task Manager is a full-stack web application built using Flask and SQLite that helps teams manage projects, assign tasks, and track member progress through a role-based management system.

The application supports Admin and Member roles, multi-member task assignment, cumulative task progress tracking, email verification, and password recovery using SMTP.

---

# Features

## Authentication
- User registration and login
- Email verification using SMTP
- Forgot password and reset password functionality
- Secure password hashing using Werkzeug
- Session-based authentication

---

## Admin Features
- Create, edit, and delete projects
- Create and manage tasks
- Assign a single task to multiple members
- Add and manage team members
- Monitor member-wise task progress
- View cumulative task progress
- Track overdue, pending, and completed tasks
- View detailed member responses for tasks

---

## Member Features
- View assigned projects
- View assigned tasks
- Update task status and progress
- Submit task responses and updates
- Track completed task history

---

## Dashboard Features
- Total projects overview
- Task statistics
- Overdue task tracking
- Member progress monitoring
- Cumulative task completion percentage
- Role-based dashboard system

---

# Tech Stack

## Backend
- Flask
- Flask SQLAlchemy
- Flask Mail
- Werkzeug Security

---

## Frontend
- HTML
- CSS
- JavaScript

---

## Database
- SQLite

---

## Authentication & Security
- Session-based authentication
- SMTP Email Verification
- Password Reset via Email
- Password Hashing

---

# Project Structure

```text
TeamTaskManager/
│
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   ├── task_manager.db
│   └── venv/
│
├── frontend/
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── member_dashboard.html
│   ├── create_project.html
│   ├── create_task.html
│   ├── edit_project.html
│   ├── edit_task.html
│   ├── view_projects.html
│   ├── view_tasks.html
│   ├── manage_members.html
│   ├── member_update_task.html
│   ├── view_member_progress.html
│   ├── verify_email.html
│   ├── forgot_password.html
│   ├── reset_password.html
│   ├── style.css
│   └── script.js
│
└── README.md

# Installation and Setup

## 1. Clone the Repository

```bash
git clone <repository-link>
cd TeamTaskManager
cd backend
```

---

## 2. Create and Activate Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Required Dependencies

```bash
pip install flask flask-sqlalchemy flask-mail werkzeug
```

OR

```bash
pip install -r requirements.txt
```

---

## 4. Configure SMTP

Inside `app.py`, update:

```python
app.config["MAIL_USERNAME"] = "your_email@gmail.com"

app.config["MAIL_PASSWORD"] = "your_gmail_app_password"
```

Use a Gmail App Password instead of your normal Gmail password.

---

## 5. Delete Old Database (Only If Models Changed)

```text
backend/task_manager.db
```

---

## 6. Run the Application

```bash
python app.py
```

---

## 7. Open in Browser

```text
http://127.0.0.1:5000
```