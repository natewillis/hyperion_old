from django.urls import path
from . import views

app_name = 'scenario'
urlpatterns = [
    path('', views.ScenarioListView.as_view(), name='scenario-list'),
    path('new', views.ScenarioCreate.as_view(), name='scenario-new'),
    path('edit/<int:pk>', views.ScenarioUpdate.as_view(), name='scenario-edit'),
]
