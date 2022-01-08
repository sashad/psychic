from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sessionData', views.sessionData, name='sessionData'),
    path('history', views.history, name='history'),
    path('guesses', views.guesses, name='guesses'),
]

