from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:thesis_id>/', views.thesis),
    path('<int:thesis_id>/<int:stance>/', views.stance),
    path('result/', views.evaluation),
]
