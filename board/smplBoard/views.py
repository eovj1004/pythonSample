import logging
import os

from board import common
from board.models import Board
from board.models import Comment
from board.models import User
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render


logger = logging.getLogger(__name__)


def boardList(request):
    """
    Sample Board List

    @param request: Request Object
    @return: View and List Of Board Data
    """
    logger.debug('Call boardList')

    page_index = None
    try:
        page_index = int(request.GET.get("page_index", 1))
    except Exception as e:
        page_index = 1

    logger.debug('page_index:%d' % page_index)

    try:
        objects = Board.objects.filter(is_deleted=False).order_by('-id')
        board_list = common.get_board_data(objects, page_index)
        idx_top = len(objects) - (page_index - 1) * settings.BOARD_VIEW_SIZE
        context = {
            'page_data': board_list,
            'idx_top': idx_top
        }

        return render(request, "board/smplBoard/list.html", context)
    except Exception as e:
        logger.error(e)


def registForm(request):
    """
    投稿画面に遷移

    @param request: Request Object
    @return: view(投稿ページ)
    """
    logger.debug('Call registForm')

    board = Board()
    context = {}
    if request.method == 'GET':
        board_id = request.GET.get('board_id', '')
        if board_id != '':
            logger.debug('投稿修正画面\nboard_id:%s' % board_id)
            try:
                board = Board.objects.get(id=int(board_id))
                context['board'] = board
            except Exception as e:
                pass
        else:
            logger.debug('投稿作成画面')
    else:
        pass

    return render(request, 'board/smplBoard/form.html', context)


def imageUpload(request):
    '''
    Froala Editor イメージ登録

    @param request: Request Object
    @return: アップロードされた画像のURL
    '''
    logger.debug('Call imageUpload')

    if request.method == 'POST':

        if 'file' in request.FILES:
            the_file = request.FILES['file']
            allowed_types = [
                'image/jpeg',
                'image/jpg',
                'image/pjpeg',
                'image/x-png',
                'image/png'
            ]
            if not the_file.content_type in allowed_types:
                return JsonResponse({'error': _('You can only upload images.')})
            # Other data on the request.FILES dictionary:
            # filesize = len(file['content'])
            # filetype = file['content-type']

            path = default_storage.save('froala/', the_file)

            link = request.build_absolute_uri(default_storage.url(path))
            logger.debug('投稿内容の画像アップロード\npath : ' % path)

            # return JsonResponse({'link': link})
            return JsonResponse({'link': link})
        else:
            logger.error('imege upload 失敗')
            raise
    else:
        logger.error('request method => "GET", POSTにしなさい。')
        raise


def imageDelete(request):
    '''
    Froala Editor イメージ削除

    @param request: Request Object
    @return: 削除結果
    '''
    logger.debug('Call imageDelete')

    context = {}

    if request.method == 'POST':
        src = request.POST.get('src', '').split('/')
        os.path.join(settings.FROALA_ROOT, src[len(src) - 1])
        os.remove(os.path.join(settings.FROALA_ROOT, src[len(src) - 1]))
        context["result"] = settings.PROC_RESULT['SUCCESS']
    else:
        logger.error('imege 削除失敗、request methodおPOSTにしなさい。')
        context["result"] = settings.PROC_RESULT['FAIL']

    return JsonResponse()


def boardInsert(request):
    '''
    投稿した内容をデータベースに保存する

    @param request: Request Object
    @return: Sample Board List画面
    '''
    logger.debug('Call boardInsert')
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '')
            is_secret = request.POST.get('is_secret', '')
            password = request.POST.get('password', '')
            content = request.POST.get('content', '')
            logger.debug('\ntitle:{0}\nis_secret:{1}\npassword:{2}\ncontent:{3}'.format(
                title, is_secret, password, content))

            user_pk = int(request.session.get('login_user', '0'))
            user = User.objects.get(id=user_pk)

            board = Board()
            board.user = user
            board.title = title
            board.is_secret = common.str_to_bool(is_secret)
            board.content = content

            logger.debug('投稿データ登録完了')

            # 非公開の場合パスワードセット
            if board.is_secret:
                board.password = password

            board.save()
        except Exception as e:
            logger.debug('投稿データ登録失敗')
            raise

    return redirect('/smplBoard/list')


def boardUpdate(request):
    '''
    投稿したデータの修正

    @param request: Request Object
    @return: 修正後List画面にredirect
    '''
    logger.debug('Call boardUpdate')

    if request.method == 'POST':
        try:
            board_id = int(request.POST.get('board_id', '0'))
            title = request.POST.get('title', '')
            is_secret = request.POST.get('is_secret', '0')
            password = request.POST.get('password', '')
            content = request.POST.get('content', '')

            logger.debug(
                '\nboard_id:{0}\ntitle:{1}\nis_secret:{2}\npassword:{3}\ncontent:{4}'.format(
                    board_id, title, is_secret, password, content))

            obj_board = Board.objects.get(id=board_id)
            obj_board.title = title
            obj_board.is_secret = common.str_to_bool(is_secret)
            obj_board.password = password
            obj_board.content = content
            obj_board.save()
            logger.debug('投稿データ修正\ntitle:%s' % title)

        except Exception as e:
            logger.debug('投稿データ修正エラー\nエラーメッセージ:%s' % e)
            raise

        return redirect('/smplBoard/list')


def boardView(request):
    '''
    simple boardの詳細画面

    @param request: Request Object
    @return: Sample Board 詳細画面
    '''
    logger.debug('Call boardView')
    context = {}
    if request.method == 'GET':
        try:
            board_id = int(request.GET.get('board_id', 0))
            logger.debug('board_id:%d' % board_id)

            obj_board = Board.objects.get(id=board_id)
            comment_list = Comment.objects.filter(
                board=obj_board).order_by('parent_id', '-is_parent', '-write_date')
            login_user = int(request.session.get('login_user', '0'))

            context['comment_list'] = comment_list
            # 自分の投稿
            if obj_board.user.id == login_user:
                context['modify_flag'] = True
            # 他人の投稿
            else:
                # 非公開投稿
                if obj_board.is_secret:
                    input_pw = request.GET.get('password', '')
                    # パスワード不一致はエラー
                    if obj_board.password != input_pw:

                        raise Exception('非公開投稿パスワード不一致')

            context['board'] = obj_board
            logger.debug('投稿照会\n投稿ID：%d' % obj_board.id)
        except Exception as e:
            logger.error('投稿照会失敗\nエラーメッセージ：%s' % e)
            raise
    return render(request, "board/smplBoard/view.html", context)


def checkPassword(request):
    '''
    他人の非公開投稿を照会する時パスワードを確認する

    @param request: Request Object
    @return: パスワード確認結果
    '''
    logger.debug('Call checkPassword')
    context = {}

    if request.method == 'POST':
        board_id = request.POST.get('board_id', '0')
        input_pw = request.POST.get('input_pw', '')

        obj_board = Board.objects.filter(id=board_id, password=input_pw)
        logger.debug('board_id：{0}\ninput_pw：{1}'.format(
            board_id, input_pw))

        if len(obj_board) == 1:
            logger.debug('パスワード一致')
            context['result'] = settings.PROC_RESULT['SUCCESS']
        else:
            logger.debug('パスワード不一致')
            context['result'] = settings.PROC_RESULT['FAIL']
    else:
        context['result'] = settings.PROC_RESULT['FAIL']

    return JsonResponse(context)


def insertComment(request):
    '''
    入力commentをデータベースに保存する

    @param request: Request Object
    @return: パスワード確認結果
    '''
    logger.debug('Call insertComment')
    context = {}

    if request.method == 'POST':
        try:
            comment = request.POST.get('comment', '')
            board_id = int(request.POST.get('board_id', '0'))
            user_id = int(request.session.get('login_user', '0'))
            parent_id = int(request.POST.get('parent_id', '0'))

            logger.debug('comment{0}\nboard_id：{1}\nuser_id：{2}\nparent_id：{3}'.format(
                comment, board_id, user_id, parent_id))

            # 空白のコメント、IDが指定されてないリクエストはエラーにする
            if comment == '' or board_id == 0:
                raise

            obj_comment = Comment()
            obj_comment.content = comment
            obj_comment.board = Board.objects.get(id=board_id)
            obj_comment.user = User.objects.get(id=user_id)
            obj_comment.parent_id = parent_id
            obj_comment.save()
            logger.debug('データベースインサート完了')

            if parent_id == 0:
                obj_comment.parent_id = obj_comment.id
                obj_comment.is_parent = True
                obj_comment.save()
                logger.debug('1depth comment アップデート完了')

            context['result'] = settings.PROC_RESULT['SUCCESS']
        except Exception as e:
            context['result'] = settings.PROC_RESULT['FAIL']
    else:
        context['result'] = settings.PROC_RESULT['FAIL']
    return JsonResponse(context)


def modifyComment(request):
    '''
    コメントを修正する

    @param request: Request Object
    @return: コメントの修正結果
    '''
    logger.debug('Call modifyComment')
    context = {}
    if request.method == 'POST':
        try:
            comment_id = int(request.POST.get('comment_id', '0'))
            comment = request.POST.get('comment', '')
            logger.debug('comment_id{0}\ncomment：{1}'.format(
                comment_id, comment))
            # 空白のコメント、IDが指定されてないリクエストはエラーにする
            if comment == '' or comment_id == 0:
                raise Exception('parameter error')

            obj_comment = Comment.objects.get(id=comment_id)
            obj_comment.content = comment
            obj_comment.save()

            context['result'] = settings.PROC_RESULT['SUCCESS']
        except Exception as e:
            logger.error('エラーメッセージ：%s' % e)

            context['result'] = settings.PROC_RESULT['FAIL']
    else:
        context['result'] = settings.PROC_RESULT['FAIL']
    return JsonResponse(context)


def removeComment(request):
    '''
    コメントを削除する

    @param request: Request Object
    @return: コメントの削除結果
    '''
    logger.debug('Call removeComment')

    context = {}
    if request.method == 'POST':
        try:
            comment_id = int(request.POST.get('comment_id', '0'))
            logger.debug('comment_id:%d' % comment_id)

            # IDが指定されてないリクエストはエラーにする
            if comment_id == 0:
                raise Exception('parameter error')

            obj_comment = Comment.objects.get(id=comment_id)

            # 一階層のコメントの場合下位コメントも全部削除する
            if obj_comment.id == obj_comment.parent_id:
                comment_list = Comment.objects.filter(parent_id=obj_comment.id)
                for item in comment_list:
                    item.delete()

            obj_comment.delete()
            context['result'] = settings.PROC_RESULT['SUCCESS']
        except Exception as e:
            logger.debug('エラーメッセージ：%s' % e)
            context['result'] = settings.PROC_RESULT['FAIL']
    else:
        context['result'] = settings.PROC_RESULT['FAIL']
    return JsonResponse(context)
