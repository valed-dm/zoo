from django.contrib.auth.views import LoginView as LoginViewContrib
from django.contrib.auth.views import LogoutView as LogoutViewContrib
from django.views.generic import CreateView

from .forms import RegisterForm
from .models import MyUser


class RegisterView(CreateView):
    model = MyUser
    # fields = "__all__"
    form_class = RegisterForm
    template_name = "userapp/myuser_form.html"
    success_url = "/login/"


class LoginView(LoginViewContrib):
    template_name = "userapp/login.html"

    # user = self.request.user


class LogoutView(LogoutViewContrib):
    pass
