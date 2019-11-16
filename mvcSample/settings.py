import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=*pi4@j+^$j8fo*_j8zs7dmv$d_+n_h(!l_&5!715gw5&0+vq5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


CHECK_URL_LIST = [
    '/user/logout',
    '/smplBoard/list',
    '/smplBoard/registForm',
    '/smplBoard/insert',
    '/smplBoard/view',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'board',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'board.middleware.sess_chk_middleware.FilterIPMiddleware',
]

ROOT_URLCONF = 'mvcSample.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', BASE_DIR + 'templates'],
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

WSGI_APPLICATION = 'mvcSample.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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


# logger 設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'format1': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'format2': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'handlers': {
        # 로그 파일을 만들어 텍스트로 로그레코드 저장
        'views': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs') + '/debug.log',
            'formatter': 'format1',
        },
        'board_views': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs') + '/smplBoard_debug.log',
            'formatter': 'format1',
        },
        'user_views': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs') + '/user_debug.log',
            'formatter': 'format1',
        },
    },

    # 로거
    # 로그 레코드 저장소
    # 로거를 이름별로 정의
    'loggers': {
        'board.views': {
            'handlers': ['views'],
            'level': 'DEBUG',
        },
        'board.smplBoard.views': {
            'handlers': ['board_views'],
            'level': 'DEBUG',
        },
        'board.user.views': {
            'handlers': ['user_views'],
            'level': 'DEBUG',
        },
    },

}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


# Media file (Upload File)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
FROALA_ROOT = os.path.join(MEDIA_ROOT, 'froala')


# CONSTANT VALUE
# Result
PROC_RESULT = {
    'SUCCESS': 1000,
    'FAIL': -1,
    'DUPLICATE': -1000
}

# 表示されるBoardのデータ件数
BOARD_VIEW_SIZE = 10

# Boolean Data
STR_TRUE_LIST = ['1', 'true']

# メールのタイトル
STR_MAIL_TITLE = 'チェのサンプルウェブサイトからのメールです。'

# メールの本文
STR_MAIL_CONTENT = '''お疲れ様です。チェデホと申します。
ソースコードを見ていただいてありがとうございます。
以前何回も面接が終わってから自分で作ったソースコードが見たいと言われたことがあって
簡単なサイトを作成してみました。

まだ足りない実力だと思っていますがPMのポジションで活躍することに目指して
ずっと勉強しながら頑張っています。

経歴はまだ短いんですが、結構人力が足りなかった会社でPLのポジションで２件のプロジェクト経験と
一人で要件定義からリリースまで完了したプロジェクトも２件あります。
その後要件さえあれば開発ができなくて大変だったことは１回もありません。

もっと上に目指して開発レベルを高めたいと思っています。
宜しくお願い致します。

チェ　デホ'''
