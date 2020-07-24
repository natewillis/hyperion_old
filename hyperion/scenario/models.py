from django.contrib.gis.db import models


# Create your models here.
class Scenario(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    page_display_name = models.CharField(max_length=200)
    country = models.ForeignKey('world.WorldBorder', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.page_display_name} - {self.pk}'


class Weapon(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    page_display_name = models.CharField(max_length=200)
    true_launch_location = models.PointField()
    observed_launch_location = models.PointField(null=True)
    observed_launch_country = models.ForeignKey('world.WorldBorder', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.page_display_name} - {self.pk}'


class Warhead(models.Model):
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    warhead_yield = models.FloatField()
    true_impact_location = models.PointField()
    observed_impact_location = models.PointField()
    observed_impact_country = models.ForeignKey('world.WorldBorder', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.warhead_yield} kt warhead - {self.pk}'
