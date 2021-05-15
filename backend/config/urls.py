from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CryptoTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        return token


class CryptoTokenObtainPairView(TokenObtainPairView):
    serializer_class = CryptoTokenObtainPairSerializer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login', CryptoTokenObtainPairView.as_view(), name='login_token_obtain_pair'),
    path('accounts/token/fresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/arbitrage/', include('bitcoin_arbitrage.urls', namespace='bitcoin_arbitrage')),
    path('api/handlers/',include('crypto_bot.urls',namespace='apis_handler'))
]
