from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=5,
        style={"input_type": "password"},
        help_text="Password user (minimum 5 characters)",
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
        )
        read_only_fields = (
            "id",
            "is_staff"
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
