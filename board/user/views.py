import logging

from board import common
from board.models import User
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect


logger = logging.getLogger(__name__)


def regist(request):
    """
    ユーザー登録の処理

    @param request: Request Object
    @return: 登録完了後indexページに redirect 
    """
    logger.debug('Call regist')

    user = User()
    response_data = {}

    if request.method == 'POST':
        try:
            user_id = request.POST['id']
            pw = request.POST['pw']
            logger.debug('\nuser_id:{0}\npw:{1}'.format(user_id, '*******'))

            user = User.objects.filter(user_id=user_id)
            if len(user) == 1:
                response_data['result'] = settings.PROC_RESULT['DUPLICATE']
                return JsonResponse(response_data)

            # password encrypt sha256
            pw = common.encrypt_string(pw)

            user = User()
            user.user_id = user_id
            user.password = pw
            user.picture = request.FILES['picture']

            user.save()
        except Exception as e:
            raise
    response_data['result'] = settings.PROC_RESULT['SUCCESS']
    return JsonResponse(response_data)
    # return redirect('/', msg='登録が完了されました。')


def loginProcess(request):
    """
    Login処理プロセス

    @param request: Request Object
    @return: Login 処理結果の Json Object 
    """
    logger.debug('Call loginProcess')
    if request.method == 'POST':
        try:
            user_id = request.POST.get('id')
            pw = common.encrypt_string(request.POST.get('pw'))

            logger.debug('\nuser_id:{0}\npw:{1}'.format(user_id, '*******'))

            user = User.objects.filter(user_id=user_id, password=pw)

            if len(user) == 1:
                request.session['login_user'] = user[0].id

                response_data = {}
                response_data['result'] = settings.PROC_RESULT['SUCCESS']
                logger.debug('ログイン完了')

                return JsonResponse(response_data)

            else:
                response_data = {}
                response_data['result'] = settings.PROC_RESULT['FAIL']
                logger.debug('ログイン失敗')
                return JsonResponse(response_data)
        except Exception as e:
            logger.error('エラーメッセージ：%s' % e)
            raise
        
    else:
        raise


def logout(request):
    """
    セッションからログイン情報削除

    @param request: Request Object
    @return: logout情報削除後indexページに redirect 
    """
    logger.debug('Call logout')
    request.session['login_user'] = None
    return redirect('/')
