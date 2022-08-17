from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register()

urlpatterns = [
    path('auth/email/', views.send_email),
    path('auth/token/', views.ObtainToken.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
