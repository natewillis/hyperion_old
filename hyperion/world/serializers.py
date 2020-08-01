from rest_framework_gis.serializers import GeoFeatureModelSerializer, ModelSerializer
from .models import WorldBorder


class WorldBorderSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = WorldBorder
        geo_field = "mpoly"
        fields = [
            'id',
            'name',
            'fips',
            'region',
            'subregion'
        ]


class WorldBorderFIPSSerializer(ModelSerializer):
    class Meta:
        model = WorldBorder
        fields = [
            'id',
            'fips',
        ]


class WorldBorderNameSerializer(ModelSerializer):
    class Meta:
        model = WorldBorder
        fields = [
            'id',
            'name',
        ]

