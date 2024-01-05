from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"}, required=True
    )
    password_confirm = serializers.CharField(
        write_only=True, style={"input_type": "password"}, required=True
    )
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "password_confirm"]

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                data["user"] = user
            else:
                raise serializers.ValidationError(
                    "Login failed with provided credentials."
                )
        else:
            raise serializers.ValidationError("username and password is required")

        return data

    class Meta:
        model = User
        fields = ["username", "password"]
