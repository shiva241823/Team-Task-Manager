from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os
import random

from flask_mail import Mail, Message

from models import (
    db,
    User,
    Project,
    Task,
    TaskAssignment
)

# ==================================================
# FLASK CONFIG
# ==================================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
   )
app.secret_key = "secretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "sqlite:///" + os.path.join(BASE_DIR, "task_manager.db")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ==================================================
# SMTP CONFIG
# ==================================================

app.config["MAIL_SERVER"] = "smtp.gmail.com"

app.config["MAIL_PORT"] = 587

app.config["MAIL_USE_TLS"] = True

app.config["MAIL_USERNAME"] = \
"mycomplainto2025@gmail.com"

app.config["MAIL_PASSWORD"] = \
"nfar ipjd fvxp bnwa"

mail = Mail(app)

# ==================================================
# CREATE DATABASE + DEFAULT ADMIN
# ==================================================

with app.app_context():

    db.create_all()

    admin = User.query.filter_by(
        username="admin"
    ).first()

    if not admin:

        admin_user = User(
    full_name="System Admin",
    username="admin",
    email="admin@gmail.com",
    age=25,
    password=generate_password_hash("admin123"),
    role="admin",
    is_verified=True
)

        db.session.add(admin_user)

        db.session.commit()

        print("Default admin created successfully!")

# ==================================================
# LOGIN ROUTE
# ==================================================

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()


        # =========================
        # USER NOT FOUND
        # =========================

        if not user:

            return "Invalid username or password"


        # =========================
        # EMAIL NOT VERIFIED
        # =========================

        if not user.is_verified:

            return "Please verify your email first"


        # =========================
        # PASSWORD CHECK
        # =========================

        if check_password_hash(
            user.password,
            password
        ):

            session["user_id"] = user.id

            session["username"] = user.username

            session["role"] = user.role

            if user.role == "admin":

                return redirect("/admin")

            return redirect("/member")

        return "Invalid username or password"

    return render_template("login.html")


# ==================================================
# REGISTER ROUTE
# ==================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]

        username = request.form["username"]

        email = request.form["email"]

        age = request.form["age"]

        password = request.form["password"]


        # =========================
        # EXISTING USER CHECK
        # =========================

        existing_username = User.query.filter_by(
            username=username
        ).first()

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_username:

            return "Username already exists"

        if existing_email:

            return "Email already exists"


        # =========================
        # CREATE USER
        # =========================

        new_user = User(

            full_name=full_name,

            username=username,

            email=email,

            age=age,

            password=generate_password_hash(
                password
            ),

            role="member",

            is_verified=True,

            verification_code=None

        )

        db.session.add(new_user)

        db.session.commit()


        # =========================
        # REDIRECT TO LOGIN
        # =========================

        return redirect("/login")

    return render_template("register.html")

# ==================================================
# FORGOT PASSWORD
# ==================================================

@app.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            return "Email not found"


        # =========================
        # GENERATE RESET TOKEN
        # =========================

        token = str(
            random.randint(100000, 999999)
        )

        user.reset_token = token

        db.session.commit()


        # =========================
        # SEND MAIL
        # =========================

        msg = Message(

            "Reset Password",

            sender=app.config[
                "MAIL_USERNAME"
            ],

            recipients=[email]

        )

        msg.body = f"""
Hello {user.full_name},

Your password reset code is:

{token}

Use this code to reset your password.
"""

        mail.send(msg)

        return redirect(
            f"/reset-password/{user.id}"
        )

    return render_template(
        "forgot_password.html"
    )


# ==================================================
# RESET PASSWORD
# ==================================================

@app.route(
    "/reset-password/<int:user_id>",
    methods=["GET", "POST"]
)
def reset_password(user_id):

    user = User.query.get_or_404(
        user_id
    )

    if request.method == "POST":

        token = request.form["token"]

        new_password = request.form[
            "password"
        ]


        # =========================
        # INVALID TOKEN
        # =========================

        if token != user.reset_token:

            return "Invalid reset code"


        # =========================
        # UPDATE PASSWORD
        # =========================

        user.password = generate_password_hash(
            new_password
        )

        user.reset_token = None

        db.session.commit()

        return redirect("/login")

    return render_template(
        "reset_password.html",
        user=user
    )


# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# ==================================================
# ADMIN DASHBOARD
# ==================================================

@app.route("/admin")
def admin_dashboard():

    if session.get("role") != "admin":
        return redirect("/login")

    total_projects = Project.query.count()

    total_tasks = Task.query.count()

    completed_tasks = 0

    pending_tasks = 0

    overdue_tasks = 0

    all_tasks = Task.query.all()

    for task in all_tasks:

        if task.overall_status == "Completed":
            completed_tasks += 1

        if task.overall_status == "Pending":
            pending_tasks += 1

        if (
            task.due_date < date.today()
            and task.overall_status != "Completed"
        ):
            overdue_tasks += 1

    members = User.query.filter_by(
        role="member"
    ).all()

    projects = Project.query.all()

    return render_template(
        "admin_dashboard.html",

        total_projects=total_projects,

        total_tasks=total_tasks,

        completed_tasks=completed_tasks,

        pending_tasks=pending_tasks,

        overdue_tasks=overdue_tasks,

        members=members,

        projects=projects,

        all_tasks=all_tasks
    )

# ==================================================
# MEMBER DASHBOARD
# ==================================================

@app.route("/member")
def member_dashboard():

    if session.get("role") != "member":
        return redirect("/login")

    user_id = session.get("user_id")

    new_tasks = TaskAssignment.query.filter(
        TaskAssignment.user_id == user_id,
        TaskAssignment.status != "Completed"
    ).all()

    old_tasks = TaskAssignment.query.filter(
        TaskAssignment.user_id == user_id,
        TaskAssignment.status == "Completed"
    ).all()

    return render_template(
        "member_dashboard.html",
        new_tasks=new_tasks,
        old_tasks=old_tasks
    )

# ==================================================
# CREATE MEMBER
# ==================================================

@app.route("/create-member", methods=["GET", "POST"])
def create_member():

    if session.get("role") != "admin":
        return redirect("/login")

    members = User.query.filter_by(
        role="member"
    ).all()

    if request.method == "POST":

        full_name = request.form["full_name"]

        username = request.form["username"]

        email = request.form["email"]

        age = request.form["age"]

        password = request.form["password"]

        existing_username = User.query.filter_by(
            username=username
        ).first()

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_username:
            return "Username already exists"

        if existing_email:
            return "Email already exists"

        new_member = User(
            full_name=full_name,
            username=username,
            email=email,
            age=age,
            password=generate_password_hash(password),
            role="member",
            is_verified=True
        )

        db.session.add(new_member)

        db.session.commit()

        return redirect("/create-member")

    return render_template(
        "manage_members.html",
        members=members
    )

# ==================================================
# CREATE PROJECT
# ==================================================

@app.route("/create-project", methods=["GET", "POST"])
def create_project():

    if session.get("role") != "admin":
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]

        description = request.form["description"]

        project = Project(
            title=title,
            description=description,
            created_by=session.get("username")
        )

        db.session.add(project)

        db.session.commit()

        return redirect("/view-projects")

    return render_template("create_project.html")

# ==================================================
# VIEW PROJECTS
# ==================================================

@app.route("/view-projects")
def view_projects():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") == "admin":

        projects = Project.query.all()

    else:

        user_id = session.get("user_id")

        assignments = TaskAssignment.query.filter_by(
            user_id=user_id
        ).all()

        project_ids = []

        for assignment in assignments:

            if assignment.task.project_id not in project_ids:

                project_ids.append(
                    assignment.task.project_id
                )

        projects = Project.query.filter(
            Project.id.in_(project_ids)
        ).all()

    return render_template(
        "view_projects.html",
        projects=projects
    )

# ==================================================
# EDIT PROJECT
# ==================================================

@app.route("/edit-project/<int:id>", methods=["GET", "POST"])
def edit_project(id):

    if session.get("role") != "admin":
        return redirect("/login")

    project = Project.query.get_or_404(id)

    if request.method == "POST":

        project.title = request.form["title"]

        project.description = request.form["description"]

        db.session.commit()

        return redirect("/view-projects")

    return render_template(
        "edit_project.html",
        project=project
    )

# ==================================================
# CREATE TASK
# ==================================================

@app.route("/create-task", methods=["GET", "POST"])
def create_task():

    if session.get("role") != "admin":
        return redirect("/login")

    projects = Project.query.all()

    members = User.query.filter_by(
        role="member"
    ).all()

    if request.method == "POST":

        title = request.form["title"]

        description = request.form["description"]

        due_date = datetime.strptime(
            request.form["due_date"],
            "%Y-%m-%d"
        ).date()

        project_id = request.form["project_id"]

        assigned_members = request.form.getlist(
            "assigned_to"
        )

        # CREATE TASK

        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            project_id=project_id
        )

        db.session.add(task)

        db.session.commit()

        # MULTIPLE MEMBER ASSIGNMENT

        for member_id in assigned_members:

            assignment = TaskAssignment(
                task_id=task.id,
                user_id=member_id
            )

            db.session.add(assignment)

        db.session.commit()

        return redirect("/admin")

    return render_template(
        "create_task.html",
        projects=projects,
        members=members
    )

# ==================================================
# VIEW TASKS OF PROJECT
# ==================================================

@app.route("/view-tasks/<int:project_id>")
def view_tasks(project_id):

    if "user_id" not in session:
        return redirect("/login")

    project = Project.query.get_or_404(
        project_id
    )

    if session.get("role") == "admin":

        tasks = Task.query.filter_by(
            project_id=project_id
        ).all()

    else:

        user_id = session.get("user_id")

        tasks = []

        assignments = TaskAssignment.query.filter_by(
            user_id=user_id
        ).all()

        for assignment in assignments:

            if assignment.task.project_id == project_id:

                tasks.append(assignment.task)

        if not tasks:
            return redirect("/member")

    return render_template(
        "view_tasks.html",
        project=project,
        tasks=tasks
    )

# ==================================================
# EDIT TASK
# ==================================================

@app.route("/edit-task/<int:id>", methods=["GET", "POST"])
def edit_task(id):

    if session.get("role") != "admin":
        return redirect("/login")

    task = Task.query.get_or_404(id)

    projects = Project.query.all()

    members = User.query.filter_by(
        role="member"
    ).all()

    if request.method == "POST":

        # =========================
        # UPDATE TASK DETAILS
        # =========================

        task.title = request.form["title"]

        task.description = request.form[
            "description"
        ]

        task.project_id = request.form[
            "project_id"
        ]

        task.due_date = datetime.strptime(
            request.form["due_date"],
            "%Y-%m-%d"
        ).date()


        # =========================
        # GET SELECTED MEMBERS
        # =========================

        selected_members = request.form.getlist(
            "assigned_members"
        )

        selected_members = [
            int(member_id)
            for member_id in selected_members
        ]


        # =========================
        # CURRENT ASSIGNMENTS
        # =========================

        current_assignments = task.assignments

        current_member_ids = [
            assignment.user_id
            for assignment in current_assignments
        ]


        # =========================
        # REMOVE UNSELECTED MEMBERS
        # =========================

        for assignment in current_assignments:

            if assignment.user_id not in selected_members:

                db.session.delete(assignment)


        # =========================
        # ADD NEW MEMBERS
        # =========================

        for member_id in selected_members:

            if member_id not in current_member_ids:

                new_assignment = TaskAssignment(

                    task_id=task.id,

                    user_id=member_id,

                    status="Pending",

                    progress=0,

                    member_response=""

                )

                db.session.add(new_assignment)


        # =========================
        # SAVE CHANGES
        # =========================

        db.session.commit()

        return redirect(
            f"/view-tasks/{task.project_id}"
        )

    return render_template(

        "edit_task.html",

        task=task,

        projects=projects,

        members=members

    )
# ==================================================
# UPDATE TASK BY MEMBER
# ==================================================

@app.route("/update-task/<int:id>", methods=["GET", "POST"])
def update_task(id):

    if session.get("role") != "member":
        return redirect("/login")


    # =========================
    # GET ASSIGNMENT
    # =========================

    assignment = TaskAssignment.query.filter_by(
        id=id,
        user_id=session.get("user_id")
    ).first_or_404()


    # =========================
    # UPDATE TASK
    # =========================

    if request.method == "POST":

        assignment.status = request.form["status"]

        assignment.progress = int(
            request.form["progress"]
        )

        assignment.member_response = request.form[
            "member_response"
        ]


        # AUTO STATUS UPDATE

        if assignment.progress == 100:

            assignment.status = "Completed"

        elif assignment.progress > 0:

            assignment.status = "In Progress"

        else:

            assignment.status = "Pending"


        db.session.commit()

        return redirect("/member")


    # =========================
    # RENDER PAGE
    # =========================

    return render_template(
        "member_update_task.html",
        assignment=assignment
    )

# ==================================================
# DELETE PROJECT
# ==================================================

@app.route("/delete-project/<int:id>")
def delete_project(id):

    if session.get("role") != "admin":
        return redirect("/login")

    project = Project.query.get_or_404(id)

    db.session.delete(project)

    db.session.commit()

    return redirect("/view-projects")

# ==================================================
# DELETE TASK
# ==================================================

@app.route("/delete-task/<int:id>")
def delete_task(id):

    if session.get("role") != "admin":
        return redirect("/login")

    task = Task.query.get_or_404(id)

    db.session.delete(task)

    db.session.commit()

    return redirect("/view-projects")

# ==================================================
# VIEW MEMBER PROGRESS - TASK LIST
# ==================================================

@app.route("/member-progress")
def member_progress():

    if session.get("role") != "admin":
        return redirect("/login")

    tasks = Task.query.all()

    return render_template(
        "member_progress.html",
        tasks=tasks
    )


# ==================================================
# VIEW TASK MEMBER DETAILS
# ==================================================

@app.route("/task-progress/<int:task_id>")
def task_progress(task_id):

    if session.get("role") != "admin":
        return redirect("/login")

    task = Task.query.get_or_404(task_id)

    assignments = TaskAssignment.query.filter_by(
        task_id=task.id
    ).all()

    return render_template(
        "task_progress.html",
        task=task,
        assignments=assignments
    )

# ==================================================
# RUN APP
# ==================================================

if __name__ == "__main__":

    app.run(debug=True)