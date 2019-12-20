from django.urls import path
from . import views

urlpatterns = [
    path('data', views.UserView.as_view()),
    path('userank', views.UserRankView.as_view()),
    path('conrank', views.ConRankView.as_view()),
]
