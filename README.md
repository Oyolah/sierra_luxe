# Sierra Luxe - African Fashion E-Commerce

A professional Django-based e-commerce platform showcasing African fashion for women, men, and kids.

## Project Overview
Sierra Luxe is an online fashion marketplace featuring authentic African dress designs including:
- Women's Fashion (Lace dresses, Asoebi, Wedding dresses, Wax print skirts)
- Men's Fashion (Aso-oke, Embroidered agbada)
- Kids' Fashion (Ankara ball gowns, Birthday outfits)

## Technology Stack
- **Backend**: Django 6.0.7
- **Frontend**: HTML, CSS, JavaScript/jQuery, Bootstrap 4
- **Database**: SQLite (development), PostgreSQL (production)
- **Image Processing**: Pillow 12.3.0
- **Forms**: django-crispy-forms, crispy-bootstrap4

## Project Structure
```
sierra_luxe/
├── cart/                   # Shopping cart functionality
├── catalog/                # Product catalog and browsing
├── orders/                 # Order management
├── reviews/                # Product ratings and reviews
├── users/                  # User authentication and profiles
├── sierra_luxe/           # Main project settings
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates
├── media/                 # User uploaded files
└── requirements.txt       # Python dependencies
```

## Setup Instructions

### 1. Clone the repository
```bash
git clone git@github.com:Oyolah/sierra_luxe.git
cd sierra_luxe
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create superuser (admin)
```bash
python manage.py createsuperuser
```

### 6. Run development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Features (Planned)
- [x] Project setup and configuration
- [ ] User authentication (registration, login, logout)
- [ ] Product catalog with categories
- [ ] Advanced search and filtering
- [ ] Shopping cart
- [ ] Order management
- [ ] Product ratings and reviews
- [ ] Wishlist functionality
- [ ] Admin dashboard
- [ ] Recommender system
- [ ] Responsive design

## Course Information
**Course**: ITC4214 Internet Programming  
**Institution**: [Your Institution]  
**Semester**: Summer 2026

## License
Educational project for ITC4214 Internet Programming course.
