from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConformationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    conformation_code = serializers.CharField(required=True)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'bio', 'email', 'role']
