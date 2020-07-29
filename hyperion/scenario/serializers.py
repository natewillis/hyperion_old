from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from . import models


class ScenarioSerializer(ModelSerializer):
    class Meta:
        model = models.Scenario
        fields = '__all__'


class WaveSerializer(ModelSerializer):
    class Meta:
        model = models.Wave
        fields = '__all__'


class WeaponGISSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = models.Weapon
        geo_field = "true_launch_location"
        fields = '__all__'


class WeaponSerializer(ModelSerializer):
    class Meta:
        model = models.Weapon
        fields = '__all__'


class WeaponTableSerializer(ModelSerializer):
    latitude = SerializerMethodField()
    longitude = SerializerMethodField()

    def get_latitude(self, obj):
        return obj.launch_location().coords[0]

    def get_longitude(self, obj):
        return obj.launch_location().coords[1]

    class Meta:
        model = models.Weapon
        fields = [
            'id',
            'page_display_name',
            'latitude',
            'longitude',
            'launch_datetime',
        ]
