from django.contrib import admin
from website import models

admin.site.register(models.command)
admin.site.register(models.Patient)
admin.site.register(models.Duration)
admin.site.register(models.DiagnoseSession)
admin.site.register(models.ToyCar)
