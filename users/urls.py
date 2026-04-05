from django.urls import path
from .views import RegisterView, UserListView, UserDetailView, MeView

urlpatterns = [
    path('register/',  RegisterView.as_view(),    name='user-register'),
    path('me/',        MeView.as_view(),           name='user-me'),
    path('',           UserListView.as_view(),     name='user-list'),
    path('<int:pk>/',  UserDetailView.as_view(),   name='user-detail'),
]