from django.contrib  import admin
from django.urls     import path, include
from django.http     import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


def health_check(request):
    return JsonResponse({
        'success': True,
        'message': 'Finance Dashboard API is running.',
        'version': '1.0.0',
    })


urlpatterns = [
    path('',          health_check,                        name='health-check'),
    path('admin/',    admin.site.urls),

    path('api/auth/login/',   TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/auth/refresh/', TokenRefreshView.as_view(),    name='token_refresh'),

    path('api/users/',     include('users.urls')),
    path('api/records/',   include('records.urls')),
    path('api/dashboard/', include('dashboard.urls')),
]