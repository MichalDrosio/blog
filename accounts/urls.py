
from django.urls import path

from accounts.views import login_user, register_user, user_logout, edit_user

app_name = 'accounts'


urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', user_logout, name='logout'),
    path('edit/', edit_user, name='edit_user'),


]