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



class PersonAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if token == None :
            raise exceptions.AuthenticationFailed('Empty Token')

        try :
            data = decode_and_check_auth_token(token)
        except:
            raise exceptions.AuthenticationFailed('Invalid Token')
        try:
            user = Patient.objects.get(id = data['id'])
        except:
            raise exceptions.AuthenticationFailed('No Such User')
        if user.last_activity + timeDelta < time() or user.login_status == False:
            if user.login_status==True:
                user.login_status=False
                if user.check_session():
                    user.end_session()
                user.save()
            raise exceptions.AuthenticationFailed('Not Logged In')

        else:
            user.last_activity=time()
            user.save()
            return (user, None)

    def verify(self, request):
        token = request.META.get('HTTP_TOKEN')
        if token == None :
            raise exceptions.AuthenticationFailed('Empty Token')
        try :
            data = decode_and_check_auth_token(token)
        except:
            raise exceptions.AuthenticationFailed('Invalid Token')
        try:
            user = Patient.objects.get(id = data['id'])
            if user.last_activity + timeDelta < time() or user.login_status == False:
                if user.login_status==True:
                    user.login_status=False
                    if user.check_session():
                        user.end_session()
                    user.save()

        except:
            raise exceptions.AuthenticationFailed('No Such User')
        return (user, None)



class NoAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        return True
        
def decode_and_check_auth_token(token):
    data = decodeToken(token)
    id = data['id']
    return data
