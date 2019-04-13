from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('thesis/<int:thesis_id>/stance/<int:stance>/',
         views.stance, name='stance'),
    path('thesis/<int:thesis_id>/', views.thesis, name='thesis'),
    path('result/', views.evaluation, name='result'),
]
