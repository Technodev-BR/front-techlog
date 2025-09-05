from pathlib import Path
from decouple import config, Csv
from dj_database_url import parse as db_url
import urllib
import environ
import os


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY" , "Chave")

DEBUG = config("DEBUG", cast=bool, default=False)

env = environ.Env(DEBUG = (bool,False))

environ.Env.DB_SCHEMES['postgres'] = 'django.db.backends.postgresql'

DEFAULT_DATABASE = os.environ.get('DATABASE_DEFAULT', "db.sqlite3")

DEFULT_DATABASE_URL = f'sqlite:///{urllib.parse.quote(str(BASE_DIR / DEFAULT_DATABASE))}'

DATABASE_URL = os.environ.get('DATABASE_URL', DEFULT_DATABASE_URL)

os.environ['DJANGO_DATABASE_URL'] =  DATABASE_URL.format(**os.environ)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "phonenumber_field",
    "jquery",
    "bootstrap5",
    "fontawesomefree",
    'dbbackup',
    "controllers.clientes",
    "controllers.operacoes",
    "controllers.iscas",
    "controllers.locais",
    "controllers.locais_clientes",
    "controllers.fornecedores",
    "controllers.solicitacoes",
    "controllers.checklists",
    "controllers.rastreamentos",
    "controllers.usuarios",
    "controllers.usuarios_operacoes",
    "controllers.login",
]

AUTHENTICATION_BACKENDS = [
    "controllers.login.authenticated.AuthenticatedBackend",
    "django.contrib.auth.backends.ModelBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "controllers.clientes.context_clientes.context_clientes",
                "controllers.fornecedores.context_fornecedores.context_fornecedores",
                "controllers.locais.context_locais.context_locais",
                "controllers.locais_clientes.context_locais_clientes.context_locais_clientes",
                "controllers.operacoes.context_operacoes.context_operacoes",
                "controllers.usuarios.context_usuarios.context_usuarios",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

DATABASES = {
        'default': env.db('DJANGO_DATABASE_URL', default=DEFULT_DATABASE_URL) 
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "pt-BR"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'

DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'backups')} 

STATIC_URL = "/assets/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "assets"),)

STATIC_ROOT = os.path.join("static")

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_HTTPONLY = True

# SESSION_COOKIE_SECURE = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_AGE = 180 * 60

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

CSRF_COOKIE_HTTPONL = True

CSRF_USE_SESSIONS = True

CSRF_TRUSTED_ORIGINS = ['https://localhost:5000','http://localhost:5000','https://181.215.134.63:5000','https://techlog.technodevbr.com'] 

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp-mail.outlook.com'

EMAIL_HOST_USER = "na@estaoderiscos.com.br"

EMAIL_HOST_PASSWORD = "a"

MEDIA_URL = "/uploads/"

MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "/"