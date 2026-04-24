# CorpTrack - Company Employee Records Management System

A web-based employee records management system built with Python (Flask) and SQLite.  
CorpTrack was developed in two versions to demonstrate a structured security improvement process:  
- **app.py** - intentionally insecure baseline (port 5000)  
- **app_secure.py** - hardened version with all security fixes applied (port 5001)

---

## Project Overview

CorpTrack allows a company to store, view, update, and delete employee records through a clean web interface. Access is controlled through two distinct user roles HR Admin and Employee enforced server-side through Flask session management.

The project follows the Secure Software Development Lifecycle (SSDLC) approach: a functional baseline was built first without security controls, a thorough security analysis was conducted, and targeted fixes were implemented and verified through testing.

---

## Features

### Functional Features
- User registration and login system
- Role-based access control — two distinct user roles with different privileges
- Full CRUD operations — Create, Read, Update, Delete employee records
- Employee search by name or department (Admin only)
- Secure logout with session clearing


## User Roles

| Role | Username | Privileges |
|------|----------|------------|
| HR Admin | admin | View all records, Add, Edit, Delete, Search |
| Employee | user | View and add own record only |



## Project Structure

```
corptrack/
│
├── app.py                    Vulnerable baseline — intentionally insecure (port 5000)
├── app_secure.py             Hardened secure version with all fixes applied (port 5001)
│
├── corptrack.db              SQLite database for app.py — plain-text passwords
├── corptrack_secure.db       SQLite database for app_secure.py — bcrypt hashed passwords
│
├── requirements.txt          Python dependencies: flask, bcrypt
├── README.md                 Project documentation (this file)
├── SECURITY.md               Vulnerability log and fix documentation
│
├── static/
│   └── css/
│       └── style.css         Shared stylesheet used by both versions
│
└── templates/
    ├── login.html            Login page
    ├── register.html         Registration page
    ├── dashboard.html        Employee records dashboard with search bar
    ├── add_employee.html     Add new employee form
    └── edit_employee.html    Edit existing employee record form
```

---

## Setup and Installation

### Prerequisites
- Python 3.x installed on your machine
- pip package manager

### Steps

1. Clone the repository:
```bash
git clone https://github.com/Sera-K/SWD.git
cd SWD
```

2. Install dependencies:
```bash
pip install flask bcrypt
```

3. Run the vulnerable baseline (for testing vulnerabilities):
```bash
python app.py
```
Open browser at: **http://127.0.0.1:5000**

4. Run the secure version (for testing fixes):
```bash
python app_secure.py
```
Open browser at: **http://127.0.0.1:5001**

---

## Default Login Credentials

| Username | Password  | Role     |
|----------|-----------|----------|
| admin    | admin123  | HR Admin |

Register a new account at `/register` to test the Employee role.

---

## Usage Guidelines

### As HR Admin
1. Login with `admin` / `admin123`
2. Dashboard shows all employee records
3. Use the search bar to filter by name or department
4. Click **+ Add Employee** to add a new record
5. Use **Edit** or **Delete** buttons on any record

### As Employee
1. Register a new account at `/register`
2. Login with your new credentials
3. Dashboard shows only your own record
4. Click **+ Add Employee** to add your details
5. No access to edit or delete other records

---

## Contributions and References

- Flask: https://flask.palletsprojects.com
- bcrypt: https://pypi.org/project/bcrypt
- Bandit SAST: https://bandit.readthedocs.io
- OWASP Top Ten (2021): https://owasp.org/www-project-top-ten/
- SQLite3 Python docs: https://docs.python.org/3/library/sqlite3.html
