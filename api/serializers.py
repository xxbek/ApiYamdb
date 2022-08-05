from rest_framework import serializers


class EmailSerializer(serializers.models):
    class Meta:
        fields = ['email']
