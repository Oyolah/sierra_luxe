# ITC4214 Internet Programming - Course Flow Summary

## Course Structure (Based on Lecture Notes)

### 1. Django Introduction & Framework Basics
- **Web Development Frameworks**: Foundation for developing software applications
- **Django Framework**: Model-View-Template (MVT) architecture
- **URL Configuration**: URLconf patterns to route requests
- **Views**: Handle HTTP requests and return responses
- **Templates**: Django Template Language for dynamic HTML

### 2. Django Project Structure
**Standard Flow:**
1. Create Django project: `django-admin startproject project_name`
2. Create apps: `python manage.py startapp app_name`
3. Register apps in `settings.py` INSTALLED_APPS
4. Configure URLs in project's `urls.py` using `include()`
5. Create app-specific `urls.py` with URL patterns
6. Define views in `views.py`
7. Create templates for rendering HTML

### 3. SQL, Models, and Migrations
**Database Abstraction:**
- Django provides abstraction layer over SQL
- Work with Python classes (Models) instead of raw SQL queries
- Relational databases: MySQL, PostgreSQL, SQLite, Oracle

**Models:**
- Python classes that inherit from `models.Model`
- Define database schema using class attributes
- Field types: CharField, IntegerField, ForeignKey, ManyToManyField, etc.

**Example Model Structure:**
```python
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE)
    duration = models.IntegerField()
```

**Migrations:**
- `python manage.py makemigrations` - Create migration files
- `python manage.py migrate` - Apply migrations to database
- Migrations track changes to models and update database schema

### 4. Django Template Language
**Dynamic Content:**
- Variables: `{{ variable_name }}`
- Template tags: `{% tag %}`
- Filters: `{{ variable|filter }}`
- Template inheritance: `{% extends "base.html" %}`
- Blocks: `{% block content %}{% endblock %}`

**Example Use Case:**
- Tasks app to manage todo lists
- Dynamic pages like "isitchristmas.com" that change based on date
- Conditional rendering based on data

### 5. Views and URL Routing
**URL Patterns:**
```python
urlpatterns = [
    path('tasks/', views.index, name='index'),
    path('admin/', admin.site.urls),
]
```

**View Functions:**
- Receive HTTP request
- Process data (query models, perform logic)
- Return HTTP response (render template, redirect, etc.)

### 6. Request-Response Cycle
1. Browser requests page by URL
2. Web server passes HTTP request to Django
3. Django checks `urls.py` for matching URL pattern
4. Django executes corresponding view
5. View interacts with Models (if needed)
6. View renders Template with data
7. Django returns HTTP response to browser

## Key Concepts for Sierra Luxe Project

### Project Setup Pattern:
1. ✅ Create virtual environment
2. ✅ Install Django and dependencies
3. ✅ Create Django project
4. ✅ Create multiple apps (catalog, users, orders, reviews, cart)
5. ✅ Configure settings.py (INSTALLED_APPS, static/media files)
6. ✅ Set up URL routing

### Next Steps (Following Course Flow):
1. **Define Models** (Phase 2):
   - Create model classes for each app
   - Define relationships (ForeignKey, ManyToManyField)
   - Run makemigrations and migrate

2. **Create Views** (Phase 3-11):
   - Function-based or class-based views
   - Handle GET/POST requests
   - Query models and pass data to templates

3. **Design Templates** (Phase 13):
   - Create base template with inheritance
   - Use Django Template Language for dynamic content
   - Implement forms with crispy-forms

4. **Configure URLs** (Throughout):
   - Map URLs to views
   - Use named URL patterns
   - Implement URL namespacing

5. **Admin Interface** (Phase 9):
   - Register models in admin.py
   - Customize admin interface

6. **Authentication** (Phase 3):
   - Use Django's built-in authentication
   - Create custom user registration/login views
   - Implement role-based access control

## Course Teaching Approach
- **Practical Examples**: Real-world applications (airline, tasks, isitchristmas)
- **Incremental Building**: Start simple, add complexity
- **MVT Architecture**: Separation of concerns (Models, Views, Templates)
- **Database Abstraction**: Work with Python objects, not SQL
- **Official Django Tutorials**: Follow Django documentation

## Application to Sierra Luxe
Following the course methodology:
1. Models first (database schema)
2. Admin interface for data management
3. Views for business logic
4. Templates for user interface
5. URL routing to connect everything
6. Forms for user input
7. Authentication for security
