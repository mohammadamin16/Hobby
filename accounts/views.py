from django.contrib.auth import logout, login
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, DetailView, RedirectView

from django.contrib.auth.forms import AuthenticationForm

from accounts.models import User
from films.models import Film


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class AddToWatched(RedirectView):
    url = reverse_lazy('accounts:profile')

    def get(self, request, *args, **kwargs):
        movie_id = self.kwargs['movie_id']
        film = Film.objects.get(imdbId=movie_id)
        self.request.user.watched_films.add(film)
        self.request.user.save()
        return super(AddToWatched, self).get(request, *args, **kwargs)



class ProfileView(DetailView):
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        print("*************************TEST***********************")
        user = User.objects.get(username=self.request.user.username)
        print(user)
        return user
