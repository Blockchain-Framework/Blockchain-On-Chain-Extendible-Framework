from django.urls import path
from . import views

urlpatterns = [
    path('create_metric/', views.create_metric, name='create_metric'),
]
