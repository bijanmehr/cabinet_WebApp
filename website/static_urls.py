from django.conf.urls import url,include
from django.urls import path
from website import views

urlpatterns = [
    url(r'.*', views.front_static),
]
