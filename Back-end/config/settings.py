"""
Django settings for config project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# --- 1. CAMINHOS DO PROJETO ---
BASE_DIR = Path(__file__).resolve().parent.parent

# AQUI ESTÁ A MÁGICA: Apontamos para a pasta src do Front-end
FRONTEND_DIR = BASE_DIR.parent / 'Front-end' / 'src'

# Carrega variáveis de ambiente
load_dotenv(BASE_DIR / '.env')

# --- SEGURANÇA ---
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-chave-dev-padrao')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*'] 

# --- APLICATIVOS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'corsheaders',
    'rest_framework',
    
    'users',
    'core',
    'feed',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Importante para arquivos estáticos
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# --- 2. CONFIGURAÇÃO DOS HTMLS (TEMPLATES) ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Dizemos ao Django para buscar HTMLs na pasta do Front-end
        'DIRS': [FRONTEND_DIR], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- BANCO DE DADOS ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
database_url = os.getenv('DATABASE_URL')
if database_url:
    DATABASES['default'] = dj_database_url.parse(database_url, conn_max_age=600)

# --- VALIDAÇÃO DE SENHA ---
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Recife'
USE_I18N = True
USE_TZ = True

# --- 3. ARQUIVOS ESTÁTICOS (CSS, JS, IMAGENS) ---
STATIC_URL = 'static/'

# Onde o Django busca os arquivos estáticos durante o desenvolvimento
STATICFILES_DIRS = [
    FRONTEND_DIR,
]

# Onde o Django salva os arquivos para produção
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configurações de Mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configurações Extras
CORS_ALLOW_ALL_ORIGINS = True
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'users:login'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'