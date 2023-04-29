from rest_framework.routers import DefaultRouter
from .views import CafeViewSet, MenuItemViewSet

router = DefaultRouter()

router.register(r'cafe', CafeViewSet, basename='cafe')
router.register(r'menu-item', MenuItemViewSet, basename='menu-item')

urlpatterns = []
urlpatterns += router.urls