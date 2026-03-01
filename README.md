# SmartCommerce Backend

A production-style Django backend project focused on building a scalable, real-world e-commerce architecture.

This project is being developed step-by-step with professional engineering practices including testing, version control, and structured documentation.

---

## 🚀 Current Phase
**Phase 1 – Infrastructure & Foundation Setup**

---

## ✅ Completed So Far

### Project Setup
- Clean Django project initialization
- Proper project structure (no nested mistakes)
- Virtual environment setup
- Dependency management using `requirements.txt`

### Database
- SQLite setup for development
- Initial migrations applied successfully
- Superuser creation and admin verification

### Authentication Verification
- Verified Django authentication system
- Confirmed password hashing and session management
- Admin panel login working

### Testing
- Basic unit test implemented for user creation
- Django test database verified
- ORM read/write operations confirmed

### Version Control
- Git initialized properly
- Clean `.gitignore` configuration
- GitHub repository linked
- Structured commit messages

---

## 🛠 Tech Stack (Current)

- Python
- Django
- SQLite (Development)
- Git & GitHub

---
## 📂 Project Structure
ecommerce_backend/
│
├── core/
│ ├── settings.py
│ ├── urls.py
│ ├── asgi.py
│ ├── wsgi.py
│ └── tests.py
│
├── manage.py
├── requirements.txt
├── dev_log.md
└── README.md


---

## 🔜 Upcoming (Next Steps)

- Create custom user model (email-based authentication)
- Create `accounts` app
- Integrate Django REST Framework (DRF)
- Implement JWT authentication
- Migrate from SQLite to PostgreSQL

---

## 🎯 Project Goal

To build a production-ready, scalable e-commerce backend demonstrating:

- Proper authentication architecture
- Database design & optimization
- Background task processing
- Caching strategies
- API security
- Deployment readiness

---

## ▶ How to Run Locally

1. Create and activate virtual environment
2. Install dependencies:
  pip install -r requirements.txt
3.  Apply migrations:
  python manage.py migrate
4.   Run server:
   python manage.py runserver
