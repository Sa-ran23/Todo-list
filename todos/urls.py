from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_todo, name='add_todo'),
    path('edit/<int:pk>/', views.edit_todo, name='edit_todo'),
    path('delete/<int:pk>/', views.delete_todo, name='delete_todo'),
    path('toggle/<int:pk>/', views.toggle_todo, name='toggle_todo'),
    path('search/', views.search_todos, name='search_todos'),
]
