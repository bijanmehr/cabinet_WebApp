#!/usr/bin/env python
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import list_route,detail_route
from website import serializer,models, settings
from website.permissions import *
from website.settings import ros  
from website.authentication import PersonAuthentication
from rest_framework import mixins
import json
from django.http import HttpResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import os
from os.path import expanduser
import datetime


dir = expanduser("~") + '/Desktop/cabinet_db/'

def create_uid_directories(num, _time):
    if not os.path.exists(dir + '%s'%num ):
        os.makedirs(dir + '%s'%num )

    if not os.path.exists(dir + '%s'%num + '/' + _time):
        os.makedirs(dir + '%s'%num + '/' + _time)
    return str(dir + '%s'%num + '/' + _time)


def create_patient_directory():
    pass


from django.views.generic import TemplateView

front_static = TemplateView.as_view(template_name='index.html')

class UserProfileList(  mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.generics.GenericAPIView):
    queryset = models.Patient.objects.all()
    serializer_class = serializer.person_serializer

    def get_authenticators(self):
        if self.request.method == "POST":
            return []
        else: return [PersonAuthentication()]
        return super(UserProfileList, self).get_authenticators()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user:
            return HttpResponse(json.dumps(self.serializer_class(instance = request.user).data), status=200,
                                content_type='application/json; charset=utf8')
        else:
            return HttpResponse(json.dumps({'detail': 'اول با حساب خود وارد شوید'}), status=400,
                                content_type='application/json; charset=utf8')

    def put(self, request, *args, **kwargs):
        if request.user :
            s = self.serializer_class(instance=request.user,partial=True,data=request.data)
            if s.is_valid():
                s.save()
            return HttpResponse(json.dumps(self.serializer_class(request.user).data), status=200,
                                content_type='application/json; charset=utf8')
        else:
            return HttpResponse(json.dumps({'detail': 'اول با حساب خود وارد شوید'}), status=400,
                                content_type='application/json; charset=utf8')

class Properties (mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.generics.GenericAPIView):
    serializer_class = serializer.properties_serializer
    def get(self, request, *args, **kwargs):
        return HttpResponse(json.dumps(self.serializer_class(instance = models.FrontConfig.get()).data), status=200,
                            content_type='application/json; charset=utf8')

class SessionView(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication,)
    permission_classes = (IsLogin,)
    serializer_class = serializer.session_serializer

    @list_route(methods=['get'],permission_classes=[NotStarted]) #auth
    def start(self,request):       
        session = request.user.start_session()
        ros.dir_info.publish('%s'%create_uid_directories(str(request.user.person_id), str(session.id)))
        ros.stage_info.publish("start_test")

        return HttpResponse(json.dumps(serializer.stage_serializer(instance = session.stage).data), status=200,
                            content_type='application/json; charset=utf8')
    
    @list_route(methods=['get'],permission_classes=[StartedSession]) #auth
    def stop(self,request):                         
        request.user.end_session()
        ros.stage_info.publish("stop_test")
        return HttpResponse("", status=200,
                            content_type='application/json; charset=utf8')


    @list_route(methods=['get'], permission_classes=[StartedSession]) #auth
    def status(self,request):         
        session = request.user.current_session()
        return HttpResponse(json.dumps(self.serializer_class(instance = session).data), status=200,
                            content_type='application/json; charset=utf8')

                            
class StageView(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication, )
    permission_classes = (IsLogin, StartedSession, )
    serializer_class = serializer.stage_serializer

    @list_route(methods=['get']) #auth
    def status(self,request):                         
        stage = request.user.current_session().stage
        return HttpResponse(json.dumps(self.serializer_class(instance = stage).data), status=200,
                            content_type='application/json; charset=utf8')

class GameCommands(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication,)
    permission_classes = (IsLogin,)

    @list_route(methods=['get'],permission_classes=[NotStarted]) #auth
    def start(self,request):                         
        session = request.user.start_session()
        ros.dir_info.publish('%s'%create_uid_directories(str(request.user.id), str(session.id)))
        ros.stage_info.publish("start_test")

        return HttpResponse(json.dumps(serializer.stage_serializer(instance = session.stage).data), status=200,
                            content_type='application/json; charset=utf8')


 

    @list_route(methods=['post'], permission_classes=[StartedGame])  # auth
    def send_data(self, request):
        try:
            data = json.loads(codecs.decode(request.body, 'utf-8'))
            session = request.user.current_session()
            session.played_game, session.played_toycar =  data['game'], data['car']
            session.save()

            return HttpResponse("", status=200,
                                content_type='application/json; charset=utf8')
        except (ValueError, json.JSONDecodeError):
            return HttpResponse(json.dumps({'detail': 'ورودی نادرست'}), status=400,
                                content_type='application/json; charset=utf8')

class WheelCommands(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication,)
    permission_classes = (IsLogin,)


    @list_route(methods=['get'],permission_classes=[StartedGame]) #auth
    def start(self,request):
        session = request.user.current_session()
        session.change_stage(settings.WHEEL_STAGE)
        ros.stage_info.publish("end_stage_one")
        ros.stage_info.publish("start_wheel")
        return HttpResponse(json.dumps(serializer.stage_serializer(instance = session.stage).data), status=200,
                            content_type='application/json; charset=utf8')

    @list_route(methods=['post'], permission_classes=[StartedWheel])  # auth
    def perform(self, request):
        try:
            data = json.loads(codecs.decode(request.body, 'utf-8'))
            status = data['status']
            ros.wheel_status.publish(str(status))
            # TODO 
            return HttpResponse("", status=200,
                                content_type='application/json; charset=utf8')
        except(ValueError, json.JSONDecodeError):
            return HttpResponse(json.dumps({'detail': 'ورودی نادرست'}), status=400,
                                content_type='application/json; charset=utf8')



class ParrotCommands(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication,)
    queryset = models.ParrotCommand.objects.all()
    serializer_class = serializer.command_serializer
    permission_classes = (IsLogin,)



    @list_route(methods=['get'],permission_classes=[StartedWheel]) #auth
    def start(self,request):
        session = request.user.current_session()
        session.change_stage(settings.PARROT_STAGE)
        
        ros.stage_info.publish("end_stage_two")
        ros.stage_info.publish("start_parrot")

        return HttpResponse(json.dumps(serializer.stage_serializer(instance = session.stage).data), status=200,
                            content_type='application/json; charset=utf8')

    @list_route(methods=['get'], permission_classes=[])  # auth
    def commands(self, request):
        ret = {}
        query = self.queryset.filter(tag="P_M").order_by("priority", "arg")
        ret["movement"] = self.serializer_class(instance=query, many=True).data
        query = self.queryset.filter(tag="P_V").order_by("priority", "arg")
        ret["voice"] = self.serializer_class(instance=query, many=True).data

        # print(ret)
        return HttpResponse(json.dumps(ret), status=200,
                            content_type='application/json; charset=utf8')


    @list_route(methods=['post'], permission_classes=[StartedParrot])  # auth
    def mode(self, request):
        try:
            data = json.loads(codecs.decode(request.body, 'utf-8'))
            commandType = data['mode']
            if (commandType != "auto" and commandType != "manual"):
                return HttpResponse(json.dumps({'detail': 'ورودی نادرست'}), status=400,
                    content_type='application/json; charset=utf8')
            ros.parrot_command_type.publish(str(commandType))
            return HttpResponse("", status=200, content_type='application/json; charset=utf8')

        except (ValueError, json.JSONDecodeError):
            return HttpResponse(json.dumps({'detail': 'ورودی نادرست'}), status=400,
                                content_type='application/json; charset=utf8')

    @list_route(methods=['post'], permission_classes=[StartedParrot])  # auth
    def perform(self, request):
        try:
            data = json.loads(codecs.decode(request.body, 'utf-8'))

            commandID = data['commandID']
            command = self.queryset.get(pk=commandID)
            ros.parrot_command_name.publish(str(command.name))
            if (command.tag == "P_V"):
                ros.parrot_voice_commands.publish(command.voice_file.path)
            else:
                ros.parrot_command.publish(str(command.arg))
            return HttpResponse("", status=200, content_type='application/json; charset=utf8')

        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'detail': 'چنین دستوری یافت نشد'}), status=400,
                                content_type='application/json; charset=utf8')
        except (ValueError, json.JSONDecodeError):
            return HttpResponse(json.dumps({'detail': 'ورودی نادرست'}), status=400,
                                content_type='application/json; charset=utf8')

    @list_route(methods=['get'], permission_classes=[StartedParrot])  # auth
    def stop(self, request):
        request.user.current_session().change_stage(settings.DONE_STAGE)
        ros.stage_info.publish("stop_test")
        return HttpResponse(json.dumps(""), status=200,
                            content_type='application/json; charset=utf8')


class Diagnosecommands(viewsets.GenericViewSet):
    authentication_classes = (PersonAuthentication,)
    permission_classes = (IsLogin)


    @list_route(methods=['post']) #auth
    def expertsystem(self,request):  
        try:
            data = json.loads(codecs.decode(request.body, 'utf-8'))
            session = request.user.current_session()
            session.expertsystem_judgement =  data['judgement']   
            session.save()                   
            return HttpResponse("", status=200,
                                content_type='application/json; charset=utf8')
        except(ValueError, json.JSONDecodeError):
            return HttpResponse(json.dumps({'detail': 'ورودی نادرست'}), status=400,
                                content_type='application/json; charset=utf8')



class ToyCarData(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.generics.GenericAPIView):
    queryset = models.ToyCar.objects.all()
    serializer_class = serializer.toycar_serializer
    permission_classes = (AnyActiveSessions, AnyAtGameStage)
    authentication_classes = ()

        
    def perform_create(self, serializer):
        user_session = models.Patient.objects.get(login_status= True).current_session()
        serializer.save(session= user_session)
        
    def post(self, request, *args, **kwargs):
    #    print(request.body)
        try:
            return self.create(request, *args, **kwargs)
        except IntegrityError: 
                return HttpResponse(json.dumps({'detail': 'Data for this timestamp were already sent'}), status=400,
                                content_type='application/json; charset=utf8')


    
#####           __________________________________________  AUTH _____________________________________________


from .models import Patient
from rest_framework import authentication
from rest_framework import exceptions
from .token import decodeToken,generateToken
from time import time
import json
import codecs
from django.http import HttpResponse
from AILab.settings import AUTH_TIME_DELTA as timeDelta
from website.serializer import person_serializer
from django.views.decorators.csrf import csrf_exempt
from .authentication import decode_and_check_auth_token

@csrf_exempt
def obtain_token(request):
    try:
        data=json.loads(codecs.decode(request.body,'utf-8'))
        person_id = data['person_id']
    except (KeyError, ValueError, json.JSONDecodeError):
        return HttpResponse(json.dumps({'detail': 'ورودی نادرست'}), status=400,
                            content_type='application/json; charset=utf8')

    try:
        user = Patient.objects.get(person_id = person_id)
    except Patient.DoesNotExist:
        return HttpResponse(json.dumps({"errors":"کاربری با این مشخصات وجود ندارد"}), status=401, content_type='application/json; charset=utf8')

    try:
        login_person = Patient.objects.get(login_status=True , last_activity__gt=time()-timeDelta)
        if not (login_person.person_id == person_id):
            return HttpResponse(json.dumps({'detail': 'فرد دیگری وارد شده است'}), status=400,
                                content_type='application/json; charset=utf8')
    except Patient.DoesNotExist:
        pass

    data={'id': user.id}
    
    for another_user in Patient.objects.filter(login_status=True):
        another_user.login_status=False
        if another_user.check_session():
            another_user.end_session()
        another_user.save()

    token = generateToken(data)
    user.last_activity = time()    
    user.login_status = True
    user.save()
    if user.check_session():
        user.resume_session()

    return HttpResponse(json.dumps({'token': token, 'id':user.id}), status=200,
                    content_type='application/json; charset=utf8')


@csrf_exempt
def verify_token(request):
    try:
        user = PersonAuthentication.verify(None, request)[0]
        return HttpResponse(json.dumps({"login_status": user.login_status}), status=200, content_type='application/json; charset=utf8')
    
    except exceptions.AuthenticationFailed as e: 
        return HttpResponse(json.dumps({"errors": str(e)}), status=400, content_type='application/json; charset=utf8')


@csrf_exempt
def remove_token(request):
    try:
        user = PersonAuthentication.authenticate(None, request)[0]
        user.login_status = False
        user.last_activity = time()
        user.save()
        if user.check_session():
            user.end_session()  # pause_session is also implemented
        return HttpResponse(json.dumps({"message": "logout complete"}), status=200,
                            content_type='application/json; charset=utf8')

    except exceptions.AuthenticationFailed as e:
        return HttpResponse(json.dumps({"errors":"کاربری با این مشخصات وارد نشده"}), status=400, content_type='application/json; charset=utf8')


def index(request,path):
    with open("./index.html") as index_file:
        return HttpResponse(index_file,status=200)  