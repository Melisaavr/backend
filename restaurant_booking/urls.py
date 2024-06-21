from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from booking.views import UserViewSet, SlotViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'slots', SlotViewSet, basename='slot')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
