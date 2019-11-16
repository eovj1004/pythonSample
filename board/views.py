from board import common
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import logging


logger = logging.getLogger(__name__)


def index(request):
    """
    index page

    @param request: Request Object
    @return: view(index page)
    """
    return render(request, 'board/index.html')


def sendMail(request):
    """
    index page からメールアドレスを作成して送信する時
    メールを発送する

    @param request: Request Object
    @return: メール発送結果
    """
    context = {}
    if request.method == 'POST':
        logger.debug('メール送信')
        try:
            email = request.POST.get('email', '')
            # mail addressが空白の場合エラー
            if email == '':
                raise Exception('メアド空白')

            common.send_mail(email)
            context['result'] = settings.PROC_RESULT['SUCCESS']
        except Exception as e:
            logger.error(e)
            context['result'] = settings.PROC_RESULT['FAIL']

        return JsonResponse(context)


def handler404(request, *args, **argv):
    '''
    404エラーが発生した時の処理

    @param request: Request Object
    @return: 404エラーページ
    '''
    logger.debug('404エラー：%s' % request.path)
    response = render(request, "404.html", {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    '''
    500エラーが発生した時の処理

    @param request: Request Object
    @return: 500エラーページ
    '''
    logger.debug('500エラー：%s' % request.path)
    response = render(request, "500.html", {})
    response.status_code = 500
    return response
