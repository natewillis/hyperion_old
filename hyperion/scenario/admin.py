from django.contrib.gis import admin
from .models import Scenario, Vehicle, Weapon, Warhead

# Register your models here.
admin.site.register(Scenario, admin.ModelAdmin)
admin.site.register(Vehicle, admin.GeoModelAdmin)
admin.site.register(Weapon, admin.GeoModelAdmin)
admin.site.register(Warhead, admin.GeoModelAdmin)
