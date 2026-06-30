"""
Tipping Point Lab – Django settings

Environment variables (set in .env for local dev, in hosting dashboard for prod):

  DATABASE_URL   Full Postgres URL
  SECRET_KEY     Django secret key 
  DEBUG          'True' or 'False' (default True in dev)
  ALLOWED_HOSTS  Comma-separated hostnames for production 
  FRONTEND_URL   Your Next.js frontend URL for CORS 
"""

import os
from pathlib import Path

# Load .env file if python-dotenv is installed (optional, dev convenience)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / '.env')
except ImportError:
    pass  


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')


DEBUG = 'False'

_raw_hosts = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(',') if h.strip()] or ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    'corsheaders',
    # Local apps
    'apps.tipping_points',
    'apps.claims',
    'apps.simulator',
    'apps.metrics'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
_DATABASE_URL = os.environ.get('DATABASE_URL', '')

if _DATABASE_URL:
    import re
    _m = re.match(
        r'postgres(?:ql)?://(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:/]+)(?::(?P<port>\d+))?/(?P<name>.+)',
        _DATABASE_URL,
    )
    if _m:
        DATABASES = {
            'default': {
                'ENGINE':   'django.db.backends.postgresql',
                'NAME':     _m.group('name'),
                'USER':     _m.group('user'),
                'PASSWORD': _m.group('password'),
                'HOST':     _m.group('host'),
                'PORT':     _m.group('port') or '5432',
                'OPTIONS':  {'sslmode': 'require'} if 'supabase.co' in _DATABASE_URL else {},
            }
        }
    else:
        raise ValueError(f'DATABASE_URL format not recognised: {_DATABASE_URL!r}')
else:
    # Fallback: SQLite for zero-config local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':   BASE_DIR / 'db.sqlite3',
        }
    }


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

ALLOWED_HOSTS = ['climate-change-service-production.up.railway.app', 'your-frontend.vercel.app']

_frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
CORS_ALLOWED_ORIGINS = [_frontend_url]

STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL   = '/media/'
MEDIA_ROOT  = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATA_DIR = BASE_DIR / 'data'
SEED_CSV  = DATA_DIR / 'tipping_point_seed_data.csv'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
