from django.core.exceptions import PermissionDenied	
from mvcSample import settings
from board.models import User


class FilterIPMiddleware(object):
	"""
	ログインセッション情報を確認する
	"""
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):

		# ログインが必要なページ
		if request.path in settings.CHECK_URL_LIST :
			if request.session.get("login_user") is not None :
				response = self.get_response(request)
			else:
				raise
		# ログインが要らないページ
		else :
			# ログインしたのか確認
			response = self.get_response(request)
			
		return response
		