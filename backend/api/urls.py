from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.router.router import router
from .views import UserRegisterView


userpatterns = [
    path("user/register/", UserRegisterView.as_view()),
    path("user/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += userpatterns
