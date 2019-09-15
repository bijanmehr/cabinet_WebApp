from rest_framework import permissions
from time import time
from AILab.settings import AUTH_TIME_DELTA as timeDelta
from website import models, settings
class AnyActiveSessions(permissions.BasePermission):
    message = 'No user currently has an active session'

    def has_permission(self, request, view):
        return models.DiagnoseSession.check_active_session()

    def has_object_permission(self, request, view, obj):
       return self.has_permission(request,view)
 
class AnyAtGameStage(permissions.BasePermission):
    message = 'No user is currently at game stage'

    def has_permission(self, request, view):
        return models.Patient.current_patient().current_session().stage.name == settings.GAME_STAGE

    def has_object_permission(self, request, view, obj):
       return self.has_permission(request,view)


class IsLogin(permissions.BasePermission):
    message = 'Please login first'

    def has_permission(self, request, view):
        return request.user and request.user.last_activity+timeDelta > time() and request.user.login_status==True

    def has_object_permission(self, request, view, obj):
       return self.has_permission(request,view)

class StartedSession(permissions.BasePermission):
    message = 'You don\'t have any active sessions'
    permission_classes = (IsLogin, )
    def has_permission(self, request, view):
        return request.user.check_session()

    def has_object_permission(self, request, view, obj):
       return self.has_permission(request,view)
       
class NotStarted(permissions.BasePermission):
    message = 'you can\'t start game at this stage'
    permission_classes = (IsLogin, )
    def has_permission(self, request, view):
        return not request.user.check_session()

    def has_object_permission(self, request, view, obj):
       return self.has_permission(request,view)

class StartedGame(permissions.BasePermission):
    message = 'You are not at game stage'
    permission_classes = (IsLogin, )
    def has_permission(self, request, view):
        return request.user.check_session() and request.user.current_session().stage.name == settings.GAME_STAGE

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class StartedWheel(permissions.BasePermission):
    message = 'You are not at wheel stage'
    permission_classes = (IsLogin, )
    def has_permission(self, request, view):
        return request.user.check_session() and request.user.current_session().stage.name == settings.WHEEL_STAGE

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class StartedParrot(permissions.BasePermission):
    message = 'You are not at parrot stage'

    permission_classes = (IsLogin, )
    def has_permission(self, request, view):
        return request.user.check_session() and request.user.current_session().stage.name == settings.PARROT_STAGE

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

