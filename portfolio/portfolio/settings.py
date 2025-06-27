import os
from pathlib import Path
from decouple import config
from django.templatetags.static import static
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    # Django Unfold Admin (must be before django.contrib.admin)
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',
    'unfold.contrib.import_export',
    
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'ckeditor',
    'ckeditor_uploader',
    'taggit',
    
    # Local apps
    'main',
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

ROOT_URLCONF = 'portfolio.urls'

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

WSGI_APPLICATION = 'portfolio.wsgi.application'

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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Callback functions for UNFOLD
def environment_callback(request):
    """Callback to show environment info in admin"""
    return ["Development", "success"] if DEBUG else ["Production", "danger"]

def dashboard_callback(request, context):
    """Callback for dashboard statistics"""
    try:
        from main.models import Project, BlogPost, Certificate, ContactMessage
        
        # Get statistics
        total_projects = Project.objects.count()
        active_projects = Project.objects.filter(is_featured=True).count()
        
        total_posts = BlogPost.objects.count()
        published_posts = BlogPost.objects.filter(status='published').count()
        
        total_certificates = Certificate.objects.count()
        
        total_messages = ContactMessage.objects.count()
        unread_messages = ContactMessage.objects.filter(is_read=False).count()
        
        context.update({
            "total_projects": total_projects,
            "active_projects": active_projects,
            "total_posts": total_posts,
            "published_posts": published_posts,
            "total_certificates": total_certificates,
            "total_messages": total_messages,
            "unread_messages": unread_messages,
            "dashboard_cards": [
                {
                    "title": "Projects",
                    "metric": total_projects,
                    "footer": f"Featured: {active_projects}",
                    "chart": "📊",
                },
                {
                    "title": "Blog Posts", 
                    "metric": total_posts,
                    "footer": f"Published: {published_posts}",
                    "chart": "📝",
                },
                {
                    "title": "Certificates",
                    "metric": total_certificates, 
                    "footer": "Professional certifications",
                    "chart": "🏆",
                },
                {
                    "title": "Messages",
                    "metric": total_messages,
                    "footer": f"Unread: {unread_messages}",
                    "chart": "💬",
                },
            ]
        })
        return context
    except Exception as e:
        # Return empty dictionary if models aren't ready
        return context # Or an empty dictionary: return {}

# Django Unfold Admin Configuration
UNFOLD = {
    "SITE_TITLE": "Portfolio Admin",
    "SITE_HEADER": "Portfolio Administration",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("images/logo-light.png"),
        "dark": lambda request: static("images/logo-dark.png"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("images/logo-light.png"),
        "dark": lambda request: static("images/logo-dark.png"),
    },
    "SITE_SYMBOL": "speed",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "portfolio.settings.environment_callback",
    "DASHBOARD_CALLBACK": "portfolio.settings.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("images/login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),
    },
    "STYLES": [
        lambda request: static("css/admin-custom.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/admin-custom.js"),
    ],
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255", 
            "200": "233 213 255",
            "300": "196 181 253",
            "400": "147 51 234",
            "500": "147 51 234",
            "600": "124 58 237",
            "700": "109 40 217",
            "800": "91 33 182",
            "900": "76 29 149",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇺🇸",
                "fr": "🇫🇷",
                "nl": "🇳🇱",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Navigation",
                "separator": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "Portfolio",
                "separator": True,
                "items": [
                    {
                        "title": "Profile",
                        "icon": "person",
                        "link": reverse_lazy("admin:main_profile_changelist"),
                    },
                    {
                        "title": "Projects",
                        "icon": "work",
                        "link": reverse_lazy("admin:main_project_changelist"),
                    },
                    {
                        "title": "Skills",
                        "icon": "psychology",
                        "link": reverse_lazy("admin:main_skill_changelist"),
                    },
                    {
                        "title": "Certificates",
                        "icon": "school",
                        "link": reverse_lazy("admin:main_certificate_changelist"),
                    },
                ],
            },
            {
                "title": "Blog",
                "separator": True,
                "items": [
                    {
                        "title": "Posts",
                        "icon": "article",
                        "link": reverse_lazy("admin:main_blogpost_changelist"),
                    },
                    {
                        "title": "Categories",
                        "icon": "category",
                        "link": reverse_lazy("admin:main_blogcategory_changelist"),
                    },
                ],
            },
            {
                "title": "Contact",
                "separator": True,
                "items": [
                    {
                        "title": "Messages",
                        "icon": "mail",
                        "link": reverse_lazy("admin:main_contactmessage_changelist"),
                    },
                ],
            },
        ],
    },
}

# CKEditor Configuration
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'extraPlugins': ','.join([
            'uploadimage',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    },
}

# Email Configuration (for contact form)
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@yourportfolio.com')
