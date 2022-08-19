from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Title, Genre, Category

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


class TitleSerializerList(serializers.ModelSerializer):
    genre = serializers.ReadOnlyField(source='genre.name')
    category = serializers.ReadOnlyField(source='category.name')
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre', 'category']


class TitleSerializerGet(serializers.Serializer):
    titles_id = serializers.IntegerField(required=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ['id', 'text', 'author', 'scope', 'pub_date']
