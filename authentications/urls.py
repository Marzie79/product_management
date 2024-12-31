from django.urls import path

from authentications.views import (
    LogoutView, AuthenticationView, RefreshTokenView)

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('authentication/', AuthenticationView.as_view(), name='authentication'),
]
