from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConformationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    conformation_code = serializers.CharField(required=True)
