from django.urls import path
from . import views


urlpatterns = [
    path('api/notice/<str:department>', views.notice, name='notice'),
    path('api/qr_start/<str:department>', views.qr_start, name='qr_start'),
    path('api/give_csrf', views.give_csrf, name='give_csrf'),
    path('api/stop/<str:department>', views.stop, name='stop'),
    path('api/qr_start_otk/<str:department>', views.qr_start_otk, name='qr_start_otk'),
    path('api/stop_otk/<str:department>', views.stop_otk, name='stop_otk'),
    path('api/back/<str:department>', views.back, name='back'),
    path('api/end/<str:department>', views.end, name='end'),
    path('api/qr/<int:id>/<str:model>', views.give_qr, name='give_qr'),
]