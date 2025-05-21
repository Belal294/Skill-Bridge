import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from decouple import config
import cloudinary

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Static & Media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security
SECRET_KEY = config("SECRET_KEY", default="your-default-secret-key")
DEBUG = True

# Frontend Config
# FRONTEND_PROTOCOL = config("FRONTEND_PROTOCOL")
# FRONTEND_DOMAIN = config("FRONTEND_DOMAIN")
# FRONTEND_URL = f"{FRONTEND_PROTOCOL}://{FRONTEND_DOMAIN}"

FRONTEND_PROTOCOL="https"
FRONTEND_DOMAIN="skill-bridge-client.vercel.app"
# FRONTEND_PROTOCOL="http"
# FRONTEND_DOMAIN="localhost:5173"
FRONTEND_URL = f"{FRONTEND_PROTOCOL}://{FRONTEND_DOMAIN}"
ALLOWED_HOSTS = [".vercel.app", "127.0.0.1", "localhost"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'corsheaders',
    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
    'django_filters',
    'whitenoise.runserver_nostatic',

    'users',
    'api',
    'services',
    'orders',
    'reviews',
    'dashboard',
    'notifications',
    'notes',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skillbridge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'skillbridge.wsgi.app'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('dbname'),
        'USER': config('user'),
        'PASSWORD': config('password'),
        'HOST': config('host'),
        'PORT': config('port'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'https://skill-bridge-client.vercel.app',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Cloudinary Configuration
cloudinary.config(
    cloud_name=config('cloud_name'),
    api_key=config('api_key'),
    api_secret=config('api_secret_key'),
    secure=True
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Djoser Config
DJOSER = {
    'EMAIL': {
        'activation': 'users.email.CustomActivationEmail',
    },
    'USER_CREATE_PASSWORD_RETYPE': False,
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializer',
        'user': 'users.serializers.UserSerializer',
        'current_user': 'users.serializers.UserSerializer',
        # 'password_reset': 'users.serializers.CustomPasswordResetSerializer',
    },
}


# DJOSER = {
#     'EMAIL': {
#         'activation': 'users.email.CustomActivationEmail',
#     },
#     'USER_CREATE_PASSWORD_RETYPE': False,
#     'SEND_ACTIVATION_EMAIL': True,
#     'ACTIVATION_URL': "{FRONTEND_URL}/activate/{uid}/{token}",
#     'PASSWORD_RESET_CONFIRM_URL': "{FRONTEND_URL}/password/reset/confirm/{uid}/{token}",
#     'SERIALIZERS': {
#         'user_create': 'users.serializers.UserCreateSerializer',
#         'user': 'users.serializers.UserSerializer',
#         'current_user': 'users.serializers.UserSerializer',
#     },
# }


# For Djoser email site info
SITE_NAME = "Skill Bridge"
DOMAIN = FRONTEND_DOMAIN

# Stripe Keys
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
