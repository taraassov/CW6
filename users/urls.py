from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, VerifyView, UserUpdateView, generate_new_password, \
    UserListView, deactivate_user, activate_user

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<str:token>/', VerifyView.as_view(), name='verify'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('user_view/', UserListView.as_view(), name='user_view'),
    path('deactivate_user/<int:pk>/', deactivate_user, name='deactivate_user'),
    path('activate_user/<int:pk>/', activate_user, name='activate_user'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
