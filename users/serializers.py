from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from tasks.serializers import TaskFormatResSerializer


class UserSerializer(serializers.ModelSerializer):
    tasks = TaskFormatResSerializer(many=True, required=False)

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if "password" in validated_data:
            instance.set_password(validated_data["password"])

        instance.save()

        return instance

    class Meta:
        model = User
        fields = ["id", "username", "password", "profile", "tasks"]
        read_only_fields = ["id", "tasks"]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ]
            },
        }
