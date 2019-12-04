from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('screen', views.condition_screen, name="screen"),
    path('rank', views.ranking_list, name="rank"),
]