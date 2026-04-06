# Finance Dashboard Backend

A production-ready REST API backend for a finance dashboard system.
Built with Django and Django REST Framework with role-based access control,
JWT authentication, and analytics endpoints.

---

## Tech Stack

| Technology | Purpose |
|------------|---|
| Python 3.13 | Programming language |
| Django 6.0 v| Web framework |
| Django REST Framework | API development |
| MySQL | Database |
| SimpleJWT | JWT authentication |
| django-cors-headers | CORS handling |
| python-decouple | Environment variables |

---

## Project Overview

This backend powers a finance dashboard where different users interact
with financial records based on their assigned role. The system supports
full financial record management, role-based access control, and
summary-level analytics designed to serve a frontend dashboard.

---

## Features

### User & Role Management
- Register and manage users
- Three roles: Viewer, Analyst, Admin
- JWT-based login with access and refresh tokens
- Activate or deactivate user accounts

### Financial Records Management
- Create, view, update, and delete financial records
- Each record includes: amount, type, category, date, notes
- Soft delete — records are never permanently removed
- Filter records by type, category, and date range

### Dashboard Analytics APIs
- Total income, total expenses, net balance
- Category-wise breakdown of transactions
- Monthly trends (last N months)
- Weekly trends (last N weeks)
- Recent activity feed

### Access Control
- Middleware-level role enforcement
- Clean 401/403 responses for unauthorized access
- Each endpoint clearly defines which role can access it

### Validation & Error Handling
- Centralized error handler with consistent JSON responses
- Field-level validation errors
- Meaningful status codes (400, 401, 403, 404)

---

## Role-Based Access Control

| Action                     | Viewer | Analyst | Admin |
|---                         |--------|-------- |-------|
| View dashboard summary     | ✅    | ✅      | ✅   |
| View recent activity       | ✅    | ✅      | ✅   |
| View all records           | ❌    | ✅      | ✅   |
| View category breakdown    | ❌    | ✅      | ✅   |
| View monthly/weekly trends | ❌    | ✅      | ✅   |
| Create records             | ❌    | ❌      | ✅   |
| Update records             | ❌    | ❌      | ✅   |
| Delete records             | ❌    | ❌      | ✅   |
| Manage users               | ❌    | ❌      | ✅   |

---

## Setup Instructions

### Prerequisites
- Python 3.10 or above
- MySQL installed and running
- Git installed

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/finance-dashboard-backend.git
cd finance-dashboard-backend
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers mysqlclient python-decouple
```

### 4. Create MySQL database

Open MySQL and run:
```sql
CREATE DATABASE finance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Create `.env` file

Create a `.env` file in the root folder:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=finance_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

### 6. Run migrations
```bash
python manage.py migrate
```

### 7. Create a superuser (admin account)
```bash
python manage.py createsuperuser
```

### 8. Start the development server
```bash
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000/`

---

## API Endpoints

### Health Check
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | / | Public | API health check |

### Authentication
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | /api/auth/login/ | Public | Login and get JWT tokens |
| POST | /api/auth/refresh/ | Public | Refresh access token |

### Users
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | /api/users/register/ | Public | Register new user |
| GET | /api/users/me/ | Any authenticated | View own profile |
| GET | /api/users/ | Admin | List all users |
| PATCH | /api/users/\<id\>/ | Admin | Update role or status |

### Financial Records
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | /api/records/ | Analyst, Admin | List all records |
| POST | /api/records/ | Admin | Create a record |
| PATCH | /api/records/\<id\>/ | Admin | Update a record |
| DELETE | /api/records/\<id\>/ | Admin | Soft delete a record |

#### Available Filters
```
/api/records/?type=income
/api/records/?type=expense
/api/records/?category=salary
/api/records/?date_from=2026-01-01
/api/records/?date_to=2026-12-31
/api/records/?type=income&date_from=2026-01-01
```

### Dashboard
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | /api/dashboard/ | Any authenticated | Full dashboard data |
| GET | /api/dashboard/summary/ | Any authenticated | Income, expenses, balance |
| GET | /api/dashboard/categories/ | Analyst, Admin | Category breakdown |
| GET | /api/dashboard/trends/monthly/ | Analyst, Admin | Monthly trends |
| GET | /api/dashboard/trends/weekly/ | Analyst, Admin | Weekly trends |
| GET | /api/dashboard/recent/ | Any authenticated | Recent transactions |

---
## API Testing (Postman)

You can test all APIs using this Postman collection:

[Postman Collection Link](https://www.postman.com/bhawsarkhushi2004-4200414/workspace/khushi-bhawsar-s-workspace/collection/53772101-b8f25f4a-c260-4c6b-aba1-967d44ec4108?action=share&creator=53772101)

---

## Project Structure
```
finance_dashboard/
├── manage.py
├── .env                        # Environment variables (not in git)
├── .gitignore
├── README.md
├── finance_backend/            # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── exceptions.py           # Centralized error handler
│   └── wsgi.py
├── users/                      # User management + roles
│   ├── models.py               # Custom User model
│   ├── views.py                # Register, list, detail, me
│   ├── serializers.py
│   ├── permissions.py          # IsAdmin, IsAnalystOrAdmin
│   └── urls.py
├── records/                    # Financial records
│   ├── models.py               # FinancialRecord model
│   ├── views.py                # CRUD + filtering
│   ├── serializers.py
│   └── urls.py
└── dashboard/                  # Analytics
    ├── views.py                # Summary, trends, breakdown
    └── urls.py
```

---

## Assumptions

- Email is used as the login identifier instead of a username.
- Deleted records use soft delete — `deleted_at` is set, the row is kept.
- Viewer role can only access summary and recent activity.
- Token lifetime is 24 hours for development convenience.
- All API responses follow a consistent JSON structure.

---

## Future Improvements

- Search support across records by notes or category
- Pagination improvements with cursor-based pagination
- Export records to CSV or PDF
- Email notifications for large transactions
- Rate limiting on authentication endpoints
- Unit tests and integration tests
- Docker support for easier deployment
- Yearly trend analytics

---

## Author

Built as a backend assessment project to demonstrate scalable API design,
clean architecture, role-based access control, and real-world data handling
using Django REST Framework.
