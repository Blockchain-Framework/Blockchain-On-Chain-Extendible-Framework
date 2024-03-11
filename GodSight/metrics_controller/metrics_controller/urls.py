from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/metrics/', include('metrics.urls')),  # Include your app's URLs with a prefix
]