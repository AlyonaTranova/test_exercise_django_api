from django.views.generic import DetailView
from rest_framework.decorators import permission_classes
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .serializers import FlatRoomSerializer, FlatSerializer, RegistrationSerializer, \
	RentOrderSerializer, CustomUserListSerializer
from .models import CustomUser, Flat, RentOrder

from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.permissions import AllowAny


@permission_classes([AllowAny])
class RegistrationView(CreateModelMixin, GenericViewSet):
	queryset = get_user_model().objects.all()
	serializer_class = RegistrationSerializer


@permission_classes([IsAuthenticated])
class CustomUserView(ListModelMixin, DetailView, GenericViewSet):
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserListSerializer

	def get_queryset(self):
		if self.request.user.status == 'ow':
			return CustomUser.objects.filter(status='re')
		elif self.request.user.status == 're':
			return CustomUser.objects.filter(status='ow')


class FlatView(ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, DetailView, GenericViewSet):
	queryset = Flat.objects.all()
	serializer_class = FlatSerializer

	def perform_create(self, serializer):
		if self.request.user.status == 'ow':
			serializer.save(user=self.request.user)
		else:
			self.permission_denied(self.request)

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)

	def perform_destroy(self, instance):
		instance.delete(user=self.request.user)

	def permission_denied(self, request, message=None, code=None):
		if request.authenticators and not request.successful_authenticator:
			raise exceptions.NotAuthenticated()
		raise exceptions.PermissionDenied(detail="user don't have access", code=401)


@permission_classes([IsAuthenticated])
class FlatRoomView(ReadOnlyModelViewSet):
	serializer_class = FlatRoomSerializer

	def get_queryset(self):
		return Flat.flatroom_set.all()


@permission_classes([IsAuthenticated])
class RentOrderView(ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, DetailView, GenericViewSet):
	queryset = RentOrder.objects.all()
	serializer_class = RentOrderSerializer

	def filter_queryset(self, queryset):
		return queryset.filter(**self.request.data)

	def get_queryset(self):
		return RentOrder.objects.filter(renter=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)

	def perform_destroy(self, instance):
		instance.delete(user=self.request.user)
