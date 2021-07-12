from rest_framework.relations import HyperlinkedIdentityField
from .models import Build, Flat, FlatRoom, FlatAttribute, CustomUser, RentOrder, FlatAttributesValue
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = CustomUser
		fields = ['id', 'email', 'username', 'password', 'password2', 'first_name',
		          'last_name', 'birthday', 'phone', 'language', 'status']
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def save(self, **kwargs):
		account = CustomUser(
			email=self.validated_data['email'],
			username=self.validated_data['username'],
			first_name=self.validated_data['first_name'],
			last_name=self.validated_data['last_name'],
			birthday=self.validated_data['birthday'],
			age=self.validated_data['age'],
			phone=self.validated_data['phone'],
			language=self.validated_data['language'],
			status=self.validated_data['status'],
		)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']

		if password != password2:
			raise serializers.ValidationError({'password': 'passwords should match'})
		account.set_password(password)
		account.save()


class CustomUserListSerializer(serializers.ModelSerializer):
	url = HyperlinkedIdentityField(view_name='v1:user-detail', lookup_url_kwarg='username')

	class Meta:
		model = CustomUser
		fields = ['id', 'url', 'first_name', 'last_name', 'email', 'username', 'phone', 'language', 'status']


class FlatAttributeSerializer(serializers.ModelSerializer):
	def validate(self, data):
		if data['count'] < 0:
			raise serializers.ValidationError({"count": "at least one value of the attribute"})
		return data

	class Meta:
		model = FlatAttribute
		fields = ['id', 'type', 'description']


class FlatAttributeValuesSerializer(serializers.ModelSerializer):
	def validate(self, data):
		if data['count'] < 0:
			raise serializers.ValidationError({"count": "at least one value of an attribute"})
		return data

	class Meta:
		model = FlatAttributesValue
		fields = ['id', 'attribute_id', 'flat_room_id', 'count', 'description']


class FlatRoomSerializer(serializers.ModelSerializer):

	def validate(self, data):
		if data.attributes['attribute_id'].count < 2:
			raise serializers.ValidationError("at least attributes in each room")
		return data

	class Meta:
		model = FlatRoom
		fields = ['id', 'type', 'description']


class FlatSerializer(serializers.ModelSerializer):

	def validate(self, data):
		if data['room_count'] <= 0:
			raise serializers.ValidationError({"room_count": "at least one room in a flat"})
		return data

	class Meta:
		model = Flat
		fields = ['id', 'build_id', 'price', 'owner_id', 'room_count', 'type', 'flat_room']
		search_fields = 'price'


class BuildSerializer(serializers.ModelSerializer):
	class Meta:
		model = Build
		fields = '__all__'


class RentOrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = RentOrder
		fields = ['date_from', 'date_to', 'total_price', 'renter', 'flat_id_for']
