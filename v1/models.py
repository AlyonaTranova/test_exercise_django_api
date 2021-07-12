from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator


class MyCustomUserManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(email=self.normalize_email(email), username=username)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(email=self.normalize_email(email), password=password, username=username)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class CustomUser(AbstractBaseUser):
	email = models.EmailField(null=False, unique=True, verbose_name='email')
	username = models.CharField(max_length=40, unique=True, verbose_name='username')
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	first_name = models.CharField(max_length=255, verbose_name='first name', default='')
	last_name = models.CharField(max_length=255, verbose_name='last name', default='')
	phone = models.CharField(max_length=13, null=False, verbose_name='phone number')
	birthday = models.DateField(null=True, verbose_name='birthday')
	age = models.PositiveIntegerField(validators=[MinValueValidator(18)], default=18)

	lang_choice = [
		('ru', 'russian'),
		('en', 'english'),
		('es', 'spanish'),
		('fr', 'french'),
		('it', 'italian'),
		('de', 'german'),
	]
	language = models.CharField(max_length=3, choices=lang_choice, default='en', verbose_name='language')
	status_choice = [
		('ow', 'owner'),
		('re', 'renter'),
	]
	status = models.CharField(max_length=3, choices=status_choice, default='owner', verbose_name='status')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='created')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='updated')

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyCustomUserManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True


class Build(models.Model):
	name = models.CharField(max_length=255, verbose_name='name')
	address = models.CharField(max_length=255, verbose_name='address', default='')
	description = models.TextField(verbose_name='description', null=False)

	def __str__(self):
		return self.name


class Flat(models.Model):
	build_id = models.ForeignKey(Build, on_delete=models.CASCADE, verbose_name='building')
	price = models.FloatField(verbose_name='price', default=0.0, null=False)
	owner_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='owner')
	room_count = models.PositiveIntegerField(verbose_name='room count', default=1, null=False)
	type_choice = [
		('st', 'studio'),
		('ap', 'apartment'),
		('h', 'house'),
		('th', 'townhouse'),
	]
	type = models.CharField(max_length=20, choices=type_choice)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='created')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='updated')


class FlatRoom(models.Model):
	room_choice = [
		('k', 'kitchen'),
		('bth', 'bathroom'),
		('eh', 'entrance hall'),
		('bd', 'bedroom'),
		('l', 'living room'),
	]
	type = models.CharField(max_length=255, choices=room_choice)
	flat_id = models.ForeignKey(to=Flat, on_delete=models.CASCADE, verbose_name='flat', related_name='flat_room')
	description = models.TextField(null=False, verbose_name='description')


class FlatAttribute(models.Model):
	name = models.CharField(max_length=256, verbose_name='flat attribute', help_text='examples: window, wardrobe, baker')


class FlatAttributesValue(models.Model):
	attribute_id = models.ForeignKey(to=FlatAttribute, on_delete=models.CASCADE, related_name='flat_attribute')
	flat_room_id = models.ForeignKey(to=FlatRoom, on_delete=models.CASCADE, related_name='flat_attributes_value')
	count = models.CharField(max_length=100, null=False, verbose_name='count')
	description = models.TextField(null=True, verbose_name='description', default='')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='created')


class RentOrder(models.Model):
	date_from = models.DateField(null=False, verbose_name='from', default='')
	date_to = models.DateField(null=False, verbose_name='to', default='')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='created')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='updated')
	total_price = models.FloatField(default=0.0, verbose_name='total price')
	renter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, verbose_name='renter', default='')
	flat_id_for = models.ForeignKey(Flat, on_delete=models.CASCADE, null=False, verbose_name='flat', default='')
