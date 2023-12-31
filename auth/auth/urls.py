from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from authApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # Token-related views
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User-related views
    path('api/signup/', views.UserSignupView.as_view(), name='user_signup'),
    path('api/login/', views.UserLoginView.as_view(), name='user_login'),
    path('api/password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('api/verify-code/', views.CodeVerificationView.as_view(), name='verify-code'),
    path('api/create-new-password/', views.CreareNewPasswordView.as_view(), name='verify-code'),
]

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')
urlpatterns += router.urls
