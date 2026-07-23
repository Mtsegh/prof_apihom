from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<slug:slug>/', views.book_detail, name='book_detail'),
]