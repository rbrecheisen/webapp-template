import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

USE_DOCKER = True if int(os.environ.get('USE_DOCKER', '0')) == 1 else False

if USE_DOCKER:
    ROOT_DIR = os.environ.get('ROOT_DIR', '/data')
else:
    ROOT_DIR = os.environ.get('ROOT_DIR', '{}/data'.format(os.environ['HOME']))
os.makedirs(ROOT_DIR, exist_ok=True)

SECRET_KEY = os.environ.get('SECRET_KEY', None)

DEBUG = False if int(os.environ.get('DEBUG', '0')) == 0 else True

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_rq',
    'session_security',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': 5432,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

if USE_DOCKER:
    FILE_UPLOAD_TEMP_DIR = '{}/files'.format(ROOT_DIR)
else:
    FILE_UPLOAD_TEMP_DIR = '/tmp'
os.makedirs(FILE_UPLOAD_TEMP_DIR, exist_ok=True)

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 * 40  # 100mb

WORKER_TIMEOUT = int(os.environ.get('WORKER_TIMEOUT', '500'))

RQ_QUEUES = {
    'default': {
        'HOST': os.environ.get('REDIS_HOST', 'localhost'),
        'PORT': int(os.environ.get('REDIS_PORT', '6379')),
        'DB': int(os.environ.get('REDIS_DB', '0')),
        'DEFAULT_TIMEOUT': WORKER_TIMEOUT,
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
os.makedirs(STATIC_ROOT, exist_ok=True)

MEDIA_URL = '/files/'
MEDIA_ROOT = os.path.join(ROOT_DIR, 'files')
os.makedirs(MEDIA_ROOT, exist_ok=True)

SESSION_SECURITY_WARN_AFTER = 840
SESSION_SECURITY_EXPIRE_AFTER = 900
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
