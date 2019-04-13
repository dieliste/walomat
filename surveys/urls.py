from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:thesis_id>/', views.thesis, name='theses'),
    path('<int:thesis_id>/<int:stance>/', views.stance, name='stances'),
    path('result/', views.evaluation, name='result'),
]
