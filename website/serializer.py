from rest_framework import serializers
from website import models


class command_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.command
        fields = ('id','name', 'title', 'category_id', 'tag')
        read_only_fields = ('id','name', 'title', 'category_id', 'tag')

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

