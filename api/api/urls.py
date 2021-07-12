from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
	openapi.Info(
		title="Documentation API",
		default_version='v1',
		description="Test description",
		terms_of_service="https://www.ourapi.com/policies/terms/",
		contact=openapi.Contact(email="contact@doc.local"),
		license=openapi.License(name="test License"),
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include('v1.urls', namespace='v1')),
	path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
