from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from authApp import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Travel App",
      default_version='v1',
      description="API for Travel App",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourdomain.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup/', views.UserSignupView.as_view(), name='user_signup'),
    path('auth/login/', views.UserLoginView.as_view(), name='user_login'),
    path('auth/password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('auth/verify-code/', views.CodeVerificationView.as_view(), name='verify-code'),
    path('auth/create-new-password/', views.CreareNewPasswordView.as_view(), name='create-new-password'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit-profile'),
    path('profile_photo/edit/', views.EditProfilePhoto.as_view(), name='edit-profile-photo'),
    path('places/popular-places/', views.PopularPlacesView.as_view(), name='popular'),
    path('places/popular-places/<int:place_id>/', views.PopularPlaceDetailsById.as_view(), name='place-details-by-id'),
    path('places/must-visit-places/<int:place_id>/', views.MustVisitPlaceDetailsById.as_view(), name='place-details-by-id'),
    path('places/packages/<int:place_id>/', views.PackagesDetailsById.as_view(), name='place-details-by-id'),
    path('places/must-visit-places/', views.MustVisitPlacesView.as_view(), name='must-visit'),
    path('places/packages/', views.TourPlacesView.as_view(), name='package'),
    path('save-place/', views.SavePlaceView.as_view(), name='save_place'),
    path('saved-places/', views.SavedPlacesListView.as_view(), name='saved_places'),

    # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Define your router and register ViewSet
router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')
urlpatterns += router.urls
