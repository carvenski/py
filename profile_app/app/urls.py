from django.conf.urls import url

from . import views

urlpatterns = [
    url('myprofile_switch', views.myprofile_switch),
    url('test', views.test),
]