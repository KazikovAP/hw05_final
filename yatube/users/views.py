from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:interests')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
