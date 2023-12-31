from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

MIN_LENGTH = 8


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        min_length=MIN_LENGTH,
        error_messages={
            "min_length": f"Password must be longer than {MIN_LENGTH} characters."
        }
    )
    password_confirm = serializers.CharField(
        write_only=True,
        min_length=MIN_LENGTH,
        error_messages={
            "min_length": f"Password must be longer than {MIN_LENGTH} characters."
        }
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password_confirm", None)

        user = User.objects.create(
            username=validated_data["email"],
            email=validated_data["email"],
        )

        user.set_password(password)
        user.save()

        return user
