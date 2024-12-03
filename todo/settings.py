"""
Django settings for todo project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Determine the environment and select the appropriate keys file
ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    keys_file = str(BASE_DIR)+"/keys.production.json"
else:
    keys_file = str(BASE_DIR)+"/keys.json"

# Open the JSON file and read its contents
with open(keys_file) as f:
    project_keys = json.loads(f.read()) # Converts JSON string to dictionary


# Function to retrieve keys
def getKey(setting, default=None):
    if isinstance(project_keys, dict):
        return project_keys.get(setting, default)
    else:
        raise TypeError("project_keys should be a dictionary")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getKey("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getKey('DJANGO_DEBUG')

ALLOWED_HOSTS = ['almalkias.pythonanywhere.com', '127.0.0.1']

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:3000',
    'http://localhost:3000', 
    'https://youdo.netlify.app'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'todo_api', 
    'django_password_validators'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

AUTH_USER_MODEL = "todo_api.CustomUser"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'todo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'todo_api/templates'],
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

WSGI_APPLICATION = 'todo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': getKey('DJANGO_DB_ENGINE'),
        'NAME': getKey('DJANGO_DB_NAME'),
        'USER': getKey('DJANGO_DB_USER', ''),
        'PASSWORD': getKey('DJANGO_DB_PASSWORD', ''),
        'HOST': getKey('DJANGO_DB_HOST', ''),
        'PORT': getKey('DJANGO_DB_PORT', ''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django_password_validators.password_character_requirements.password_validation.PasswordCharacterValidator',
        'OPTIONS': {
            'min_length_digit': 1,
            'min_length_alpha': 2,
            'min_length_special': 1,
            'special_characters': "~!@#$%^&*()_+{}\":;'[].<>|/,`-",
        }
    }
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Riyadh'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DOMAIN = '127.0.0.1:3000'  # Your frontend domain without http/https
SITE_NAME = 'To Do'  # The name that appears in the email

DJOSER = {
    "USER_CREATE_PASSWORD_RETYPE": True,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True, 
    'DOMAIN': DOMAIN,
    'SITE_NAME': SITE_NAME
}

EMAIL_BACKEND = getKey("EMAIL_BACKEND", '')
EMAIL_HOST = getKey("EMAIL_HOST", '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = getKey("EMAIL_HOST_USER", '')
EMAIL_HOST_PASSWORD = getKey("EMAIL_HOST_PASSWORD", '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
