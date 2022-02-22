from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('operator', views.operator, name='operator'),
    path('detal/<int:id>', views.detal, name='detal'),
    path('about', views.about, name='about'),
    path('abouttoo/<int:id>', views.abouttoo, name='abouttoo'),
    path('pin/<int:id>', views.pin, name='pin'),
    path('meeting', views.meeting, name='meeting'),
    path('contracts', views.contracts, name='contracts'),
]