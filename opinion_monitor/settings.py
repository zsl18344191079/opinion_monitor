"""
Django settings for opinion_monitor project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'low*$4mdq*nbv$b$(#=$w8e69e@o4xer11=q3b$h54*x3m&pvj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # django-allauth必须安装的app
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 第三方账号相关，根据需求添加
    'allauth.socialaccount.providers.weibo',
    'allauth.socialaccount.providers.github',
    # Django模板语言样式库
    'widget_tweaks',
    # restful
    'rest_framework',
    # 模型
    'Myaccount.apps.MyaccountConfig',
    'MBlog.apps.MblogConfig',
    'monitor.apps.MonitorConfig',
]

# django-allauth相关设置
AUTHENTICATION_BACKENDS = (
    # django admin所使用的用户登录与django-allauth无关
    'django.contrib.auth.backends.ModelBackend',
    # allauth 身份验证
    'allauth.account.auth_backends.AuthenticationBackend',
)

# app django.contrib.sites需要的设置
SITE_ID = 1
# 指定要使用的登录方法(用户名、电子邮件地址两者之一)
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
# smtp 服务器地址
EMAIL_HOST = "smtp.qq.com"
# 要求用户注册时必须填写email
ACCOUNT_EMAIL_REQUIRED = True
# 注册成功后，会发送一封验证邮件，用户必须验证邮箱后，才能登陆
ACCOUNT_EMAIL_VERIFICATION = "optional"
# 邮箱确认邮件的截止日期(天数)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
# 更改为True，用户一旦确认他们的电子邮件地址，就会自动登录
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
# 登录或注册后自动跳转到/accounts/profile/
LOGIN_REDIRECT_URL = '/accounts/profile/'
# 默认端口25，若请求超时可尝试465
EMAIL_PORT = 465
# 用户名
EMAIL_HOST_USER = "1434317359@qq.com"
# 邮箱代理授权码（不是邮箱密码）
EMAIL_HOST_PASSWORD = "afdddmhlalgdjfhh"
# 是否使用了SSL 或者TLS（两者选其一）
# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
# 发送人
EMAIL_FROM = "1434317359@qq.com"  #
# 默认显示的发送人，（邮箱地址必须与发送人一致），不设置的话django默认使用的webmaster@localhost
DEFAULT_FROM_EMAIL = "微博與情 <1434317359@qq.com>"

# 如果使用自定义用户model user，为了让 Django 能够识别自定义的用户模型，必须在此处添加app.自定义表名
AUTH_USER_MODEL = 'Myaccount.User'
# ___________________________________________________________________________________________________________________________________

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'opinion_monitor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'DIRS': ['wb_opinion/dist'],
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

WSGI_APPLICATION = 'opinion_monitor.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'microblog',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'wb_opinion/dist')]


# 媒体文件专属参数设置（需要加url识别才能访问）
MEDIA_URL = "/media/"  # 媒体文件别名(相对路径) 和 绝对路径

# 存放上传的文件
MEDIA_ROOT = (
    os.path.join(BASE_DIR, 'media')
)
