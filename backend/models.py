from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ==================================================
# USER MODEL
# ==================================================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="member"
    )
    # admin or member


    # ==================================================
    # AUTH FEATURES
    # ==================================================

    is_verified = db.Column(
        db.Boolean,
        default=False
    )

    verification_code = db.Column(
        db.String(20),
        nullable=True
    )

    reset_token = db.Column(
        db.String(200),
        nullable=True
    )

    google_id = db.Column(
        db.String(200),
        nullable=True
    )


    # ==================================================
    # CREATED DATE
    # ==================================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # ==================================================
    # RELATIONSHIPS
    # ==================================================

    task_assignments = db.relationship(
        "TaskAssignment",
        backref="user",
        lazy=True,
        cascade="all, delete"
    )


    # ==================================================
    # STRING REPRESENTATION
    # ==================================================

    def __repr__(self):

        return f"<User {self.username}>"


# ==================================================
# PROJECT MODEL
# ==================================================

class Project(db.Model):

    __tablename__ = "projects"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    created_by = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # ==================================================
    # RELATIONSHIPS
    # ==================================================

    tasks = db.relationship(
        "Task",
        backref="project",
        lazy=True,
        cascade="all, delete"
    )


    # ==================================================
    # STRING REPRESENTATION
    # ==================================================

    def __repr__(self):

        return f"<Project {self.title}>"


# ==================================================
# TASK MODEL
# ==================================================

class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    due_date = db.Column(
        db.Date,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # ==================================================
    # FOREIGN KEYS
    # ==================================================

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=False
    )


    # ==================================================
    # RELATIONSHIPS
    # ==================================================

    assignments = db.relationship(
        "TaskAssignment",
        backref="task",
        lazy=True,
        cascade="all, delete"
    )


    # ==================================================
    # CUMULATIVE PROGRESS
    # ==================================================

    @property
    def cumulative_progress(self):

        if not self.assignments:
            return 0

        total = sum(
            assignment.progress
            for assignment in self.assignments
        )

        return int(
            total / len(self.assignments)
        )


    # ==================================================
    # OVERALL STATUS
    # ==================================================

    @property
    def overall_status(self):

        if not self.assignments:
            return "Pending"

        completed = all(
            assignment.status == "Completed"
            for assignment in self.assignments
        )

        in_progress = any(
            assignment.status == "In Progress"
            for assignment in self.assignments
        )

        if completed:
            return "Completed"

        if in_progress:
            return "In Progress"

        return "Pending"


    # ==================================================
    # STRING REPRESENTATION
    # ==================================================

    def __repr__(self):

        return f"<Task {self.title}>"


# ==================================================
# TASK ASSIGNMENT MODEL
# ==================================================

class TaskAssignment(db.Model):

    __tablename__ = "task_assignments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # ==================================================
    # FOREIGN KEYS
    # ==================================================

    task_id = db.Column(
        db.Integer,
        db.ForeignKey("tasks.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    # ==================================================
    # MEMBER TASK DATA
    # ==================================================

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    progress = db.Column(
        db.Integer,
        default=0
    )

    member_response = db.Column(
        db.Text,
        nullable=True
    )

    assigned_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # ==================================================
    # STRING REPRESENTATION
    # ==================================================

    def __repr__(self):

        return (
            f"<Assignment "
            f"Task:{self.task_id} "
            f"User:{self.user_id}>"
        )