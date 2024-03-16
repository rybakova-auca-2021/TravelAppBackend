from rest_framework import generics, permissions, status, viewsets
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework import serializers
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile, PopularPlace, MustVisitPlace, Tour, SavedPlace, Place
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from .serializers import PopularPlaceSerializer, EditProfileSerializer, EditUserProfileSerializer, UserSerializer, UserSerializerSignUp, UserSerializerLogin, NewPasswordSerializer, PasswordResetSerializer, CodeVerificationSerializer, UserProfileSerializer, MustVisitPlaceSerializer, TourSerializer, SavedPlaceSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication


VERIFICATION_CODE = "2207"

place_id_param = openapi.Parameter(
    'place_id',
    openapi.IN_QUERY,
    description="ID of the place to save",
    type=openapi.TYPE_INTEGER
)

def get_user_by_username(username):
    return User.objects.filter(username=username).first()

def get_user_by_email(email):
    return User.objects.filter(email=email).first()

def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    return str(access), str(refresh)


class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerSignUp
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        user = serializer.instance
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)

        return Response({
            "message": "User created successfully",
            "user_id": user.id,
            "access_token": str(access),
            "refresh_token": str(refresh),
        }, status=status.HTTP_201_CREATED)

# views.py
class UserLoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializerLogin

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = UserSerializerLogin(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)

            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)

            return Response({
                "message": "Successfully logged in",
                "user_id": user.id,
                "access_token": str(access),
                "refresh_token": str(refresh),
            })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class PasswordResetView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetSerializer

    def send_verification_code(self, email, verification_code):
        try:
            subject = 'Verification Code'
            message = f'Your verification code is: {verification_code}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return True
        except Exception as e:
            return False

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = get_user_by_email(email)

        if user:
            verification_code = VERIFICATION_CODE 
            if self.send_verification_code(email, verification_code):
                return Response({"message": "Verification code sent successfully"})
            else:
                return Response({"error": "Failed to send verification code"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "User not found for the provided email"}, status=status.HTTP_404_NOT_FOUND)

class UserLogoutView(APIView):
    permission_classes = []

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class CodeVerificationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CodeVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = CodeVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verification_code = serializer.validated_data['verification_code']
        email = serializer.validated_data['email']

        user = User.objects.filter(email=email).first()

        if user:
            saved_verification_code = "2207"
            if verification_code == saved_verification_code:
                return Response({"message": "Verification successful. Proceed with password reset"})
            else:
                return Response({"error": "Incorrect verification code"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User not found for the provided user ID"}, status=status.HTTP_404_NOT_FOUND)

class CreareNewPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = NewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        new_password = serializer.validated_data['new_password']

        user = User.objects.filter(email=email).first()

        if user:
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successfully"})
        else:
            return Response({"error": "User not found for the provided mobile number"}, status=status.HTTP_404_NOT_FOUND)            

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserSerializer(user, context={'request': request})  

        serialized_data = {
            **serializer.data,
        }

        return Response(serialized_data)

class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        user_serializer = EditProfileSerializer(user, data=request.data, partial=True)
        user_profile_serializer = EditUserProfileSerializer(user_profile, data=request.data, partial=True)

        if user_serializer.is_valid() and user_profile_serializer.is_valid():
            user_serializer.save()
            user_profile_serializer.save()
            return Response({**user_serializer.data, **user_profile_serializer.data})
        
        errors = {}
        if not user_serializer.is_valid():
            errors.update(user_serializer.errors)

        if not user_profile_serializer.is_valid():
            errors.update(user_profile_serializer.errors)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)




class EditProfilePhoto(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def patch(self, request, *args, **kwargs):
        user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            profile_photo = request.data.get('profile_photo')
            if profile_photo:
                user_profile.profile_photo = profile_photo
                user_profile.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PopularPlacesView(APIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return PopularPlace.objects.all()

    def get(self, request):
        popular_places = self.get_queryset()
        serializer = PopularPlaceSerializer(popular_places, many=True) 
        return Response(serializer.data)


class MustVisitPlacesView(APIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return MustVisitPlace.objects.all()

    def get(self, request):
        popular_places = self.get_queryset()
        serializer = MustVisitPlaceSerializer(popular_places, many=True) 
        return Response(serializer.data)        

class TourPlacesView(APIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return Tour.objects.all()

    def get(self, request):
        popular_places = self.get_queryset()
        serializer = TourSerializer(popular_places, many=True) 
        return Response(serializer.data)

class PopularPlaceDetailsById(RetrieveAPIView):
    queryset = PopularPlace.objects.all()
    serializer_class = PopularPlaceSerializer 

    def get_object(self):
        place_id = self.kwargs['place_id']
        return get_object_or_404(self.queryset, id=place_id)

class MustVisitPlaceDetailsById(RetrieveAPIView):
    queryset = MustVisitPlace.objects.all()
    serializer_class = MustVisitPlaceSerializer 

    def get_object(self):
        place_id = self.kwargs['place_id']
        return get_object_or_404(self.queryset, id=place_id)


class PackagesDetailsById(RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer 

    def get_object(self):
        place_id = self.kwargs['place_id']
        return get_object_or_404(self.queryset, id=place_id)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SavePlaceView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'place_id',
                openapi.IN_QUERY,
                description="ID of the place to save",
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def post(self, request):
        place_id = request.query_params.get('place_id') 
        if not place_id:
            return Response({"error": "Place ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        place = get_object_or_404(Place, id=place_id)

        saved_place_data = {
            'user': request.user.pk,
            'name': place.name,
            'description': place.description,
            'main_image': place.main_image,
        }
        serializer = SavedPlaceSerializer(data=saved_place_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SavedPlacesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saved_places = SavedPlace.objects.filter(user=request.user)
        serializer = SavedPlaceSerializer(saved_places, many=True)
        return Response(serializer.data)