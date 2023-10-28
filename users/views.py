import random

from django.conf import settings
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView, ListView

from users.forms import UserRegisterForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('client:main_page')
    template_name = 'users/register.html'

    def form_valid(self, form):
        # Сохраняем объект пользователя
        response = super().form_valid(form)
        # Отправляем пользователю электронное письмо с подтверждением
        user = form.save(commit=False)
        token = user.generate_verification_token()
        user.save()
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Для подтверждения регистрации на сайте перейдите по ссылке: {self.request.build_absolute_uri(reverse_lazy("users:verify", kwargs={"token": token}))}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return response


class VerifyView(TemplateView):
    template_name = 'users/verify.html'

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            user = User.objects.get(verification_token=token)
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect('client:main_page')
        except User.DoesNotExist:
            return HttpResponseBadRequest('Invalid verification token')


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
    )
    user = request.user
    user.set_password(new_password)
    user.save()
    login(request, user)
    return redirect(reverse('users:profile'))


# class UserListView(LoginRequiredMixin, ListView):
#     model = User
#     fields = ('title', 'content')
#     extra_context = {
#         'title': 'Пользователи'
#     }

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = get_user_model()
    fields = ('title', 'content')
    extra_context = {
        'title': 'Пользователи'
    }
    success_url = reverse_lazy('client:main_page')

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = get_user_model().objects.all()
        return context


def deactivate_user(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()
    return redirect('users:user_view')


def activate_user(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    return redirect('users:user_view')
