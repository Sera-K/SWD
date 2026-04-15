from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os
import bcrypt
app = Flask(__name__)
app.secret_key = "corptrack_secret"  

DB = "corptrack.db"

def get_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row  
    return conn
def validate_input(value, field_name, max_length=100):
    if not value or value.strip() == "":
        return f"{field_name} cannot be empty."
    if len(value) > max_length:
        return f"{field_name} must be under {max_length} characters."
    return None

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
    existing = conn.execute("SELECT * FROM users WHERE username='admin'").fetchone()
    if not existing:
        hashed = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt())
conn.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, 'admin')",
    ("admin", hashed.decode("utf-8"))
)conn.commit()
    conn.close()

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
        
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username,password)
        ).fetchone() 
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
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
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        conn.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, 'employee')",
        (username, hashed.decode("utf-8"))
        )
        conn.commit()
        conn.close()
        return redirect(url_for("login"))
    return render_template("register.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    search = request.args.get("search", "")

    conn = get_db()
    if session["role"] == "admin":
        if search:
            employees = conn.execute(
                "SELECT * FROM employees WHERE name LIKE ? OR department LIKE ?",
                (f"%{search}%", f"%{search}%")
            ).fetchall()
        else:
            employees = conn.execute("SELECT * FROM employees").fetchall()
    else:
        employees = conn.execute(
            "SELECT * FROM employees WHERE username=?", (session["username"],)
        ).fetchall()
    conn.close()
    return render_template("dashboard.html", employees=employees, search=search)
@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
    name        = request.form["name"].strip()
    email       = request.form["email"].strip()
    department  = request.form["department"].strip()
    job_title   = request.form["job_title"].strip()
    phone       = request.form["phone"].strip()
    date_joined = request.form["date_joined"].strip()

    error = (
        validate_input(name, "Name") or
        validate_input(email, "Email") or
        validate_input(department, "Department") or
        validate_input(job_title, "Job title") or
        validate_input(phone, "Phone") or
        validate_input(date_joined, "Date joined")
    )

    if not error:
        conn = get_db()
        conn.execute("""
            INSERT INTO employees (name, email, department, job_title, phone, date_joined, username)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, 
            request.form["name"],
            request.form["email"],
            request.form["department"],
            request.form["job_title"],
            request.form["phone"],
            request.form["date_joined"],
            session["username"]
        )
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))
    return render_template("add_employee.html",error=error)

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

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
