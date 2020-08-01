from rest_framework import viewsets
from . import serializers
from .models import WorldBorder


class WorldBorderViewSet(viewsets.ModelViewSet):
    queryset = WorldBorder.objects.all().order_by('name')
    serializer_class = serializers.WorldBorderSerializer


class WorldBorderFIPSViewSet(viewsets.ModelViewSet):
    queryset = WorldBorder.objects.all().order_by('fips')
    serializer_class = serializers.WorldBorderFIPSSerializer


class WorldBorderNameViewSet(viewsets.ModelViewSet):
    queryset = WorldBorder.objects.all().order_by('name')
    serializer_class = serializers.WorldBorderNameSerializer

