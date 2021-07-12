from django.contrib import admin
from .models import CustomUser, FlatRoom, Flat, FlatAttribute, FlatAttributesValue, Build, RentOrder


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
	list_display = ['username', 'first_name', 'last_name', 'phone', 'birthday', 'id', 'email', 'language', 'status', 'age']
	list_filter = ['language', 'birthday']
	search_fields = ['email', 'first_name', 'last_name', 'phone']
	ordering = ['first_name', 'last_name']


@admin.register(Build)
class BuildingAdmin(admin.ModelAdmin):
	list_display = ['id', 'address', 'name', 'description']


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
	list_display = ['id', 'build_id', 'price', 'owner_id', 'type', 'room_count']


@admin.register(FlatRoom)
class FlatRoomAdmin(admin.ModelAdmin):
	list_display = ['id', 'flat_id', 'description', 'type']


@admin.register(FlatAttribute)
class FlatAttributeAdmin(admin.ModelAdmin):
	list_display = ['name']


@admin.register(FlatAttributesValue)
class FlatAttributesValueAdmin(admin.ModelAdmin):
	list_display = ['attribute_id', 'flat_room_id', 'count', 'description', ]


@admin.register(RentOrder)
class RentOrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'flat_id_for', 'date_from', 'date_to', 'total_price', 'renter']