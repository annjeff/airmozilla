# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings/local.py
import os

from bundles import PIPELINE_CSS, PIPELINE_JS


ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        '..'
    ))


def path(*dirs):
    return os.path.join(ROOT, *dirs)


SITE_ID = 1

LANGUAGE_CODE = 'en-US'

PROJECT_MODULE = 'airmozilla'


# Defines the views served for root URLs.
ROOT_URLCONF = '%s.urls' % PROJECT_MODULE

INSTALLED_APPS = (
    'pipeline',
    'django_browserid',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'session_csrf',
    'mozilla_django_oidc',

    # Application base, containing global templates.
    'airmozilla.base',
    'airmozilla.main',
    'airmozilla.authentication',
    'airmozilla.manage',
    'airmozilla.suggest',
    'airmozilla.search',
    'airmozilla.comments',
    'airmozilla.uploads',
    'airmozilla.starred',
    'airmozilla.subtitles',
    'airmozilla.surveys',
    'airmozilla.roku',
    'airmozilla.cronlogger',
    'airmozilla.staticpages',
    'airmozilla.new',
    'airmozilla.popcorn',
    'airmozilla.chapters',
    'airmozilla.closedcaptions',

    'djcelery',
    'kombu.transport.django',
    'bootstrapform',
    'sorl.thumbnail',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.flatpages',  # this can be deleted later
    'cronjobs',
    'raven.contrib.django.raven_compat',
    'django_jinja',
    'django_nose',  # deliberately making this the last one
)

# Absolute path to the directory that holds media.
MEDIA_ROOT = path('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
STATIC_ROOT = path('static')

# URL prefix for static files
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Necessary so that test-utils doesn't try to execute some deprecated
# functionality on the database connection.
SQL_RESET_SEQUENCES = False

# We can use the simplest hasher because we never store usable passwords
# thanks to Persona.
PASSWORD_HASHERS = ('django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',)

# our session storage is all memcache so using it instead of FallbackStorage
# which uses CookieStorage by default so sessions are better
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# Note that this is different when running tests.
# You know in case you're debugging tests.
AUTHENTICATION_BACKENDS = (
    # '%s.authentication.backend.AirmozillaBrowserIDBackend' % PROJECT_MODULE,
    # but we're keeping this in case people still have sessions
    # whose backend cookie points to this class path
    # 'django_browserid.auth.BrowserIDBackend',
    'airmozilla.authentication.backend.AirmozillaOIDCAuthenticationBackend',
    # Needed because the tests
    # use self.client.login(username=..., password=...)
    'django.contrib.auth.backends.ModelBackend',
)

# Domains allowed for log in
ALLOWED_BID = (
    'mozilla.com',
    'mozillafoundation.org',
    'mozilla-japan.org',
    'getpocket.com',
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL_FAILURE = '/login-failure/'


_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'session_csrf.context_processor',
    'django.contrib.messages.context_processors.messages',

    'airmozilla.manage.context_processors.badges',
    'airmozilla.main.context_processors.base',
    'airmozilla.main.context_processors.nav_bar',
    'airmozilla.main.context_processors.search_form',
    'airmozilla.main.context_processors.sidebar',
    'airmozilla.main.context_processors.analytics',
    'airmozilla.main.context_processors.dev',
    'airmozilla.main.context_processors.browserid',
    'airmozilla.main.context_processors.faux_i18n',
    'airmozilla.main.context_processors.autocompeter',
    'airmozilla.main.context_processors.fanout',
    'airmozilla.starred.context_processors.stars',
)

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'APP_DIRS': True,
        'OPTIONS': {
            # Use jinja2/ for jinja templates
            'app_dirname': 'jinja2',
            # Don't figure out which template loader to use based on
            # file extension
            'match_extension': '',
            # 'newstyle_gettext': True,
            'context_processors': _CONTEXT_PROCESSORS,
            'debug': False,
            'undefined': 'jinja2.Undefined',
            'extensions': [
                'jinja2.ext.do',
                'jinja2.ext.loopcontrols',
                'jinja2.ext.with_',
                'jinja2.ext.i18n',  # needed to avoid errors in django_jinja
                'jinja2.ext.autoescape',
                'django_jinja.builtins.extensions.CsrfExtension',
                'django_jinja.builtins.extensions.StaticFilesExtension',
                'django_jinja.builtins.extensions.DjangoFiltersExtension',
                'pipeline.jinja2.PipelineExtension',
            ],
            'globals': {
                'browserid_info': 'django_browserid.helpers.browserid_info',
                'browserid_login': 'django_browserid.helpers.browserid_login',
                'browserid_logout': 'django_browserid.helpers.browserid_logout'
            }
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # what does this do?!
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': False,
            'context_processors': _CONTEXT_PROCESSORS,
        }
    },
]

# Always generate a CSRF token for anonymous users.
ANON_ALWAYS = True


# Remove localization middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mozilla_django_oidc.middleware.RefreshIDToken',
    'django.middleware.security.SecurityMiddleware',
    'session_csrf.CsrfMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
    # 'airmozilla.authentication.middleware.ValidateIDToken',
    'airmozilla.manage.middleware.CacheBustingMiddleware',
    'airmozilla.staticpages.middleware.StaticPageFallbackMiddleware',
)

X_FRAME_OPTIONS = 'DENY'

# Enable timezone support for Django TZ-aware datetime objects
# Times stored in the db as UTC; forms/templates as Pacific time
USE_TZ = True
TIME_ZONE = 'UTC'

# Configuration for live/archiving events treatment
# How much time, in minutes, an event shows as "live" before its start time.
LIVE_MARGIN = 10

# Default amount of time, in minutes, an event spends in the "archiving" state.
ARCHIVING_MARGIN = 60

# How many events in the past (and future) should the calendar system
# return.  E.g. if CALENDAR_SIZE=30, up to 60 events (half from the past
# and half from the future) will be output.
CALENDAR_SIZE = 30

# How many events should appear in the syndication feeds
FEED_SIZE = 20

# Number of upcoming events to display in the sidebar
UPCOMING_SIDEBAR_COUNT = 5

# Number of featured/trending events to display in the sidebar
FEATURED_SIDEBAR_COUNT = 5

# Number of trending events to display in the Roku feed
TRENDING_ROKU_COUNT = 20

# Use memcached for session storage with fallback on the database
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Always use secure cookies
COOKIES_SECURE = True

# URL to connect to ElasticSearch
ELASTICSEARCH_URL = 'http://localhost:9200/'

# Number of related events to display (max)
RELATED_CONTENT_SIZE = 4

# Boosting of title and tags, makes them matter more.
RELATED_CONTENT_BOOST_TITLE = 1.0
RELATED_CONTENT_BOOST_TAGS = -0.5

# Defaults for Mozillians
MOZILLIANS_API_BASE = 'https://mozillians.org'

# API base URL
VIDLY_BASE_URL = 'https://vid.ly'
VIDLY_API_URL = 'https://m.vid.ly/api/'

# Name of the default Channel
DEFAULT_CHANNEL_SLUG = 'main'
DEFAULT_CHANNEL_NAME = 'Main'

# Name of the default channel for Mozillians
MOZILLIANS_CHANNEL_SLUG = 'mozillians'
MOZILLIANS_CHANNEL_NAME = 'Mozillians'

# How often, maximum are approval pester emails sent
PESTER_INTERVAL_DAYS = 3  # days

# Where you put secure username+password combinations for example
URL_TRANSFORM_PASSWORDS = {}

# Bit.ly URL shortener access token
# See README about how to generate one
BITLY_ACCESS_TOKEN = None
BITLY_URL = 'https://api-ssl.bitly.com/v3/shorten'

# Overridden so we can depend on more complex checking
BROWSERID_VERIFY_CLASS = (
    '%s.authentication.views.CustomBrowserIDVerify' % PROJECT_MODULE
)
BROWSERID_REQUEST_ARGS = {'siteName': 'Air Mozilla'}

# Name of the bucket where you upload all large videos
S3_UPLOAD_BUCKET = 'air-mozilla-uploads'

# See http://amara.org/en/profiles/account/
# (THESE MIGHT BE OBSOLETE!)
AMARA_BASE_URL = 'https://www.amara.org/api2/partners'
AMARA_API_USERNAME = ''
AMARA_API_KEY = ''

# The new settings
AMARA_BASE_URL = 'https://amara.org'
AMARA_TEAM = 'mozilla'
AMARA_PROJECT = 'airmozilla'
AMARA_USERNAME = ''
AMARA_API_KEY = ''


SCRAPE_CREDENTIALS = {
    # ('username', 'password'): ['intranet.mozilla.org'],
}

# If true, every search is logged and recorded
LOG_SEARCHES = True

try:
    # ujson is a much faster json serializer
    # We tell the django-jsonview decorator to use it only if the ujson
    # package is installed and can be imported
    import ujson  # NOQA
    JSON_MODULE = 'ujson'
    JSON_USE_DJANGO_SERIALIZER = False
except ImportError:
    pass


# When extracting screen captures, how many do we want to extract
# for each video. This number is static independent of the length
# of the video.
SCREENCAPTURES_NO_PICTURES = 12

# Name of the directory that gets created in the temp directory
# that we fill with screencaps, and that gets later picked up
# by another job that imports the JPEGs created there.
SCREENCAPTURES_TEMP_DIRECTORY_NAME = 'airmozilla-screencaps'


# Usernames of people who have contributed to Air Mozilla (as a contributor).
# This list is ordered! Ordered by the first contributor first, and the most
# recent contributor last.
# These usernames must exist in the
# https://mozillians.org/en-US/group/air-mozilla-contributors/ group.
CONTRIBUTORS = (
    'onceuponatimeforever',
    'bugZPDX',
    'lcamacho',
    'quentinp',
    'leo',
    'koddsson',
    'KrystalYu',
    'anuragchaudhury',
    'gloriadwomoh',
    'a-buck',
    'anjalymehla',
    'julian.alexander.murillo',
)

# Override this if you want to run the selenium based tests
RUN_SELENIUM_TESTS = False


# When enabled, together with DEBUG==True, by visiting /god-mode/ you
# can become anybody.
# This is a good tool for doing testing without doing any Persona auth.
GOD_MODE = False


# If you want to disable all of the browser ID stuff, set this to True.
# That means you won't be able to sign in at all. Or sign out.
BROWSERID_DISABLED = False


# How many times to try sending out an event tweet.
MAX_TWEET_ATTEMPTS = 3


# Where do we store jobs for the celery message queue
BROKER_URL = 'django://'

CELERY_ALWAYS_EAGER = False

BROKER_CONNECTION_TIMEOUT = 0.1
CELERYD_CONCURRENCY = 2
CELERY_IGNORE_RESULT = True


THUMBNAIL_BACKEND = 'optisorl.backend.OptimizingThumbnailBackend'


# This turns of the thumbnail optimizer using pngquant so it's
# not used unless you explicitely turn it on.
PNGQUANT_LOCATION = None

# The user group where being a member means you get an email about
# all new event requests
NOTIFICATIONS_GROUP_NAME = 'Event Notifications'


# Adding prefix to airmozilla events index
ELASTICSEARCH_PREFIX = 'airmozilla'
ELASTICSEARCH_INDEX = 'events'

# legacy junk in settings/local.py on production deployments
BASE_PASSWORD_HASHERS = HMAC_KEYS = []

YOUTUBE_API_KEY = None

# You have to run `npm install` for this to be installed in `./node_modules`
PIPELINE = {
    'STYLESHEETS': PIPELINE_CSS,
    'JAVASCRIPT': PIPELINE_JS,
    'JS_COMPRESSOR': 'pipeline.compressors.uglifyjs.UglifyJSCompressor',
    'UGLIFYJS_BINARY': path('node_modules/.bin/uglifyjs'),
    'UGLIFYJS_ARGUMENTS': '--mangle',
    'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CSSMinCompressor',
    'CSSMIN_BINARY': path('node_modules/.bin/cssmin'),
    # Don't wrap javascript code in... `(...code...)();`
    # because possibly much code has been built with the assumption that
    # things will be made available globally.
    'DISABLE_WRAPPER': True,
    # The pipeline.jinja2.PipelineExtension extension doesn't support
    # automatically rendering any potentional compilation errors into
    # the rendered HTML, so just let it raise plain python exceptions.
    'SHOW_ERRORS_INLINE': False,
}

POPCORN_EDITOR_CDN_URL = "//d2edlhmcxlovf.cloudfront.net"

# Fanout.io account defaults for a realm.
FANOUT_REALM_ID = FANOUT_REALM_KEY = None


# Content Security Policies
CSP_DEFAULT_SRC = (
    "'self'",
)
CSP_FONT_SRC = (
    "'self'",
    'data:',
    'air.cdn.mozilla.net',
    'cdn.jsdelivr.net',
    'ssl.p.jwpcdn.com',
)
CSP_IMG_SRC = (
    "'self'",
    'data:',
    'vid.ly',
    'air.cdn.mozilla.net',
    'secure.gravatar.com',
    'jwpltx.com',  # used by JWPlayer
    'ssl.google-analytics.com',
    'mozillians.org',
    'https://i0.wp.com',  # used by mozillians.org
)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",  # needed for video templates
    "'unsafe-eval'",    # needed for hls.js
    'cdn.jsdelivr.net',
    'air.cdn.mozilla.net',
    'vid.ly',
    's.vid.ly',
    'cf.cdn.vid.ly',
    'ssl.p.jwpcdn.com',  # Where vidly hosts the JWPlayer
    'ssl.google-analytics.com',
    'd132d9vcg4o0oh.cloudfront.net',  # vid.ly's jwplayer.js
)
CSP_CONNECT_SRC = (
    "'self'",
    'vid.ly',
    'mozillalives-i.akamaihd.net',
    'autocompeter.com',
)
CSP_MEDIA_SRC = (
    "'self'",
    'blob:',
    'vid.ly',
    'mozillalives-i.akamaihd.net'
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    'air.cdn.mozilla.net',
)
CSP_CHILD_SRC = (
    "'self'",
    'blob:',
    'vid.ly',
    'www.youtube-nocookie.com',
    'login.persona.org',
)

# See https://bugzilla.mozilla.org/show_bug.cgi?id=1310807
SECURE_HSTS_SECONDS = 31536000

# See
# https://wiki.mozilla.org/Security/Guidelines/Web_Security#X-XSS-Protection
# Sets the 'X-XSS-Protection' header to '1; mode=block'
SECURE_BROWSER_XSS_FILTER = True

# See
# https://wiki.mozilla.org/Security/Guidelines/Web_Security#X-Content-Type-Options  # noqa
SECURE_CONTENT_TYPE_NOSNIFF = True


REV_CLIENT_API_KEY = ''
REV_USER_API_KEY = ''
REV_BASE_URL = 'https://www.rev.com'

AUTH0_DOMAIN = 'auth.mozilla.auth0.com'
AUTH0_CLIENT_ID = 'YOU_CLIENT_ID'
AUTH0_SECRET = 'YOUR_SECRET'
AUTH0_CALLBACK_URL = 'https://air.mozilla.org/authentication/callback/'
AUTH0_SUCCESS_URL = '/?logged=in'
AUTH0_PATIENCE_TIMEOUT = 5  # seconds

AUTH_SIGNOUT_URL = 'https://air.mozilla.org/?logged=out'

# This is the number of seconds that define how often we check the
# logged in users' id_token (if they have one).
# If this number is too low, too many requests on this site are blocked
# on talking to Auth0. If it's too high, we're not being secure enough.
RENEW_ID_TOKEN_EXPIRY_SECONDS = 60 * 15  # 15 min

VIDLY_VIDEO_URL_FORMAT = 'https://vid.ly/{}?content=video&format=webm'
VIDLY_POSTER_URL_FORMAT = 'https://vid.ly/{}/poster'


# In settings/__init__.py, if these aren't set they can be populated
# from other variables like AUTH0_* which was the old way.
OIDC_RP_CLIENT_ID = None
OIDC_RP_CLIENT_SECRET = None

OIDC_OP_AUTHORIZATION_ENDPOINT = None
OIDC_OP_TOKEN_ENDPOINT = None
OIDC_OP_USER_ENDPOINT = None

LOGIN_REDIRECT_URL = None
LOGOUT_REDIRECT_URL = None


# Set to false because we will manually control this because we need
# to set the profile carefully.
OIDC_CREATE_USER = False
