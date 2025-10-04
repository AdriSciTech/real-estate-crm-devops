# Real Estate CRM

A web-based Customer Relationship Management (CRM) system designed for real estate professionals to manage properties, clients, tasks, and collaborate with team members.

## Features

### Currently Implemented
- **Property Management**: Full CRUD operations for real estate listings
  - Add, view, update, and delete properties
  - Track property details including price, type, status, and specifications
  - Filter properties by status and type
  - Search properties by address or description
  - Assign properties to collaborators

### Planned Features
- **Client Management**: Track buyers and sellers
- **Task Management**: Create and manage tasks with due dates
- **Collaborator Management**: Manage team members and assignments

## Technology Stack

- **Backend**: Django 5.0+ (Python web framework)
- **Database**: SQLite (lightweight, file-based database)
- **Frontend**: HTML, CSS (no JavaScript dependencies)
- **Development Model**: Agile with iterative development

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

4. **Configure Django settings**
   - The project is pre-configured to work out of the box
   - Database settings use SQLite (no additional setup required)

5. **Update the main project's urls.py**
   In `realestate_crm/urls.py`, add the following:
   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('crm.urls')),
   ]
   ```

6. **Update settings.py**
   In `realestate_crm/settings.py`, ensure 'crm' is in INSTALLED_APPS:
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'crm',  # Add this line
   ]
   ```

   Also add this to enable proper number formatting:
   ```python
   USE_THOUSAND_SEPARATOR = True
   ```

7. **Create and apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Open your browser and navigate to: http://127.0.0.1:8000/
    - Admin interface (if superuser created): http://127.0.0.1:8000/admin/

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
│   │       ├── property_list.html
│   │       ├── property_detail.html
│   │       ├── property_form.html
│   │       └── property_confirm_delete.html
│   ├── __init__.py
│   ├── admin.py            # Admin interface configuration
│   ├── apps.py
│   ├── forms.py            # Django forms
│   ├── models.py           # Database models
│   ├── urls.py             # App URL configuration
│   └── views.py            # View functions
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Usage Guide

### Managing Properties

1. **View all properties**: Click "Properties" in the navigation menu
2. **Add a new property**: Click "Add New Property" button
3. **Edit a property**: Click "Edit" link next to any property
4. **Delete a property**: Click "Delete" link and confirm
5. **Filter properties**: Use the filter form to search by status or type
6. **Search properties**: Use the search box to find properties by address

### Database Schema

The application uses four main database tables:

- **Properties**: Stores property listings with address, price, type, and status
- **Clients**: Manages buyer and seller information
- **Tasks**: Tracks tasks and reminders with due dates
- **Collaborators**: Manages team members who can be assigned to properties

## Development Workflow

### Git Commit Guidelines

Follow these conventions for commit messages:
- `feat(scope): description` - New features
- `fix(scope): description` - Bug fixes
- `docs(scope): description` - Documentation updates
- `style(scope): description` - Code style changes
- `refactor(scope): description` - Code refactoring
- `test(scope): description` - Test additions/changes

Example: `feat(property): add property search functionality`

### Adding New Features

1. Create a new branch: `git checkout -b feature/feature-name`
2. Make your changes
3. Test thoroughly
4. Commit with descriptive messages
5. Push to repository

## Scaling and DevOps Considerations

### Potential Scaling Improvements

1. **Database**: Migrate from SQLite to PostgreSQL for production
2. **Caching**: Implement Redis for session and data caching
3. **Static Files**: Use CDN for serving static assets
4. **Media Storage**: Integrate cloud storage (S3) for property images
5. **Search**: Implement Elasticsearch for advanced property search
6. **API**: Add Django REST Framework for mobile app support

### DevOps Practices

1. **Containerization**: Use Docker for consistent deployments
2. **CI/CD Pipeline**: Implement with GitHub Actions or GitLab CI
3. **Monitoring**: Add application monitoring (Sentry, New Relic)
4. **Load Balancing**: Use Nginx as reverse proxy
5. **Environment Management**: Separate settings for dev/staging/production
6. **Automated Testing**: Implement unit and integration tests
7. **Database Backups**: Automated daily backups
8. **Security**: Implement SSL, security headers, and regular updates

## Troubleshooting

### Common Issues

1. **"No module named 'crm'" error**
   - Ensure 'crm' is added to INSTALLED_APPS in settings.py

2. **Template not found errors**
   - Check that templates are in the correct directory: `crm/templates/crm/`

3. **Database errors**
   - Run `python manage.py makemigrations` and `python manage.py migrate`

4. **Static files not loading**
   - Ensure DEBUG=True in settings.py for development

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## License

This project is created for educational purposes as part of a Software Development Life Cycle course.

## Support

For questions or issues, please create an issue in the project repository.