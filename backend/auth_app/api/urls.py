from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegistrationView, LoginView


urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),

    # path('logout/, ')
]