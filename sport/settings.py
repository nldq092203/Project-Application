"""
Django settings for sport project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-#&z!_!')
DEBUG = os.getenv('DEBUG', 'True')
ALLOWED_HOSTS = ['localhost', '10.0.2.2','127.0.0.1', '.vercel.app']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.gis",
    'orienteering',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sport.urls'

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

WSGI_APPLICATION = 'sport.wsgi.app'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'Sport'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'USER': os.getenv('DB_USER', 'sportmanager'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'sportmanager123'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }, #Ensures that the password isn't too similar to the user's other attributes (e.g., username, email, etc.)
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }, #Enforces a minimum length for the password - 8 characters
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }, #Enforces that the password isn't entirely numeric
]

AUTH_USER_MODEL = 'orienteering.Participant'

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ]
}
DJOSER ={
    'USER_ID_FIELD': 'username',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}', # Generate the URL for the password reset confirmation step
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False, # Sent email to the user after their password has been changed.
    'CREATE_SESSION_ON_LOGIN': False, # Create a new session after logout
    'EMAIL': {
        'password_reset': 'djoser.email.PasswordResetEmail',
        'password_changed_confirmation': 'djoser.email.PasswordChangedConfirmationEmail',
    },
    'COACH_SECRET_CODE': 'iamcoach',
    'SERIALIZERS': {
        'user_create': 'orienteering.serializers.ParticipantSerializer',
    },
}

GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH', r'C:\OSGeo4W\bin\gdal309')
DJANGO_COACH_SECRET_CODE = 'iamcoach'
CORS_ALLOW_ALL_ORIGINS = True



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}


# # Celery Configuration Options
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
# CELERY_TIMEZONE = "UTC"
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60

if os.environ.get('VERCEL'):
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
