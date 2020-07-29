from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


# API router
router = DefaultRouter()
router.register(r'scenarios', views.ScenarioViewSet)
router.register(r'waves', views.WaveViewSet)
router.register(r'weapons', views.WeaponViewSet)
router.register(r'weapons_gis', views.WeaponGISViewSet)
router.register(r'weapons_table', views.WeaponTableViewSet)

app_name = 'scenario'
urlpatterns = [
    path('', views.ScenarioListView.as_view(), name='scenario_list'),
    path('new', views.ScenarioCreate.as_view(), name='scenario_new'),
    path('edit/<int:pk>', views.ScenarioUpdate.as_view(), name='scenario_edit'),
    path('dashboard/<int:pk>', views.scenario_dashboard, name='scenario_dashboard'),
    path('testtable/', views.testtable, name='testtable'),
    path('api/', include(router.urls)),
]
