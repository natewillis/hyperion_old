from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


# API router
router = DefaultRouter()
router.register(r'scenarios', views.ScenarioViewSet, 'scenarios')

app_name = 'scenario'
urlpatterns = [
    path('', views.ScenarioListView.as_view(), name='scenario_list'),
    path('new', views.ScenarioCreate.as_view(), name='scenario_new'),
    path('edit/<int:pk>', views.ScenarioUpdate.as_view(), name='scenario_edit'),
    path('dashboard/<int:pk>', views.scenario_dashboard, name='scenario_dashboard'),
    path('api/', include(router.urls)),
]
