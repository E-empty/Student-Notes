from django.contrib import admin
from django.urls import path, include
from . import views


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
]
