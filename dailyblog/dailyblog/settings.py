# -*- coding: utf-8 -*-

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gna^*4u41q+qu1mi1rnb&rsv2--o&3f)8yu997ty!nqoq@k4(7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not os.environ.get("APP_NAME", "")

PASSWORD_RESET_TIMEOUT_DAYS = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'rest_framework'
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE':2,
     'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

MIDDLEWARE_CLASSES = [
    #middleware, a framework of hooks into Django’s request/response processing
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'blog.middleware.LoadTimeMiddware',
]

ROOT_URLCONF = 'dailyblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'dailyblog.wsgi.application'

ADMIN_MEDIA_PREFIX = '/static/admin/'

ALLOWED_HOSTS = ['localhost','127.0.0.1','dailyblog.applinzi.com']

if  DEBUG:
    DB_NAME = 'app_dailyblog'
    MYSQL_USER = 'root'
    MYSQL_PWD =  '*****'
    MYSQL_PORT = ''
    MYSQL_HOST = ''
    DOMAIN = 'http://localhost:8080'


else:
    import sae.const
    DB_NAME = sae.const.MYSQL_DB
    MYSQL_USER = sae.const.MYSQL_USER
    MYSQL_PWD = sae.const.MYSQL_PASS
    MYSQL_HOST = sae.const.MYSQL_HOST
    MYSQL_PORT = sae.const.MYSQL_PORT
    DOMAIN = 'http://dailyblog.applinzi.com'

DEBUG = True

DATABASES = {
    'default': {
    'NAME': DB_NAME,#数据库名称
    'ENGINE': 'django.db.backends.mysql',
    'USER':MYSQL_USER ,
    'PASSWORD':MYSQL_PWD,
    'PORT':MYSQL_PORT,
    'HOST':MYSQL_HOST,
},
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/


TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = (os.path.join(BASE_DIR, 'static'))

STATICFILES_FINDERS = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        )

STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)


NUM_PER_PAGE = 5



LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'filters': {
        #This filter will only pass on records when settings.DEBUG is False.
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        #定义日志输出格式
        'simple': {
            'format': '[%(levelname)s] %(module)s : %(message)s'
        },
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(message)s in %(filename)s %(levelno)s'
        }
    },

    'handlers': {

        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'   #它将打印 DEBUG （和更高级）的消息到stderr。这个handler 使用verbose输出格式。
        },
        'mail_admins': {
            #一个AdminEmailHandler，它将用邮件发送 ERROR （和更高级）的消息到站点管理员
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        }
    },
    'loggers': {
        '': {
            'handlers': [ 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            #传递所有DEBUG及以上的信息给文件和控制台
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            #传递所有ERROR信息给邮件和控制台
            #Log messages related to the handling of requests. 5XX responses are raised as ERROR messages;
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#Cache configuration
CACHE_TYPE='simple'
CACHE_DEFAULT_TIMEOUT=300
#CACHE_MEMCACHE_SERVER=

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
    'memcache': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sina.com'
EMAIL_HOST_PASSWORD = '****'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'qyqx_1314@sina.com'
EMAIL_SUBJECT_PREFIX = u'海波'
#EMAIL_USE_TLS = True                  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
