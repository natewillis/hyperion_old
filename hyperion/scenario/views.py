from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from .models import Scenario, Weapon
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from . import serializers


class ScenarioListView(ListView):

    model = Scenario


class ScenarioCreate(CreateView):

    model = Scenario
    fields = ['name', 'description', 'exercise_start', 'scenario_start']
    success_url = reverse_lazy('scenario:scenario-list')


class ScenarioUpdate(UpdateView):

    model = Scenario
    fields = ['name', 'description', 'exercise_start', 'scenario_start']
    success_url = reverse_lazy('scenario:scenario-list')


def scenario_dashboard(request, pk):
    scenario = get_object_or_404(Scenario, pk=pk)
    return render(request, 'scenario/scenario_dashboard.html', {'scenario': scenario})


class ScenarioViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ScenarioSerializer
    queryset = Scenario.objects.all()
    lookup_field = 'id'

    @action(detail=True, methods=["GET"])
    def weapons(self, request, id=None):
        scenario = self.get_object()
        weapons = Weapon.objects.filter(wave__scenario=scenario)
        serializer = serializers.WeaponSerializer(weapons, many=True)
        return Response(serializer.data, status=200)
