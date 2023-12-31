from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from sendsms.message import SmsMessage
from rest_framework import serializers
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings


VERIFICATION_CODE = "2207"

def get_user_by_username(username):
    return User.objects.filter(username=username).first()

def get_user_by_email(email):
    return User.objects.filter(email=email).first()

def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    return str(access), str(refresh)


class NewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "min_length": f"Password must be longer than {8} characters."
        }
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "min_length": f"Password must be longer than {8} characters."
        }
    )
    email = serializers.CharField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField()

class CodeVerificationSerializer(serializers.Serializer):
    verification_code = serializers.CharField()
    email = serializers.CharField()

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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



class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
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


class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

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


class CodeVerificationView(APIView):
    permission_classes = [permissions.AllowAny]

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

        user = User.objects.filter(email = email).first()

        if user:
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successfully"})
        else:
            return Response({"error": "User not found for the provided mobile number"}, status=status.HTTP_404_NOT_FOUND)            



class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer