from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from time import time
from website import myexceptions
from django.core.exceptions import ValidationError
from website import settings

def getTime():
    return int(time())

def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)

class Duration(models.Model):
    def clean(self):
        validate_only_one_instance(self)

    game_duration_minutes = models.SmallIntegerField(default= settings.DEFAULT_GAME_DURATION)
    wheel_duration_minutes = models.SmallIntegerField(default= settings.DEFAULT_WHEEL_DURATION)
    parrot_duration_minutes = models.SmallIntegerField(default= settings.DEFAULT_PARROT_DURATION)
    diagnose_duration_minutes = models.SmallIntegerField(default= settings.DEFAULT_DIAGNOSE_DURATION)
#    done_duration_minutes = models.SmallIntegerField(default= 0)

    def __str__(self):
        return 'Duration For Different Stages'

    @staticmethod
    def get():
        try:
            return Duration.objects.all()[0]
        except IndexError:
            return Duration.objects.create()
        
    def game_duration(self): return self.game_duration_minutes * 60
    def wheel_duration(self): return self.wheel_duration_minutes * 60
    def parrot_duration(self): return self.parrot_duration_minutes * 60
    def diagnose_duration(self): return self.diagnose_duration_minutes * 60

    def stage_duration(self, stage_name):
        if stage_name == settings.GAME_STAGE:
            return self.game_duration()
        elif stage_name == settings.WHEEL_STAGE:
            return self.wheel_duration()
        elif stage_name == settings.PARROT_STAGE:
            return self.parrot_duration()
        elif stage_name == settings.DONE_STAGE:
            return 0
        else: raise ValueError('No stage is named ' + stage_name)

class FrontConfig(models.Model):
    def clean(self):
        validate_only_one_instance(self)

    prestart_help = models.CharField(max_length= 8192, default= "محتویات این فیلد را میتوانید در صفحه ادمین ویرایش کنید.")

    @staticmethod
    def get():
        try:
            return FrontConfig.objects.all()[0]
        except IndexError:
            return FrontConfig.objects.create()

    def __str__(self):
        return 'FrontEnd Properties'



class ParrotCommand(models.Model):
    TAG_CHOICES = (
        ("P_M", "Parrot Movement"),
        ("P_V", "Parrot Voice"),
        ("P_A", "Parrot Auto"),
    )
    name = models.CharField(max_length=40,null=False,blank=False)
    title = models.CharField(max_length=40,null=False,blank=False)
    category_id = models.IntegerField(null= False, blank= False, default= 0)
    tag = models.CharField(choices=TAG_CHOICES,max_length=4,null=False,blank=False)
    arg = models.IntegerField(unique=True,blank=False,null=False)
    priority = models.IntegerField(blank=False,null=False,default=10)
    voice_file = models.FileField(blank = True)
    perform_time = models.IntegerField(default=5) #in second

    def __str__(self):
        return self.tag + ": " + self.name

    
import re
def is_valid_iran_code(input):
    if not re.search(r'^\d{10}$', input):
        raise ValidationError("کد ملی عددی ۱۰ رقمی باید باشد")

    check = int(input[9])
    s = sum([int(input[x]) * (10 - x) for x in range(9)]) % 11
    if not ((s < 2 and check == s) or (s >= 2 and check + s == 11)):
#        raise ValidationError("کد ملی وارد شده صحیح نیست")
        pass

class Patient(models.Model):
    first_name = models.CharField(max_length=40,null=False,blank=False)
    last_name = models.CharField(max_length=50,null=False,blank=False)
    phone_regex = RegexValidator(regex=r'^\+?0?\d{9,15}$',
                                 message="شماره تلفن خود را در فرمت مناسب بنویسید")
    phone_number = models.CharField(max_length=17,null=False,blank=False, validators=[RegexValidator])  # validators should be a list
    birth_year = models.IntegerField(null=True, blank=True)
    gender_values = (
        ("male", "مرد"),
        ("female", "زن"),
    )
    
    gender = models.CharField(null=False, blank=False, max_length=10, choices=gender_values)

    medical_history = (
        ("ADHD", "ADHD"),
        ("normal", "نرمال"),
        ("autism", "اتیسم"),
        ("NA", "تعیین نشده"),
    )
    medical_info = models.CharField(choices=medical_history, max_length=10, default= medical_history[3][0])
    person_id = models.CharField(validators=[is_valid_iran_code], null=False, blank=False, unique=True, max_length=10)

    login_status = models.BooleanField(default=False)
    last_activity = models.BigIntegerField(default=getTime)


    def clean(self, *args, **kwargs):
        super(Patient, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Patient, self).save(*args, **kwargs)

    def __str__(self):
        return self.person_id

    def current_session(self):
        try:
            return self.diagnosesession_set.get(expired= False)

        except MultipleObjectsReturned: # Should never happen
            most_recent = self.diagnosesession_set.filter(expired= False).order_by('start_time')[-1]
            to_expire = self.diagnosesession_set.filter(expired= False).exclude(id= most_recent.id)
            to_expire.update(expired= True)

            import logging
            logger = logging.getLogger('django.db.backends')
            logger.exception('current_session, multiple objects returned')
            return most_recent


    def check_session(self):
        if not self.diagnosesession_set.filter(expired= False):
            return False
        return True

    def start_session(self):
        now = int(time())
        default_stage = Stage.objects.create(start_time= now, duration= Duration.get().game_duration(), name= settings.GAME_STAGE)
        started_session = DiagnoseSession.objects.create(patient= self, start_time= now, stage= default_stage)

        return started_session

  
    def end_session(self):
        current_session = self.current_session()
        current_session.expired = True
        current_session.save()

    def pause_session(self):
        current_session = self.current_session()
        current_session.paused = True
        current_session.save()
    
    def resume_session(self):
        current_session = self.current_session()
        current_session.paused = False
        current_session.save()

    @staticmethod
    def current_patient():
        return Patient.objects.get(login_status= True)

class Stage(models.Model):
    start_time = models.BigIntegerField(null= False)
    duration = models.IntegerField(null= False)
    stages = (
        (settings.GAME_STAGE, "game"),
        (settings.WHEEL_STAGE, "Wheel"),
        (settings.PARROT_STAGE, "parrot"),
        (settings.DONE_STAGE, "done"),
    )
    name = models.CharField(choices=stages,max_length=2, default= settings.GAME_STAGE)



class DiagnoseSession(models.Model):
    patient = models.ForeignKey(Patient, on_delete= models.CASCADE)
    start_time = models.BigIntegerField(null= False, default= False)
    finish_time = models.BigIntegerField(default= 0)
    
    stage = models.ForeignKey(Stage, on_delete= models.DO_NOTHING)

    played_game = models.BooleanField(default= True)
    played_toycar = models.BooleanField(default= True)

    diagnose_result = (
        ('AUTISTIC_HP', 'اتیسم به احتمال قوی'),
        ('AUTISTIC_LP', 'اتیسم به احتمال  ضعیف'),
        ('NOT_AUTISTIC', 'عدم تشخیص اتیسم'),
        ('NA', 'NA')
    )
    expertsystem_judgement = models.CharField(choices= diagnose_result, max_length= 16, default= diagnose_result[3][0])

    paused = models.BooleanField(default= False)
    expired = models.BooleanField(default= False)

    def change_stage(self, new_stage):
        self.stage.start_time = int(time())
        self.stage.duration= Duration.get().stage_duration(new_stage)
        self.stage.name= new_stage
        self.stage.save()   

        if self.stage.name == settings.DONE_STAGE:
            self.expired = True
        self.save()


    @staticmethod
    def check_active_session():
        try:
            DiagnoseSession.objects.get(expired= False, paused= False)
            return True
        except DiagnoseSession.DoesNotExist:
            return False



class ToyCar(models.Model):
    session = models.ForeignKey(DiagnoseSession, on_delete=models.CASCADE)
    time = models.BigIntegerField(null= False)
    ac_x = models.BigIntegerField(null= False)
    ac_y = models.BigIntegerField(null= False)
    ac_z = models.BigIntegerField(null= False)
    encode1 = models.BigIntegerField(null= False)
    encode2 = models.BigIntegerField(null= False)

#    class Meta:
#       unique_together = ('session', 'time', )

