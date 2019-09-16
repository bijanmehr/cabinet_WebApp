from django.conf.urls import url,include
from django.urls import path
from website import views
from rest_framework.routers import SimpleRouter
from website.views import obtain_token,verify_token,remove_token

router = SimpleRouter()
router.register('stage/game',views.GameCommands,'Game')
router.register('stage/wheel',views.WheelCommands,'Wheel')
router.register('stage/parrot',views.ParrotCommands,'Parrot')
router.register('stage/diagnose',views.Diagnosecommands,'Diagnose')
router.register('stage', views.StageView, 'Stage')
router.register('session', views.SessionView, 'Session')
# router.register('eval/toycar', views.ToyCarData, 'ToyCar')

urlpatterns = [
    url(r'auth/login', obtain_token),
    url(r'auth/check', verify_token),
    url(r'auth/logout', remove_token),
    path('user/',views.UserProfileList.as_view()),
    path('properties/',views.Properties.as_view()),
    path('toycar', views.ToyCarData.as_view()),
    url('', include(router.urls)),
]
