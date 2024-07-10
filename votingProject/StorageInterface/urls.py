from django.shortcuts import redirect
from django.urls import path
from . import views

app_name = 'election'  # Define your app's namespace

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('vote/', views.vote, name='vote'),
    path('already_voted/', views.already_voted, name='already_voted'),
    path('results/', views.results, name='results'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('voters/', views.voters_list, name='voters_list'),
]
