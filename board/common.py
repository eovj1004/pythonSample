from django.conf import settings
from django.core.paginator import Paginator
from email.mime.text import MIMEText
import hashlib
import smtplib


def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('test')
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return simple_middleware


def get_board_data(data_list, page_index):
    """
    pagination 処理

    @param request: list of model object
    @param page_index: ページ番号
    @return: 表示されるデータのlist
    """

    # Pagenation Object
    obj_page = Paginator(data_list, settings.BOARD_VIEW_SIZE)
    # 表示されるデータ
    result_data = None

    # データの件数が0の場合サイズ0のlistをreturnする
    if obj_page.count == 0:
        return []
    else:
        # 表示されるページのデータを結果として代入
        result_data = obj_page.page(page_index)

    return result_data


def str_to_bool(str_value):
    '''
    convert string to boolean
    '''
    return str_value.lower() in settings.STR_TRUE_LIST


def send_mail(mail_addr):
    '''
    email 発送
    '''
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('cdhmailtest@gmail.com', 'mailtest1')
    msg = MIMEText(settings.STR_MAIL_CONTENT)
    msg['Subject'] = settings.STR_MAIL_TITLE
    s.sendmail("no_reply@unknown.com", mail_addr, msg.as_string())
    s.quit()
