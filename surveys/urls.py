from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/thesis/<int:thesis_no>/',
         views.thesis_detail,
         name='thesis_detail'),
    path('<slug:slug>/thesis/<int:thesis_no>/stance/<int:stance_id>/',
         views.stance_detail,
         name='stance_detail'),
    path('<slug:slug>/result/', views.result_index, name='result_index'),
    path('<slug:slug>/generate_pdf/', views.theses_pdf, name='theses_pdf'),
]
