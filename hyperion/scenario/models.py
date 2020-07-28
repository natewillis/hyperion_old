from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
import datetime

DEFAULT_COUNTRY_ID = 1
DEFAULT_WAVE_ID = 1
DEFAULT_POINT = Point(0, 0, srid=4326)
DEFAULT_DURATION = datetime.timedelta(days=0)


# Create your models here.
class Scenario(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    exercise_start = models.DateTimeField(default=datetime.datetime.now)
    scenario_start = models.DurationField(default=0)

    def __str__(self):
        return self.name


class Wave(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_delta = models.DurationField(default=DEFAULT_DURATION)

    def start_datetime(self):
        return self.scenario.exercise_start + self.start_delta


class Vehicle(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    page_display_name = models.CharField(max_length=200)
    country = models.ForeignKey('world.WorldBorder', on_delete=models.CASCADE, default=DEFAULT_COUNTRY_ID)

    def __str__(self):
        return f'{self.page_display_name} - {self.pk}'


class Weapon(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    wave = models.ForeignKey(Wave, on_delete=models.CASCADE, default=DEFAULT_WAVE_ID)
    page_display_name = models.CharField(max_length=200)
    true_launch_location = models.PointField(default=DEFAULT_POINT)
    observed_launch_location = models.PointField(null=True, blank=True)
    observed_launch_country = models.ForeignKey('world.WorldBorder', null=True, blank=True, on_delete=models.CASCADE)
    launch_delta = models.DurationField(default=DEFAULT_DURATION)

    def __str__(self):
        return f'{self.page_display_name} - {self.pk}'

    def launch_location(self):
        if self.observed_launch_location is None:
            return self.true_launch_location
        else:
            return self.observed_launch_location

    def launch_datetime(self):
        return self.wave.start_datetime() + self.launch_delta


class Warhead(models.Model):
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    warhead_yield = models.FloatField()
    true_impact_location = models.PointField(default=DEFAULT_POINT)
    observed_impact_location = models.PointField(null=True)
    observed_impact_country = models.ForeignKey('world.WorldBorder', null=True, on_delete=models.CASCADE)
    impact_delta = models.DurationField(default=DEFAULT_DURATION)

    def __str__(self):
        return f'{self.warhead_yield} kt warhead - {self.pk}'

    def impact_datetime(self):
        return self.weapon.launch_datetime() + self.impact_delta
