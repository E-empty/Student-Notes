from django.contrib import admin
from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('notes', views.notes, name='notes'),
    path('create_notes', views.create_note_view, name='create_notes'),
 #   path('notes_list', views.notes_list, name='notes_list'),
    path('notes_list/', views.notes_list, name='notes_list'),
    path('notes/<int:pk>/update', views.update_note_view, name='updateNote'),
    path('notes/<int:pk>/delete', views.delete_note_view, name='deleteNote'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:pk>/update/', views.group_update, name='group_update'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),
    path('groups_list/', views.group_list, name='group_list'),
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/delete_user/<int:user_id>/', views.remove_user_from_group, name='remove_user'),
]
