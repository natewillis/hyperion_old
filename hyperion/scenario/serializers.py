from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ModelSerializer
from . import models


class ScenarioSerializer(ModelSerializer):
    class Meta:
        model = models.Scenario
        fields = [
            'id',
            'name',
            'description',
            'exercise_start',
            'scenario_start',
        ]


class WeaponSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = models.Weapon
        geo_field = "true_launch_location"
        fields = ['id', 'page_display_name']