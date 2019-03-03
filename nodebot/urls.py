from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/message/', views.MessageAPIView.as_view(), name='api_message'),
]
