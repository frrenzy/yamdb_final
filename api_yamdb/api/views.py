from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyMixin
from api.permissions import ContentPermission, IsAdmin, IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleWriteSerializer,
    UserSerializer,
    UserSignupSerializer,
)
from api.utils import code_generator, send_mail
from reviews.models import Category, Genre, Review, Title, User


class AuthViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = (permissions.AllowAny,)

    @action(detail=False, methods=['post'], url_path='signup')
    def signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        confirmation_code = code_generator.make_code(user)
        send_mail(
            'Confirm your email',
            (
                f'Confirm your email to obtain personal access token. '
                f'Your confirmation_code: {confirmation_code}'
            ),
            to=[user.email],
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers,
        )

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @action(detail=False, methods=['post'], url_path='token')
    def get_jwt(self, request, *args, **kwargs):
        try:
            username = request.data['username']
        except KeyError:
            return Response(
                {'username': 'missing'}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            confirmation_code = request.data['confirmation_code']
        except KeyError:
            return Response(
                {'confirmation_code': 'missing'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(User, username=username)
        if code_generator.check_code(user, confirmation_code):
            return Response({'token': str(AccessToken.for_user(user))})
        return Response(
            {'confirmation_code': 'invalid'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
        'trace',
    ]

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleWriteSerializer
        return TitleSerializer


class GenreViewSet(
    ListCreateDestroyMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class CategoryViewSet(
    ListCreateDestroyMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ContentPermission,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
        'trace',
    ]

    def create(self, request, *args, **kwargs):
        if not request.data.get('username'):
            return Response(
                {'username': 'required field'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not request.data.get('email'):
            return Response(
                {'email': 'required field'}, status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)


class MeViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'patch']

    @action(detail=False, methods=['get', 'patch'], url_path='')
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            instance = request.user
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        if request.data.get('role'):
            return Response(
                {'role': 'you can not change your role'},
                status=status.HTTP_403_FORBIDDEN,
            )

        instance = request.user
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ContentPermission,)
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
        'trace',
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)
