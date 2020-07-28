from rest_framework import viewsets
from .serializers import WorldBorderSerializer
from .models import WorldBorder


class WorldBorderViewSet(viewsets.ModelViewSet):
    queryset = WorldBorder.objects.all().order_by('name')
    serializer_class = WorldBorderSerializer

