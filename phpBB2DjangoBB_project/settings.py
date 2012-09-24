# coding: utf-8

"""
    Django settings for phpBB2DjangoBB project.
"""


import os.path

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# We set it to "UTC" (same as Greenwich Mean Time, GMT-0, without daylight-saving time)
TIME_ZONE = "UTC"

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'please change in local_settings.py'


MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'djangobb_forum.middleware.LastLoginMiddleware',
    'djangobb_forum.middleware.UsersOnline',
)

ROOT_URLCONF = 'phpBB2DjangoBB_project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'phpBB2DjangoBB_project.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'pagination',
    'djangobb_forum',
    'haystack',

    'django_phpBB3',
)

try:
    import south
    INSTALLED_APPS += ('south',)
    SOUTH_TESTS_MIGRATE = False
except ImportError:
    pass

FORCE_SCRIPT_NAME = ''

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'djangobb_forum.context_processors.forum_settings',
)

# Haystack settings
HAYSTACK_SITECONF = 'phpBB2DjangoBB_project.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, 'djangobb_index')

# Account settings
ACCOUNT_ACTIVATION_DAYS = 10
LOGIN_REDIRECT_URL = '/forum/'
LOGIN_URL = '/forum/account/signin/'

#Cache settings
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

#------------------------------------------------------------------------------
# default django-phpBB3 settings:

PHPBB_TABLE_PREFIX = u"phpbb3_"

# filesystem path to the /files/ sub directory of the phpBB installation:
# e.g.: = "/path/to/phpBB/files/"
PHPBB_ATTACHMENT_PATH = None

# for redirect example views
# e.g.: domain.tld/phpbb/viewtopic.php?t=123 -> phpbb 
OLD_PHPBB_URL_PREFIX = "phpbb"

# Exists the captcha_questions database table? FIXME: In which case does it exists?
PHPBB_CAPTCHA_QUESTIONS_MODEL_EXIST = False

# Add PhpBBPasswordHasher to the default hashers
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
    'django_phpBB3.hashers.PhpBB3PasswordHasher',
)

#------------------------------------------------------------------------------

try:
    from local_settings import *
except ImportError, err:
    if str(err).startswith("No module named"):
        import os
        msg = (
            "There is no local_settings.py file in '%s' !"
            " (Original error was: %s)\n"
        ) % (os.getcwd(), err)
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(msg)
    else:
        raise
