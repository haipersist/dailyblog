# -*- coding: utf-8 -*-

import os
import djcelery

djcelery.setup_loader()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SAE_APPKEY = '5n530w1n50'
SAE_SECRETKEY = 'm5k5lyjx4hh30k3zyxi4ymyz4xlkmmhkhxxkkzwy'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gna^*4u41q+qu1mi1rnb&rsv2--o&3f)8yu997ty!nqoq@k4(7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


PASSWORD_RESET_TIMEOUT_DAYS = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.blog',
    'apps.comment',
    'apps.account',
    'apps.dashboard',
    'apps.trip',
    'apps.job',
    'rest_framework',
    'djcelery',
    'ckeditor',
    'ckeditor_uploader',
    #'django_celery_results',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE':5,
     'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

MIDDLEWARE_CLASSES = [
    #middleware, a framework of hooks into Django’s request/response processing
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.blog.middleware.LoadTimeMiddleware',
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
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'dailyblog.wsgi.application'

ADMIN_MEDIA_PREFIX = '/static/admin/'

ALLOWED_HOSTS = ['localhost',
                 '10.13.27.47',
                 '192.168.1.9',
                 '127.0.0.1',
		         'www.hbnnforever.cn',
		         'hbnnforever.cn',
		         '101.200.63.158',
		         '172.17.64.119',
                 ]



DB_NAME = 'app_dailyblog'
MYSQL_USER = 'root'
MYSQL_PWD =  'admin'
MYSQL_PORT = ''
MYSQL_HOST = ''



DOMAIN = 'http://hbnnforever.cn/'

#DOMAIN = 'http://10.13.27.47/'


STATIC_CLOUD_STORE = 'http://blog-1251509264.costj.myqcloud.com/'



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
STATIC_ROOT = (os.path.join(BASE_DIR, 'static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))


CKEDITOR_UPLOAD_PATH = 'ckeditor/uploads/'
#CKEDITOR_JQUERY_URL = '/static/jquery/jquery-2.1.3.min.js'
CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_CONFIGS = {
    'default': {
         'toolbar': (
			['div','codesnippet','Source','-','Save','NewPage','Preview','-','Templates'],
			['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print','SpellChecker','Scayt'],
			['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
			['Form','Checkbox','Radio','TextField','Textarea','Select','Button', 'ImageButton','HiddenField'],
			['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
			['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
			['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
			['Link','Unlink','Anchor'],
			['Image','CodeSnippet','HorizontalRule','Table','Smiley','SpecialChar','PageBreak'],
			['Styles','Format','Font','FontSize'],
			['TextColor','BGColor'],
			['Maximize','ShowBlocks','-','About', 'pbckcode'],
		),
        'toolbarGroups' : [
            { 'name': 'clipboard',   'groups': [ 'clipboard', 'undo' ] },
            { 'name': 'editing',     'groups': [ 'find', 'selection', 'spellchecker' ] },
            { 'name': 'links' },
            { 'name': 'insert' },
            { 'name': 'forms' },
            { 'name': 'tools' },
            { 'name': 'document',       'groups': [ 'mode', 'document', 'doctools' ] },
            { 'name': 'others' },
            '/',
            { 'name': 'basicstyles', 'groups': [ 'basicstyles', 'cleanup' ] },
            { 'name': 'paragraph',   'groups': [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
            { 'name': 'styles' },
            { 'name': 'colors' },
            { 'name': 'about' },
        ],
        'width' : 660,
        'removeButtons' : 'Underline,Subscript,Superscript',
        'format_tags' : 'p;h1;h2;h3;pre',
        'removeDialogTabs' : 'image:advanced;link:advanced',
        'tabSpaces':4,
        'extraPlugins' :','.join([
            'div',
            'clipboard',
            'dialog',
            'dialogui',
            'sourcedialog',
            'widget',
            'lineutils',
            'codesnippet',
            ]
        ),
        'allowedContent' : True,
    },
}



NUM_PER_PAGE = 10



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
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
    'redis': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6739',
        'options': {
            'MAX_ENTRIES': 1024,
            'CLIENT_CLASS':'redis_cache.client.DefaultClient',
        }
    },
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_PASSWORD = 'nanaNANA320'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = 'hbnnlong@163.com'
EMAIL_SUBJECT_PREFIX = u'海波'
#EMAIL_USE_TLS = True                  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

#CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'


