# Skill-Bridge

## Description
Skill-Bridge is a freelancing platform where buyers and sellers interact. Buyers can purchase services, and sellers provide services. An admin manages users and has full access to oversee platform activities.

## Features
- User authentication (Buyer & Seller roles)
- Service listing and management
- Order placement and tracking
- Review and rating system
- Notification system
- Admin dashboard

## Installation

### Prerequisites
Make sure you have the following installed:
- Python 3.8+
- Django 5.1.7
- PostgreSQL (or any preferred database)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/skillbridge.git
   cd skillbridge
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Required Packages
```
asgiref==3.8.1
certifi==2025.1.31
cffi==1.17.1
charset-normalizer==3.4.1
cloudinary==1.43.0
cryptography==44.0.2
defusedxml==0.7.1
Django==5.1.7
django-cloudinary-storage==0.3.0
django-filter==25.1
djangorestframework==3.15.2
djangorestframework_simplejwt==5.5.0
djoser==2.3.1
drf-yasg==1.21.10
idna==3.10
inflection==0.5.1
oauthlib==3.2.2
packaging==24.2
pillow==11.1.0
psycopg2-binary==2.9.10
pycparser==2.22
PyJWT==2.9.0
python-decouple==3.8
python-dotenv==1.1.0
python3-openid==3.2.0
pytz==2025.2
PyYAML==6.0.2
requests==2.32.3
requests-oauthlib==2.0.0
six==1.17.0
social-auth-app-django==5.4.3
social-auth-core==4.5.6
sqlparse==0.5.3
tzdata==2025.2
uritemplate==4.1.1
urllib3==2.3.0
whitenoise==6.9.0
```

4. Configure environment variables (create a `.env` file):
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=your_database_url
   ```
5. Apply migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints (if applicable)
| Method | Endpoint            | Description              |
|--------|---------------------|--------------------------|
| POST   | /api/auth/login/    | User login              |
| POST   | /api/auth/register/ | User registration       |
| GET    | /api/services/      | List all services       |
| POST   | /api/orders/        | Place a new order       |
| GET    | /api/reviews/       | Fetch all reviews       |

## Technologies Used
- Django 5.1.7
- Django REST Framework
- PostgreSQL
- Docker (Optional for deployment)
- Celery & Redis (For async tasks)
- WhiteNoise (For static file handling)

## Contributing
If you want to contribute, feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

