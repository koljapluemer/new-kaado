import django_heroku
import os
import environ 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# env stuff
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


ALLOWED_HOSTS = ['chaoskasten.com', 'localhost', 'chaoskasten.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'main',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lazysignup',
    'stripe',
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

AUTHENTICATION_BACKENDS = (
  'django.contrib.auth.backends.ModelBackend',
  'lazysignup.backends.LazySignupBackend',
)


ROOT_URLCONF = 'main.urls'

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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': os.environ['DATABASE_PORT'],
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


DOMAIN_URL = os.environ['DOMAIN_URL']

if os.environ["STRIPE_LIVE_MODE"] == "True":
    print('stripe live mode')
    STRIPE_PUBLIC_KEY = os.environ['STRIPE_LIVE_PUBLIC_KEY']
    STRIPE_SECRET_KEY = os.environ['STRIPE_LIVE_SECRET_KEY']
else:
    print('stripe test mode')
    STRIPE_PUBLIC_KEY = os.environ["STRIPE_TEST_PUBLIC_KEY"]
    STRIPE_SECRET_KEY = os.environ["STRIPE_TEST_SECRET_KEY"]



STRIPE_PRICE_ID = os.environ["STRIPE_PRICE_ID"]

APPEND_SLASH=False

SECRET_KEY = os.environ['SECRET_KEY']

# false when it does not exist (wtf)
try:
    os.environ['DEBUG']
    DEBUG = True
except:
    DEBUG = False

print('DEBUG: ', DEBUG)
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']

# Activate Django-Heroku.
django_heroku.settings(locals())


LAZYSIGNUP_CUSTOM_USER_CREATION_FORM = 'main.forms.SignUpForm'