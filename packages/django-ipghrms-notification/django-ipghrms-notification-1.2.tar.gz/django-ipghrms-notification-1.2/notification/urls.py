from django.urls import path, include


urlpatterns = [
    path('', include('notification.notif_urls')),
    path('api/', include('notification.api_urls')),
]
