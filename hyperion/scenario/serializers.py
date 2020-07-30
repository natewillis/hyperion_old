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

    launch_country_code = SerializerMethodField()
    wave_name = SerializerMethodField()

    def get_launch_country_code(self, obj):
        return obj.launch_country().fips

    def get_wave_name(self, obj):
        return obj.wave.name

    class Meta:
        model = models.Weapon
        geo_field = "true_launch_location"
        fields = [
            'id',
            'page_display_name',
            'wave_name',
            'launch_country_code'
        ]


class WeaponSerializer(ModelSerializer):
    class Meta:
        model = models.Weapon
        fields = '__all__'


class WarheadTableSerializer(ModelSerializer):
    latitude = SerializerMethodField()
    longitude = SerializerMethodField()

    def get_latitude(self, obj):
        return obj.impact_location().coords[0]

    def get_longitude(self, obj):
        return obj.impact_location().coords[1]

    class Meta:
        model = models.Warhead
        fields = [
            'id',
            'warhead_yield',
            'impact_datetime',
            'latitude',
            'longitude',
        ]


class WeaponTableSerializer(ModelSerializer):
    latitude = SerializerMethodField()
    longitude = SerializerMethodField()
    launch_country_code = SerializerMethodField()
    wave_name = SerializerMethodField()
    warheads = WarheadTableSerializer(many=True)

    def get_latitude(self, obj):
        return obj.launch_location().coords[0]

    def get_longitude(self, obj):
        return obj.launch_location().coords[1]

    def get_launch_country_code(self, obj):
        return obj.launch_country().fips

    def get_wave_name(self, obj):
        return obj.wave.name

    class Meta:
        model = models.Weapon
        fields = [
            'id',
            'wave_name',
            'page_display_name',
            'latitude',
            'longitude',
            'launch_datetime',
            'launch_country_code',
            'warheads'
        ]


class WarheadGISSerializer(GeoFeatureModelSerializer):

    launch_country_code = SerializerMethodField()
    wave_name = SerializerMethodField()

    def get_launch_country_code(self, obj):
        return obj.weapon.launch_country().fips

    def get_wave_name(self, obj):
        return obj.weapon.wave.name

    class Meta:
        model = models.Warhead
        geo_field = "true_impact_location"
        fields = [
            'id',
            'target_display_name',
            'wave_name',
            'launch_country_code'
        ]
