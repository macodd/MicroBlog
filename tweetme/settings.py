"""
Django settings for tweetme project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wl*%vh)ro8^ggf5=x@oc(nft%=7@b^g&o2n2z29w#z-ywugv59'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

if not DEBUG:
    ALLOWED_HOSTS = ['mark-codd-micro-blog-fogata.herokuapp.com', 'www.lafogata.biz']
else:
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party
    'crispy_forms',
    'rest_framework',
    'storages',

    # local
    'tweets.apps.TweetsConfig',
    'accounts.apps.AccountsConfig',
    'hashtags.apps.HashtagsConfig',
    'register.apps.RegisterConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tweetme.urls'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = LOGIN_URL

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'lafogatablog@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Fogata <info@lafogata.biz>"

ADMINS = [('Mark', EMAIL_HOST_USER)]
MANAGERS = ADMINS

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'tweetme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USERNAME': 'codd8',
        'PASSWORD': 'Morgenth@u2016',
        'HOST': 'localhost',
        'PORT': '',
    }
}
if not DEBUG:
    import dj_database_url
    db_from_env = dj_database_url.config()
    DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

CRISPY_TEMPLATE_PACK = 'bootstrap4'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

if DEBUG:
    STATIC_URL = '/static/'
    LOCAL_STATIC_CDN = os.path.join(os.path.dirname(BASE_DIR), 'static-cdn')
    STATIC_ROOT = os.path.join(LOCAL_STATIC_CDN, 'static')
    MEDIA_ROOT = os.path.join(LOCAL_STATIC_CDN, 'media')
    MEDIA_URL = '/media/'

else:

    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''

    AWS_FILE_EXPIRE = 200
    AWS_PRELOAD_METADATA = True
    AWS_QUERYSTRING_AUTH = True

    DEFAULT_FILE_STORAGE = 'tweetme.storage_backends.MediaRootS3Boto3Storage'
    STATICFILES_STORAGE = 'tweetme.storage_backends.StaticRootS3Boto3Storage'

    AWS_STORAGE_BUCKET_NAME = ''
    AWS_DEFAULT_ACL = 'public-read'
    S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
    MEDIA_ROOT = MEDIA_URL
    STATIC_URL = S3_URL + 'static/'
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

    import datetime

    two_months = datetime.timedelta(days=61)
    date_two_months_later = datetime.date.today() + two_months
    expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

    AWS_HEADERS = {
        'Expires': expires,
        'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
    }

CELERY_BROKER_URL = 'redis://h:pd099a5bbc21c431e00d9a10ce92dc60a734be504ee164074a491c80e84a72227@ec2-52-21-199-125.compute-1.amazonaws.com:28899'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL'),
    }
}
