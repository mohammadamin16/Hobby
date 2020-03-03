from django.urls import path
from accounts import views

app_name = 'accounts'


urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('add-to-watched/<movie_id>', views.AddToWatched.as_view(), name='add-to-watched'),
]
