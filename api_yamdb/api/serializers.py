import re

from django.utils import timezone
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField

from users.models import User
from reviews.models import Category, Comment, Genre, Title, Review


class UserSignupSerializer(serializers.ModelSerializer):
    username_regex = re.compile(r'^[\w\.\@\-\+]+\Z')

    class Meta:
        fields = (
            'username',
            'email',
        )
        model = User
        extra_kwargs = {
            'username': {'required': True, 'validators': []},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if not self.username_regex.match(attrs['username']):
            raise serializers.ValidationError(
                'username does not match pattern'
            )
        if len(attrs['username']) > 150:
            raise serializers.ValidationError(
                'username must be less than 151 character long'
            )
        if attrs['username'].lower() == 'me':
            raise serializers.ValidationError('"me" is not a valid username')
        queryset = User.objects.filter(username=attrs['username'])
        if queryset.exists():
            if not queryset.filter(email=attrs['email']).exists():
                raise serializers.ValidationError(
                    'username is already registered'
                )
        queryset = User.objects.filter(email=attrs['email'])
        if queryset.exists():
            if not queryset.filter(username=attrs['username']):
                raise serializers.ValidationError(
                    'email is already registered'
                )
        return attrs

    def save(self, **kwargs):
        return User.objects.get_or_create(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )[0]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'bio',
            'role',
            'first_name',
            'last_name',
        )
        model = User

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if username := attrs.get('username'):
            if len(username) > 150:
                raise serializers.ValidationError(
                    'username must be less than 151 character long'
                )
        if first_name := attrs.get('first_name'):
            if len(first_name) > 150:
                raise serializers.ValidationError(
                    'first_name must be less than 151 character long'
                )
        if last_name := attrs.get('last_name'):
            if len(last_name) > 150:
                raise serializers.ValidationError(
                    'last_name must be less than 151 character long'
                )
        if email := attrs.get('email'):
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    'email is already registered'
                )

        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        model = Review
        read_only_fields = (
            'title',
            'pub_date',
        )

    def validate(self, attrs):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError('Review already exists')

        return attrs


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
        model = Title

    def validate_year(self, value):
        year = int(timezone.now().year)
        if value > year:
            raise serializers.ValidationError(
                'Проверьте год публикации тайтла!'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        model = Comment
