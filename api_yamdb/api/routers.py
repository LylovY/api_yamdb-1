from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SelfUserViewSet, ReviewViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
