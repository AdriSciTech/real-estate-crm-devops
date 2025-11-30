# Real Estate CRM

![CI Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci.yml/badge.svg)
[![Coverage](https://img.shields.io/badge/coverage-97%25-brightgreen)](htmlcov/index.html)

A web-based Customer Relationship Management (CRM) system designed for real estate professionals to manage properties, clients, tasks, and collaborate with team members.

## Features

### Currently Implemented
- **Property Management**: Full CRUD operations for real estate listings
  - Add, view, update, and delete properties
  - Track property details including price, type, status, and specifications
  - Filter properties by status and type
  - Search properties by address or description
  - Assign properties to collaborators

- **Client Management**: Track buyers and sellers
  - Manage client contact information
  - Track client type (Buyer/Seller/Both)
  - Link clients to properties of interest

- **Task Management**: Create and manage tasks with due dates
  - Set priority levels and status
  - Assign tasks to collaborators
  - Link tasks to properties or clients

- **Collaborator Management**: Manage team members and assignments
  - Track roles (Agent, Manager, Admin, Assistant)
  - View assigned properties and tasks

## Technology Stack

- **Backend**: Django 5.0+ (Python web framework)
- **Database**: SQLite (lightweight, file-based database)
- **Frontend**: HTML, CSS (no JavaScript dependencies)
- **Testing**: pytest, pytest-django, pytest-cov

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd real-estate-crm
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create and apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to: http://127.0.0.1:8000/
   - Admin interface (if superuser created): http://127.0.0.1:8000/admin/

## Testing

### Run All Tests
```bash
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=crm --cov-report=html
```

### Run Specific Test Files
```bash
# Run model tests
pytest crm/tests/test_models.py -v

# Run form tests
pytest crm/tests/test_forms.py -v

# Run service tests
pytest crm/tests/test_services.py -v

# Run view tests
pytest crm/tests/test_views.py -v
```

### View Coverage Report
After running tests with coverage, open `htmlcov/index.html` in your browser.

### Current Test Coverage
- **145 tests** covering all major functionality
- **97.89% code coverage** (above the 70% requirement)

## Project Structure

```
real-estate-crm/
├── realestate_crm/          # Main Django project directory
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py
├── crm/                     # Main application
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   └── crm/
│   │       ├── base.html
│   │       ├── home.html
│   │       └── ... (other templates)
│   ├── tests/               # Test files
│   │   ├── test_constants.py
│   │   ├── test_forms.py
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_views.py
│   ├── __init__.py
│   ├── admin.py            # Admin interface configuration
│   ├── apps.py
│   ├── constants.py        # Centralized constants
│   ├── forms.py            # Django forms
│   ├── models.py           # Database models
│   ├── services.py         # Business logic layer
│   ├── urls.py             # App URL configuration
│   └── views.py            # View functions
├── conftest.py             # Pytest fixtures
├── pytest.ini              # Pytest configuration
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── REPORT.md               # Code quality improvement report
└── README.md               # This file
```

## Code Quality

### SOLID Principles Applied
- **Single Responsibility**: Separate layers for models, forms, services, views
- **Open/Closed**: Constants can be extended without modification
- **Liskov Substitution**: TimeStampedModel base class for all models
- **Interface Segregation**: Specific forms and services per domain
- **Dependency Inversion**: Views depend on service abstractions

### Architecture
- **Constants Layer**: Centralized configuration in `constants.py`
- **Service Layer**: Business logic in `services.py`
- **Model Layer**: Data structure and basic methods in `models.py`
- **Form Layer**: Validation and widgets in `forms.py`
- **View Layer**: HTTP handling in `views.py`

## Environment Variables

The application supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | Development key (change in production) |
| `DJANGO_DEBUG` | Debug mode | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts | Empty |

## Usage Guide

### Managing Properties

1. **View all properties**: Click "Properties" in the navigation menu
2. **Add a new property**: Click "Add New Property" button
3. **Edit a property**: Click "Edit" link next to any property
4. **Delete a property**: Click "Delete" link and confirm
5. **Filter properties**: Use the filter form to search by status or type
6. **Search properties**: Use the search box to find properties by address

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/feature-name`
3. Make your changes
4. Run tests: `pytest`
5. Commit with descriptive messages
6. Push to repository
7. Submit a pull request

## License

This project is created for educational purposes as part of a Software Development DevOps course at IE University.