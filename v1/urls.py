from rest_framework.routers import DefaultRouter
from .views import FlatView, RentOrderView, RegistrationView, CustomUserView, FlatRoomView
app_name = 'v1'

router = DefaultRouter()
router.register(r'register', RegistrationView, basename='register')
router.register(r'users', CustomUserView, basename='user')
router.register(r'users/<int:pk>', CustomUserView, basename='user-detail')
router.register(r'flats', FlatView, basename='flat-list')
router.register(r'flats/<int:pk>/rooms', FlatRoomView, basename='rooms')
router.register(r'orders', RentOrderView, basename='order')
urlpatterns = router.urls
