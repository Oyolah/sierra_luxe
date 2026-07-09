# Sierra Luxe - African Fashion E-Commerce

A Django-based e-commerce platform for African fashion.

## Tech Stack
- Django 6.0.7
- Bootstrap 4
- SQLite (development)

## Setup
```bash
git clone git@github.com:Oyolah/sierra_luxe.git
cd sierra_luxe
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

## Features
- Product catalog
- Shopping cart
- User authentication
- Order management
- Product reviews
