from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.gis.geos import Point
from . import models
from django.apps import apps
import dateutil.parser


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
        return obj.impact_location().coords[1]

    def get_longitude(self, obj):
        return obj.impact_location().coords[0]

    class Meta:
        model = models.Warhead
        fields = [
            'id',
            'weapon',
            'warhead_yield',
            'target_display_name',
            'impact_datetime',
            'latitude',
            'longitude',
        ]


class WeaponTableSerializer(ModelSerializer):
    latitude = SerializerMethodField()
    longitude = SerializerMethodField()
    launch_country_id = SerializerMethodField()
    warheads = WarheadTableSerializer(many=True)

    def get_longitude(self, obj):
        return obj.launch_location().coords[0]

    def get_latitude(self, obj):
        return obj.launch_location().coords[1]

    def get_launch_country_id(self, obj):
        return obj.launch_country().id

    class Meta:
        model = models.Weapon
        fields = [
            'id',
            'wave',
            'page_display_name',
            'latitude',
            'longitude',
            'launch_datetime',
            'launch_country_id',
            'warheads'
        ]

    def to_internal_value(self, data):  # In a post, this is called before validate

        # turn lat/lon back into a point
        launch_latitude = float(data.pop('latitude'))
        launch_longitude = float(data.pop('longitude'))
        launch_point = Point(x=launch_longitude, y=launch_latitude)
        data['true_launch_location'] = launch_point

        # properly name launch country
        WorldBorder = apps.get_model('world', 'WorldBorder')
        data['country'] = WorldBorder.objects.get(pk=data.pop('launch_country_id'))

        # turn launch_datetime back into delta from wave
        data['wave'] = models.Wave.objects.get(pk=data['wave'])
        launch_datetime = dateutil.parser.isoparse(data.pop('launch_datetime'))
        data['launch_delta'] = launch_datetime - data['wave'].start_datetime()

        for warhead_data in data['warheads']:

            # turn impact lat/lon back into a point
            impact_latitude = float(warhead_data.pop('latitude'))
            impact_longitude = float(warhead_data.pop('longitude'))
            print(f'impact lat:{impact_latitude} lon:{impact_longitude}')
            impact_point = Point(x=impact_longitude, y=impact_latitude)
            warhead_data['true_impact_location'] = impact_point

            # turn impact_datetime back into delta from wave
            impact_datetime = dateutil.parser.isoparse(warhead_data.pop('impact_datetime'))
            warhead_data['impact_delta'] = impact_datetime - launch_datetime

        # return fixed object
        return data

    def create(self, validated_data):

        print('create')
        print(validated_data)

        # get warhead data from nested
        warheads = validated_data.pop('warheads')

        # create/update weapon object
        if 'id' in validated_data.items():
            weapon = models.Weapon.objects.get(pk=validated_data['id'])
            for key, value in validated_data:
                if not key == 'id':
                    setattr(weapon, key, value)
        else:
            weapon = models.Weapon(**validated_data)

        # Save new/updated object
        weapon.save()

        # create a warhead object
        for warhead_data in warheads:
            print('warhead')
            print(warhead_data)

            # create/update warhead object
            if 'id' in warhead_data.items():
                warhead = models.Warhead.objects.get(pk=warhead_data['id'])
                for key, value in warhead_data:
                    if not key == 'id':
                        setattr(warhead, key, value)
                setattr(warhead, 'weapon', weapon)
            else:
                warhead = models.Warhead(**warhead_data)
                setattr(warhead, 'weapon', weapon)

            # Save new/updated object
            warhead.save()

        return weapon


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
