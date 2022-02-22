from django.urls import path
from . import views


urlpatterns = [
    path('api/notice/<str:department>', views.notice, name='notice'),
    path('api/start/<str:department>', views.start, name='start'),
    path('api/give_csrf', views.give_csrf, name='give_csrf'),
    path('api/stop/<str:department>', views.stop, name='stop'),
    path('api/start_otk/<str:department>', views.start_otk, name='start_otk'),
    path('api/stop_otk/<str:department>', views.stop_otk, name='stop_otk'),
    path('api/back/<str:department>', views.back, name='back'),
    path('api/end/<str:department>', views.end, name='end'),
    path('api/qr/<int:id>/<str:model>', views.give_qr, name='give_qr'),
    path('api/end_otk/<str:department>', views.end_otk, name='end_otk'),
]