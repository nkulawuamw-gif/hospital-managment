import os
from datetime import timedelta
from decouple import config, Csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY', default='dev-secret-key-change-in-production')
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default='')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = [
    f'https://{h}' for h in ALLOWED_HOSTS if h != 'localhost'
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',
    'import_export',
    'crispy_forms',
    'crispy_bootstrap5',
    'drf_spectacular',
    'simple_history',
    'django_celery_beat',

    # Apps
    'apps.accounts',
    'apps.patients',
    'apps.appointments',
    'apps.doctors',
    'apps.emr',
    'apps.inpatient',
    'apps.pharmacy',
    'apps.laboratory',
    'apps.billing',
    'apps.insurance',
    'apps.inventory',
    'apps.hr',
    'apps.reports',
    'apps.notifications',
    'apps.audit',
    'apps.dashboard',
    'apps.api',
    'apps.requisitions',
    'apps.encounters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.accounts.middleware.ModuleAccessMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

SITE_NAME = 'Hope Medi - Clinic'
SITE_URL = 'http://localhost:8000'

ROOT_URLCONF = 'hms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.accounts.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'hms.wsgi.application'

DB_DIR = BASE_DIR / "local"
DB_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = config('DATABASE_URL', default='')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
    print(f'Using database: {DATABASES["default"]["ENGINE"]} on {DATABASES["default"]["HOST"]}')
else:
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
            'NAME': DB_DIR / "db.sqlite3",
            'USER': config('DB_USER', default=''),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default=''),
            'PORT': config('DB_PORT', default=''),
        }
    }

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:dashboard'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# ---------- REST Framework ----------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'apps.api.utils.custom_exception_handler',
}

# ---------- JWT ----------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=config('JWT_ACCESS_TOKEN_LIFETIME_HOURS', default=1, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('JWT_REFRESH_TOKEN_LIFETIME_DAYS', default=30, cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# ---------- CORS ----------
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:8000', cast=Csv())

# ---------- Spectacular (API Docs) ----------
SPECTACULAR_SETTINGS = {
    'TITLE': 'Hospital Management System API',
    'DESCRIPTION': 'Enterprise-level HMS REST API',
    'VERSION': '1.0.0',
}

# ---------- Celery ----------
if config('CELERY_BROKER_URL', default='') and not config('DISABLE_CELERY', default=True, cast=bool):
    CELERY_BROKER_URL = config('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Africa/Nairobi'

# ---------- Email ----------
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
if 'smtp' in EMAIL_BACKEND:
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='HMS <noreply@hospital.com>')

# ---------- Redis Cache ----------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

if config('REDIS_URL', default='') and not config('DISABLE_REDIS', default=False, cast=bool):
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL'),
    }

# ---------- Session ----------
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ---------- Logging ----------
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
        'level': 'INFO',
    },
}
