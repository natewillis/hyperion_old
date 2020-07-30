from django.contrib.gis import admin
from . import models

# Register your models here.
admin.site.register(models.Scenario, admin.ModelAdmin)
admin.site.register(models.Weapon, admin.GeoModelAdmin)
admin.site.register(models.Warhead, admin.GeoModelAdmin)
admin.site.register(models.Wave, admin.GeoModelAdmin)
