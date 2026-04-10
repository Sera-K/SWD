# CorpTrack — Company Employee Records System

CorpTrack is a web-based employee records management system built with Python (Flask) and SQLite. It supports two user roles: HR Admin and Employee.

## Features
- Login and registration system
- HR Admin can Create, Read, Update and Delete all employee records
- Employees can only view and submit their own record
- Role-based access control enforced on every route

## Tech Stack
- Python 3 / Flask 3.0
- SQLite (built-in database)
- HTML5 / CSS3
- Jinja2 templating (built into Flask)

## Setup Instructions
1. Make sure Python 3 is installed
2. Install Flask: `pip install flask`
3. Run the app: `python app.py`
4. Open browser at: `http://127.0.0.1:5000`

## Default Admin Login
| Username | Password  |
|----------|-----------|
| admin    | admin123  |

## Known Security Vulnerabilities (Intentional)
1. SQL Injection on login form
2. Passwords stored as plain text
3. No input validation on any form field
4. Hardcoded Flask secret key
5. No CSRF protection on forms