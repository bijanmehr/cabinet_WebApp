from rest_framework import serializers
from website import models


class properties_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.FrontConfig
        fields = ('prestart_help',)
        read_only_fields = ('prestart_help',)


class command_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.ParrotCommand
        fields = ('id','name', 'title', 'category_id', 'tag', 'perform_time')
        read_only_fields = ('id','name', 'title', 'category_id', 'tag', 'perform_time')

class person_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patient
        fields = ('first_name','last_name','phone_number','birth_year','gender','medical_info','person_id')

class toycar_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.ToyCar
        fields = ('time', 'ac_x', 'ac_y', 'ac_z', 'encode1', 'encode2')

class stage_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stage
        fields = ('name', 'start_time', 'duration')
        
class session_serializer(serializers.ModelSerializer):
    stage = stage_serializer(many=False, read_only=True)
    class Meta:
        model = models.DiagnoseSession
        fields = ('id', 'start_time', 'finish_time', 'expired', 'stage')

