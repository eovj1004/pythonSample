from board import views
from board.smplBoard import views as board_views
from board.user import views as user_views
from django.conf import settings
from django.conf.urls import handler400, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from board.scraping import views as scraping_views


handler400 = 'board.views.handler404'
handler404 = 'board.views.handler404'
handler500 = 'board.views.handler500'


# Media file
urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('sendMail', views.sendMail),
]

# user
urlpatterns += [
    path('user/regist', user_views.regist),
    path('user/loginProcess', user_views.loginProcess),
    path('user/logout', user_views.logout),
]

# board
urlpatterns += [
    path('smplBoard/list', board_views.boardList),
    path('smplBoard/registForm', board_views.registForm),
    path('smplBoard/insert', board_views.boardInsert),
    path('smplBoard/update', board_views.boardUpdate),
    path('smplBoard/view', board_views.boardView),
    path('smplBoard/checkPassword', board_views.checkPassword),
    path('smplBoard/insertComment', board_views.insertComment),
    path('smplBoard/removeComment', board_views.removeComment),
    path('smplBoard/modifyComment', board_views.modifyComment),
]

# image
urlpatterns += [
    path('image/upload', board_views.imageUpload),
    path('image/delete', board_views.imageDelete),
]


# scraping
urlpatterns += [
    path('scraping/yahoo', scraping_views.getYahooNews),
    path('scraping/getNews', scraping_views.getNewsContent),
    path('scraping/detail', scraping_views.getDetailContent),

]