from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "corptrack_secret"  # Used to manage login sessions

DB = "corptrack.db"

# ─── Database Setup ────────────────────────────────────────────────────────────

def get_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row  # Lets us access columns by name
    return conn

def init_db():
    """Create tables if they don't exist, and add a default admin."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role     TEXT   -- 'admin' or 'employee'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT,
            email       TEXT,
            department  TEXT,
            job_title   TEXT,
            phone       TEXT,
            date_joined TEXT,
            username    TEXT   -- links employee record to a user account
        )
    """)
    # Default admin account (no hashing — intentionally insecure)
    existing = conn.execute("SELECT * FROM users WHERE username='admin'").fetchone()
    if not existing:
        conn.execute("INSERT INTO users (username, password, role) VALUES ('admin','admin123','admin')")
    conn.commit()
    conn.close()

# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        # No prepared statements — intentionally vulnerable to SQL injection
        user = conn.execute(
            f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        ).fetchone()
        conn.close()
        if user:
            session["username"] = user["username"]
            session["role"]     = user["role"]
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, 'employee')",
            (username, password)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("login"))
    return render_template("register.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    if session["role"] == "admin":
        # Admin sees ALL employee records
        employees = conn.execute("SELECT * FROM employees").fetchall()
    else:
        # Employee sees only their own record
        employees = conn.execute(
            "SELECT * FROM employees WHERE username=?", (session["username"],)
        ).fetchall()
    conn.close()
    return render_template("dashboard.html", employees=employees)


@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        conn = get_db()
        conn.execute("""
            INSERT INTO employees (name, email, department, job_title, phone, date_joined, username)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form["name"],
            request.form["email"],
            request.form["department"],
            request.form["job_title"],
            request.form["phone"],
            request.form["date_joined"],
            session["username"]
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))
    return render_template("add_employee.html")


@app.route("/edit/<int:emp_id>", methods=["GET", "POST"])
def edit_employee(emp_id):
    if "username" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    employee = conn.execute("SELECT * FROM employees WHERE id=?", (emp_id,)).fetchone()
    if request.method == "POST":
        conn.execute("""
            UPDATE employees
            SET name=?, email=?, department=?, job_title=?, phone=?, date_joined=?
            WHERE id=?
        """, (
            request.form["name"],
            request.form["email"],
            request.form["department"],
            request.form["job_title"],
            request.form["phone"],
            request.form["date_joined"],
            emp_id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))
    conn.close()
    return render_template("edit_employee.html", employee=employee)


@app.route("/delete/<int:emp_id>")
def delete_employee(emp_id):
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("dashboard"))
    conn = get_db()
    conn.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ─── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
