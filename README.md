# Student Portal

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.1.3-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0.52-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Tailwind_CSS-CDN-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

<p align="center">
  A full-stack web application for managing student records — built with <strong>Flask</strong>, <strong>SQLAlchemy</strong>, and a dark-themed UI powered by <strong>Tailwind CSS</strong>.<br>
  Features two-factor authentication via email OTP, full CRUD operations, real-time analytics, and automated email notifications.
</p>

---

## Features

| Feature | Description |
|---|---|
| Secure Authentication | Email + password login protected by a 6-digit OTP sent to the user's inbox |
| User Accounts | Register, login, view profile, and change password via OTP verification |
| Student CRUD | Add, view, edit, and delete student records |
| Search & Pagination | Full-text search across name and email with server-side pagination (5 per page) |
| Analytics Dashboard | Live course-wise student distribution chart powered by ApexCharts |
| Email Notifications | Automated HTML welcome email sent to every newly enrolled student |
| Forgot Password | OTP-based, self-service password reset flow |
| Responsive UI | Mobile-friendly collapsible navbar with a consistent dark theme |

---

## Tech Stack

**Backend**
- [Python 3.14](https://www.python.org/) + [Flask 3.1.3](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy 3.1.1](https://flask-sqlalchemy.palletsprojects.com/) — ORM with SQLite
- [Flask-Login 0.6.3](https://flask-login.readthedocs.io/) — session-based authentication
- [Werkzeug 3.1.8](https://werkzeug.palletsprojects.com/) — password hashing (PBKDF2-SHA256)
- [python-dotenv 1.2.3](https://pypi.org/project/python-dotenv/) — environment variable management
- `smtplib` / `email.mime` — SMTP email via Gmail (STARTTLS, port 587)
- `threading.Thread` — non-blocking background email dispatch

**Frontend**
- [Jinja2 3.1.6](https://jinja.palletsprojects.com/) — server-side HTML templating
- [Tailwind CSS](https://tailwindcss.com/) (CDN) — utility-first dark UI
- [ApexCharts](https://apexcharts.com/) (CDN) — interactive analytics line chart
- Custom CSS (`static/css/styles.css`) — fade-in animations and navbar overrides

**Database**
- [SQLite](https://www.sqlite.org/) — file-based, zero-config (`instance/student_portal.db`)

---

## Project Structure

```
Student Portal/
│
├── app.py                   # Main Flask application — routes, models, email logic
├── create_db.py             # One-time script to initialise the database
├── populated_student.py     # Seed script — bulk-inserts fake students via Faker
├── .env                     # Environment variables (email credentials) — NOT committed
│
├── templates/
│   ├── layout.html          # Base template: navbar, flash messages, Tailwind CDN
│   ├── home.html            # Public landing page with feature highlights
│   ├── login.html           # Login form
│   ├── register.html        # User registration form
│   ├── verify_otp.html      # OTP entry page (login and password reset)
│   ├── forget_password.html # Forgot password — email entry
│   ├── reset_password.html  # New password form (post-OTP verification)
│   ├── dashboard.html       # Analytics dashboard with ApexCharts
│   ├── profile.html         # Authenticated user profile
│   ├── add_student.html     # Add new student form
│   ├── view_student.html    # Paginated, searchable student list
│   ├── edit_student.html    # Edit student record form
│   ├── student.html         # Individual student detail view
│   └── email_temp.html      # HTML template for welcome emails
│
├── static/
│   └── css/
│       └── styles.css       # Custom CSS — global styles, navbar, animations
│
└── instance/
    └── student_portal.db    # SQLite database file (auto-created)
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A Gmail account with an [App Password](https://support.google.com/accounts/answer/185833) configured (requires Gmail 2-Step Verification)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/student-portal.git
cd student-portal
```

### 2. Create and Activate a Virtual Environment

```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask flask-sqlalchemy flask-login werkzeug python-dotenv faker
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
EMAIL_USER=your_gmail_address@gmail.com
EMAIL_PASS=your_gmail_app_password
```

> **Important:** Use a Gmail App Password, not your regular account password. Add `.env` to `.gitignore` and never commit it to version control.

### 5. Initialise the Database

```bash
python create_db.py
```

Creates `instance/student_portal.db` with the `User` and `Student` tables.

### 6. (Optional) Seed with Sample Data

```bash
python populated_student.py
```

Inserts 1,000 randomly generated students across the following courses: `AI`, `CSE`, `ECE`, `MECH`, `CIVIL`, `EEE`, `DS`.

### 7. Run the Development Server

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## Authentication Flow

**Login with OTP**
```
Register --> Login (email + password)
                  |
                  | credentials valid
                  v
         OTP dispatched to email (background thread)
                  |
                  | OTP entered correctly
                  v
         Authenticated --> Dashboard
```

**Password Reset**
```
Forgot Password --> Enter registered email
                        |
                        | account found
                        v
                 OTP dispatched to email
                        |
                        | OTP verified
                        v
                 Set new password --> Login
```

---

## Application Routes

| Method | Route | Auth Required | Description |
|--------|-------|:---:|-------------|
| GET | `/` | No | Public landing page |
| GET / POST | `/register` | No | Create a new user account |
| GET / POST | `/login` | No | Email and password login |
| GET / POST | `/verify_otp` | No | 6-digit OTP verification |
| GET | `/logout` | Yes | Log out the current user |
| GET | `/dashboard` | Yes | Analytics dashboard |
| GET | `/profile/` | Yes | User profile page |
| GET | `/request_change_password` | Yes | Trigger OTP to change password |
| GET / POST | `/forget_password` | No | Forgot password — enter email |
| GET / POST | `/reset_password` | No | Set new password after OTP |
| GET / POST | `/add_students` | Yes | Add a new student record |
| GET | `/view_students` | No | Paginated and searchable student list |
| GET / POST | `/edit/<int:id>` | Yes | Edit an existing student record |
| GET / POST | `/delete/<int:id>` | Yes | Delete a student record |
| GET | `/student/<int:id>` | No | Individual student detail view |

---

## Database Models

### `User`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key | Auto-increment identifier |
| `username` | String(50) | NOT NULL | Display name |
| `email` | String(50) | NOT NULL | Login email address |
| `password_hash` | String(200) | NOT NULL | PBKDF2-SHA256 hashed password |

### `Student`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key | Auto-increment identifier |
| `name` | String(50) | NOT NULL | Full name |
| `email` | String(50) | NOT NULL | Contact email address |
| `course` | String(50) | NOT NULL | Enrolled course (AI, CSE, etc.) |
| `year` | String(5) | NOT NULL | Academic year (I – IV) |

---

## Email System

Two automated emails are sent via Gmail SMTP with STARTTLS on port 587:

1. **OTP Verification** — A 6-digit one-time password is generated with `random.randint` and dispatched in a background thread (`threading.Thread`) so the HTTP response is not blocked. Used for both login and password reset.

2. **Student Welcome Email** — An HTML-formatted email (`templates/email_temp.html`) is sent when a new student is added. The student's name and enrolled course are substituted at send time.

Both email functions read credentials from `.env` via `python-dotenv`.

---

## Security Considerations

The following areas should be addressed before any production deployment:

- **Secret key** — Replace the hardcoded `'supersecretkey123'` in `app.py` with a cryptographically strong value loaded from `.env`.
- **OTP expiry** — OTPs are stored in the session with no time-based expiry. Implement a TTL (e.g., 5 minutes using `session['otp_expires']`).
- **HTTPS** — Deploy behind a reverse proxy (Nginx or Caddy) with a valid TLS certificate.
- **Input validation** — Add server-side validation and sanitisation on all form fields using a library such as WTForms.
- **Email enumeration** — The forgot-password endpoint reveals whether an email is registered. Use a uniform response regardless of outcome.
- **Rate limiting** — Add [Flask-Limiter](https://flask-limiter.readthedocs.io/) to the login and OTP endpoints to mitigate brute-force attacks.
- **`.gitignore`** — Ensure `.env` and `instance/` are excluded from version control.

---

## Deployment

For a production environment, consider the following:

1. Replace SQLite with **PostgreSQL** or **MySQL** by updating `SQLALCHEMY_DATABASE_URI` in `.env`.
2. Use **Gunicorn** as the WSGI server:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```
3. Serve static files and reverse-proxy Gunicorn via **Nginx**.
4. Set `DEBUG=False` and move all secrets to platform environment variables or a secrets manager.
5. Use a process manager such as **systemd** or **Supervisor** to keep the app running.

---

## Contributing

Contributions are welcome. Please follow the steps below:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes with a descriptive message: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feature/your-feature`
5. Open a Pull Request against `main`.

Please ensure your code follows PEP 8 style guidelines and includes relevant comments where appropriate.

---

<p align="center">Built with Flask and Tailwind CSS</p>
