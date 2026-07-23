from django.urls import path
from . import views

app_name = 'research'

urlpatterns = [
    path('', views.research_list, name='research_list'),
    path('teaching/', views.teaching_list, name='teaching_list'),
]