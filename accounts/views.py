from django.conf import settings
from django.contrib.auth import logout, login
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, DetailView, RedirectView, CreateView, TemplateView, ListView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin

from accounts.forms import SighUpForm
from accounts.models import User
from films.models import Film
from hobby import urls


class SignUpView(FormView):
    def get(self, request, *args, **kwargs):
        form = SighUpForm()

        return render(request, 'accounts/signup.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = SighUpForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                name = form.cleaned_data['full_name']
                user = User.objects.create(
                    username=username,
                    password=password,
                    name=name)
                user.set_password(password)
                user.save()
                return HttpResponseRedirect(reverse_lazy('accounts:login'))

        return HttpResponseRedirect(reverse_lazy('home'))


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


class AddToFav(RedirectView):
    url = reverse_lazy('accounts:profile')

    def get(self, request, *args, **kwargs):
        movie_id = self.kwargs['movie_id']
        film = Film.objects.get(imdbId=movie_id)
        self.request.user.fav_list.add(film)
        self.request.user.save()
        return super(AddToFav, self).get(request, *args, **kwargs)



class ProfileView(DetailView):
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        print(urls.urlpatterns)
        user = User.objects.get(username=self.request.user.username)
        return user


class FindPeopleView(FormMixin, ListView):
    template_name = 'accounts/find_people.html'

    def post(self, request, *args, **kwargs):
        query = self.request.POST['query']
        results = User.objects.filter(name__contains=query)
        return render(request, self.template_name, {'results': results})

