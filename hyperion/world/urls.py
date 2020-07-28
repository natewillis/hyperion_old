from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


# API router
router = DefaultRouter()
router.register(r'worldborders', views.WorldBorderViewSet)

app_name = 'world'
urlpatterns = [
    path('api/', include(router.urls)),
]