from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SelfUserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet)
