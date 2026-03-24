# SmartCommerce Backend

A production-style Django backend project focused on building a scalable, real-world e-commerce architecture.

This project is being developed step-by-step with professional engineering practices including testing, version control, and structured documentation.

---

## 🚀 Current Phase
**Phase 1 – Infrastructure & Foundation Setup**

Engineered a RESTful backend using Django & DRF featuring custom user authentication, secure password hashing, token-based authentication (JWT), and modular API architecture.
---

## ✅ Completed So Far

### Project Setup
- Clean Django project initialization
- Proper project structure (no nested mistakes)
- Virtual environment setup
- Dependency management using `requirements.txt`
- Create custom user model (email-based authentication)
- Create `accounts` app
- Integrate Django REST Framework (DRF)

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

- Implement JWT authentication
- Migrate from SQLite to PostgreSQL
phase 2:
1. Category System

Category model

Nested categories (optional advanced)

Slug-based routing

Category API endpoints

📦 2. Product System

Product model

Slug field

Price field

Stock tracking

Active/inactive flag

Product listing endpoint

Product detail endpoint

Filtering & sorting

Advanced:

Product images

Multiple product variants (size, color)

SKU management

🧺 3. Cart System

Cart model

CartItem model

One cart per user

Add to cart endpoint

Remove from cart endpoint

Update quantity endpoint

Auto total calculation

Advanced:

Handle duplicate adds

Atomic cart updates

📑 4. Order System

Order model

OrderItem model

Snapshot product price at time of purchase

Order status (Pending, Paid, Shipped, Delivered)

Order creation endpoint

Order history endpoint

Advanced:

Transaction atomicity

Prevent double order submission

💳 5. Payment Logic (Mocked)

Payment status tracking

Payment reference ID

Order locking after payment

We won’t integrate real gateway yet — but simulate logic properly.
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
