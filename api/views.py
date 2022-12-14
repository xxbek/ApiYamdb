from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import status, permissions, viewsets, filters, mixins
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, action
from .serializers import EmailSerializer, ConformationCodeSerializer, UsersSerializer, \
    TitleSerializer, GenreSerializer, CategorySerializer, ReviewSerializer, CommentSerializer
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Title, Genre, Category, Review, Comments
from .permissions import AdminOrReadOnly, ReadOnlyOrAuthor, ModeratorPermission, AdminPermission
from django.db.models import Avg
from api.filters import TitleFilter


User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_email(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    user, created = User.objects.get_or_create(email=email, username=email)
    conformation_code = default_token_generator.make_token(user)
    send_mail(
        'Yamdb access',
        f'Your conformation code is {conformation_code}',
        'from@example.com',
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
        )
    return Response('Your code is delivered')


class ObtainToken(APIView):
    permission_classes = [permissions.AllowAny, ]

    @staticmethod
    def post(request):
        serializer = ConformationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conformation_code = serializer.data.get('conformation_code')
        user_email = serializer.data.get('email')
        user = get_object_or_404(User, email=user_email)

        if default_token_generator.check_token(user, conformation_code):
            token = AccessToken.for_user(user)
            return Response(f'token: {token}', status=status.HTTP_200_OK)

        return Response('???????????????? conformation code', status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAdminUser, ]

    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['username', ]
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    @action(detail=False,
            methods=['GET', 'PATCH'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        if request.method == 'GET':
            serializer = UsersSerializer(user, many=False)
            return Response(data=serializer.data)

        elif request.method == 'PATCH':
            serializer = UsersSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg("reviews__score")).order_by('id')
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = [AdminOrReadOnly]
    pagination_class = PageNumberPagination
    serializer_class = TitleSerializer
    filterset_class = TitleFilter


class GenreAndCategoryMixin(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = [AdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenreViewSet(GenreAndCategoryMixin):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer


class CategoryViewSet(GenreAndCategoryMixin):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch']
    queryset = Review.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ReadOnlyOrAuthor | ModeratorPermission | AdminPermission]
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Review.objects.all()
        title = get_object_or_404(Title, pk=self.kwargs["title_id"])
        if title is not None:
            queryset = Review.objects.filter(title=self.kwargs.get("title_id"))
        return queryset.order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ReadOnlyOrAuthor | ModeratorPermission | AdminPermission]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        queryset = Comments.objects.filter(review=self.kwargs.get('review_id'))
        return queryset.order_by('id')

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)




