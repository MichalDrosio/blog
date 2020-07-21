from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import login_user, register_user

app_name = 'accounts'


urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]