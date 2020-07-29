from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from . import models
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from . import serializers


def testtable(request):
    return render(request, 'scenario/testtable.html')


class ScenarioListView(ListView):

    model = models.Scenario


class ScenarioCreate(CreateView):

    model = models.Scenario
    fields = ['name', 'description', 'exercise_start', 'scenario_start']
    success_url = reverse_lazy('scenario:scenario-list')


class ScenarioUpdate(UpdateView):

    model = models.Scenario
    fields = ['name', 'description', 'exercise_start', 'scenario_start']
    success_url = reverse_lazy('scenario:scenario-list')


def scenario_dashboard(request, pk):
    scenario = get_object_or_404(models.Scenario, pk=pk)
    return render(request, 'scenario/scenario_dashboard.html', {'scenario': scenario})


class ScenarioViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ScenarioSerializer
    queryset = models.Scenario.objects.all()


class WaveViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WaveSerializer
    queryset = models.Wave.objects.all()
    filterset_fields = ('scenario',)


class WeaponViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WeaponSerializer
    queryset = models.Weapon.objects.all()
    filterset_fields = ('wave', 'wave__scenario')


class WeaponGISViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WeaponGISSerializer
    queryset = models.Weapon.objects.all()
    filterset_fields = ('wave', 'wave__scenario')


class WeaponTableViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WeaponTableSerializer
    queryset = models.Weapon.objects.all()
    filterset_fields = ('wave', 'wave__scenario')


