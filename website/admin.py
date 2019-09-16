from django.contrib import admin
from website import models as website_models
from django.db import models 
from django.core.exceptions import ValidationError

from django import forms
class FrontConfigForm( forms.ModelForm ):
    prestart_help = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = website_models.FrontConfig
        fields = '__all__'

class FrontConfig_Admin( admin.ModelAdmin ):
    form = FrontConfigForm


admin.site.register(website_models.FrontConfig, FrontConfig_Admin)
admin.site.register(website_models.ParrotCommand)
admin.site.register(website_models.Patient)
admin.site.register(website_models.Duration)
admin.site.register(website_models.DiagnoseSession)
admin.site.register(website_models.ToyCar)
