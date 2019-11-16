from django.db import models
import datetime


class UploadFileModel(models.Model):
    '''
    File Uploadに使われるオブジェクト

    Usage :
    # import form.py > UploadFileForm class 
    form = UploadFileForm(request.POST, request.FILES)
	if form.is_valid():
		form.save()
    '''
    title = models.TextField(default='')
    file = models.FileField(null=True)


class User(models.Model):
    '''サイト利用者'''

    # ユーザー ID
    user_id = models.CharField(max_length=15)
    # パスワード
    password = models.CharField(max_length=64)
    # ユーザー登録画面でアップロードしたファイル
    picture = models.FileField(null=True)
    # 削除可否
    is_deleted = models.BooleanField(default=False)


class Board(models.Model):
    '''Board'''

    # 作成者
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # タイトル
    title = models.CharField(max_length=100)
    # 内容
    content = models.CharField(max_length=5000)
    # 非公開可否
    is_secret = models.BooleanField(default=False)
    # パスワード
    password = models.CharField(null=True, 	max_length=64)
    # 作成年月日
    write_date = models.DateTimeField(auto_now_add=True)
    # 修正年月日
    modify_date = models.DateTimeField(auto_now_add=True)
    # 削除可否
    is_deleted = models.BooleanField(default=False)


class Comment(models.Model):
    '''Comment'''

    # fk Board
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    # fk User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 作成日
    write_date = models.DateTimeField(auto_now_add=True)
    # 内容
    content = models.CharField(max_length=5000)
    # 上位コメントのid
    parent_id = models.IntegerField()
    # 1階層可否
    is_parent = models.BooleanField(default=False)
