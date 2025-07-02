import os
from pathlib import Path
import environ

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'your-secret-key-here'),
    EMAIL_HOST=(str, 'smtp.gmail.com'),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
    EMAIL_HOST_USER=(str, ''),
    EMAIL_HOST_PASSWORD=(str, ''),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'crispy_bootstrap5',
    
    # Local apps
    'core',
    'news',
    'events',
    'contact',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pranteey_yuva.urls'

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

WSGI_APPLICATION = 'pranteey_yuva.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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
LANGUAGE_CODE = 'hi'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEditor Configuration
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': '100%',
        'removePlugins': '',
        'allowedContent': True,
        'extraAllowedContent': '*(*);*{*}',
    },
    'admin': {
        'toolbar': [
            ['Source', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
            ['Find', 'Replace', '-', 'SelectAll', '-', 'Scayt'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField'],
            '/',
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe'],
            '/',
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks']
        ],
        'height': 500,
        'width': '100%',
        'removePlugins': '',
        'allowedContent': True,
        'extraAllowedContent': '*(*);*{*}',
        'extraPlugins': 'colordialog,colorbutton',
        'colorButton_enableMore': True,
        'colorButton_enableAutomatic': True,
        'colorButton_colors': '000,800000,8B4513,2F4F4F,008080,000080,4B0082,696969,' +
                             'B22222,A52A2A,DAA520,006400,40E0D0,0000CD,800080,808080,' +
                             'F00,FF8C00,FFD700,008000,0FF,00F,EE82EE,A9A9A9,' +
                             'FFA07A,FFA500,FFFF00,00FF00,AFEEEE,ADD8E6,DDA0DD,D3D3D3,' +
                             'FFF0F5,FAEBD7,FFFFE0,F0FFF0,F0FFFF,F0F8FF,E6E6FA,FFF,' +
                             'FF69B4,DC143C,FF1493,FF6347,FF4500,FFA500,FFD700,ADFF2F,' +
                             '32CD32,00FF7F,00CED1,1E90FF,9370DB,BA55D3,FF20DD,F0E68C',
        'format_tags': 'p;h1;h2;h3;h4;h5;h6;pre;address;div',
        'entities': False,
        'removeDialogTabs': '',
        'stylesSet': [
            {'name': 'Marker: Yellow', 'element': 'span', 'styles': {'background-color': 'Yellow'}},
            {'name': 'Marker: Green', 'element': 'span', 'styles': {'background-color': 'Lime'}},
            {'name': 'Marker: Pink', 'element': 'span', 'styles': {'background-color': 'HotPink'}},
            {'name': 'Marker: Blue', 'element': 'span', 'styles': {'background-color': 'LightBlue'}},
            {'name': 'Red Text', 'element': 'span', 'styles': {'color': 'Red'}},
            {'name': 'Blue Text', 'element': 'span', 'styles': {'color': 'Blue'}},
            {'name': 'Green Text', 'element': 'span', 'styles': {'color': 'Green'}},
            {'name': 'Orange Text', 'element': 'span', 'styles': {'color': 'Orange'}},
            {'name': 'Big', 'element': 'big'},
            {'name': 'Small', 'element': 'small'},
            {'name': 'Computer Code', 'element': 'code'},
            {'name': 'Keyboard Phrase', 'element': 'kbd'},
            {'name': 'Sample Text', 'element': 'samp'},
            {'name': 'Variable', 'element': 'var'},
            {'name': 'Deleted Text', 'element': 'del'},
            {'name': 'Inserted Text', 'element': 'ins'},
            {'name': 'Cited Work', 'element': 'cite'},
            {'name': 'Inline Quotation', 'element': 'q'},
        ],
    }
}

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF Settings for Replit
CSRF_TRUSTED_ORIGINS = [
    'https://*.replit.dev',
    'https://*.replit.co',
    'https://*.replit.app',
]

# Messages Framework
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
