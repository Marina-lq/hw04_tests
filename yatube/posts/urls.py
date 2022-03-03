# posts/urls.py.py
from django.urls import path

from . import views

app_name = 'post'


urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    # Профайл пользователя
    path('profile/<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # Создание нового поста
    path('create/', views.post_create, name='post_create'),
    # Редактирование поста
    path('posts/<post_id>/edit/', views.post_edit, name='edit'),
]
