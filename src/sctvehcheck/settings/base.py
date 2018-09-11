"""
Django settings for sctvehcheck project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from pathlib import Path

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / "directory"
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Additional locations of static files
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.

STATICFILES_DIRS = [str(BASE_DIR / 'static'), ]
MEDIA_ROOT = str(BASE_DIR / 'media')
MEDIA_URL = "/media/"

# Use Django templates using the new Django 1.8 TEMPLATES settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(BASE_DIR / 'templates'),
            # insert more TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Use 12factor inspired environment variables or from a file
import environ

# Create a local.env file in the settings directory
# But ideally this env file should be outside the git repo
env_file = Path(__file__).resolve().parent / 'local.env'
if env_file.exists():
    environ.Env.read_env(str(env_file))

env = environ.Env()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    #Tema de bootstrap adaptativo para django
    'bootstrap_admin',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authtools',
    'crispy_forms',
    'easy_thumbnails',

    'profiles',
    'accounts',
    'hello',
    #Aplicacion para el chequeo de vehiculos
    'vehiclecheck',
    #Global configuration
    'globalconfig',
    #Manage global configurations in django site
    'solo',
    #Captcha para el formulario de verificacion vehicular
    #'captcha',
    #Aplicacion que coloca un boton de borrado en cada widget de tipo texto
    # 'clearable_widget',


    #Smart selects
    'smart_selects',
    #'clearable_widget',
    #Aplicacion para importar/exportar datos en aplicaciones django
    'import_export',
    'adminactions',
    'ajax_select'  # django-ajax-selects



)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'sctvehcheck.urls'

WSGI_APPLICATION = 'sctvehcheck.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/dev/ref/settings/#databases

DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in
    # os.environ
    'default': env.db(),
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

# Locales folder

# Languages support

# Definition of languages supported: django/conf/global_settings.py
LANGUAGES = [

    ('en', _('English (US)')),
    ("es", _('Spanish'))
]

# Allowed IP adresess
ALLOWED_HOSTS = []

#### Crispy Form Theme - Bootstrap 3 ###
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# For Bootstrap 3, change error alert to 'danger'
from django.contrib import messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}
### End Crispy Form settings ####

# Authentication Settings
AUTH_USER_MODEL = 'authtools.User'
LOGIN_REDIRECT_URL = reverse_lazy("profiles:show_self")
LOGIN_URL = reverse_lazy("accounts:login")

THUMBNAIL_EXTENSION = 'png'     # Or any extn for your thumbnails



##############Captcha app settings#########################

#CAPTCHA_LENGTH = 6
#CAPTCHA_BACKGROUND_COLOR = "red"
#CAPTCHA_FOREGROUND_COLOR = "#ffffff"

##############django-ajax-selects settings#################
# define the lookup channels in use on the site
AJAX_LOOKUP_CHANNELS = {
    'cliente': ('vehiclecheck.lookups', 'ClienteLookup'),
    'vehiculo' : ('vehiclecheck.lookups', 'VehiculoLookup'),
}

######################Configurando Memcached como mecanismo de cacheo de Django################
#Se indica que el backend de cacheo es Memcached solamente y que esta corriendo como servicio localmente, en el puerto 11221
CACHES = {
     'default': {
         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
         'LOCATION': '127.0.0.1:11211',
     },
     'local': {
         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
     },
}

#####################################################################################
################Configurando las variables de control de las sessiones de usuario ###################
#Configurando la expiracion de la sesion de usuario.
# Sesion expira al cerrar el navegador.Este por defecto esta en falso
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Tiempo de expiracion de la session en segundos. Por defecto son dos semanas
SESSION_COOKIE_AGE = 5800

#Usando el mecanismo de session basado en cache y base de datos
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
#################################################################################

#####################Django-solo app configutation ############################
SOLO_CACHE = "local"
SOLO_CACHE_TIMEOUT = 60*5 # 5 minutos
SOLO_CACHE_PREFIX = 'solo'

