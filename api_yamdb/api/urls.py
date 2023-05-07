from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register(
    'auth',
    views.AuthViewSet,
    basename='auth',
)
router.register(
    'titles',
    views.TitleViewSet,
    basename='titles',
)
router.register(
    'genres',
    views.GenreViewSet,
    basename='genres',
)
router.register(
    'categories',
    views.CategoryViewSet,
    basename='categories',
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    views.CommentsViewSet,
    basename='comments',
)
router.register(
    'users',
    views.MeViewSet,
    basename='me',
)
router.register(
    r'users(?!/me)',
    views.UsersViewSet,
    basename='users',
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    views.ReviewViewSet,
    basename='reviews',
)

urlpatterns = [
    path('v2/', include(router.urls)),
]
