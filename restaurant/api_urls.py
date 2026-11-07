from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import BookingViewSet, MenuViewSet, RegisterView, TokenLoginView

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'menu', MenuViewSet, basename='menu')

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('token/login/', TokenLoginView.as_view(), name='token-login'),
]
