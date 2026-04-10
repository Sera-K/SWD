# CorpTrack — Company Employee Records System

A simple web application for managing company employee records.
Built with Python (Flask) and SQLite. Intentionally insecure for educational/security analysis purposes.

---

## Project Structure

```
corptrack/
│
├── app.py                  # Main Flask application (all routes and logic)
├── corptrack.db            # SQLite database (auto-created on first run)
├── requirements.txt        # Python dependencies
│
├── static/
│   └── css/
│       └── style.css       # All styling
│
└── templates/
    ├── login.html          # Login page
    ├── register.html       # Register page
    ├── dashboard.html      # View all employee records
    ├── add_employee.html   # Add a new employee
    └── edit_employee.html  # Edit an existing employee
```

---

## Setup & Run

1. Make sure Python is installed on your machine.

2. Install Flask:
   ```
   pip install flask
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

---

## Default Admin Login

| Username | Password  |
|----------|-----------|
| admin    | admin123  |

---

## User Roles

| Role     | Can Do                                      |
|----------|---------------------------------------------|
| Admin    | View ALL records, Add, Edit, Delete         |
| Employee | Add their own record, View their own record |

---

## Known Security Vulnerabilities (Intentional)

These are left in on purpose for the security assignment:

1. **SQL Injection** — The login query uses raw string formatting, making it vulnerable.
2. **No password hashing** — Passwords are stored as plain text in the database.
3. **No input validation** — Any data can be submitted in any field.
4. **Weak secret key** — The Flask session secret key is hardcoded and simple.
5. **No CSRF protection** — Forms have no cross-site request forgery tokens.
