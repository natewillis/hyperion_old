from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from .models import Scenario
from django.urls import reverse_lazy


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
