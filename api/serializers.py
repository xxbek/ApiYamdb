from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Title, Genre, Category, Review, Comments

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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "name",
            "slug",
        )


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField(slug_field='slug', queryset=Category.objects.all(), required=False)
    genre = GenreField(slug_field='slug', queryset=Genre.objects.all(), many=True)
    rating = serializers.IntegerField(required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username", many=False
    )

    def validate(self, attrs):
        author = (self.context["request"].user.id,)
        title = self.context["view"].kwargs.get("title_id")
        message = "Author review already exist"
        if (
            not self.instance
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError(message)
        return attrs

    class Meta:
        model = Review
        fields = ["id", "text", "author", "score", "pub_date"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username', many=False)

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date', 'review']
        model = Comments
