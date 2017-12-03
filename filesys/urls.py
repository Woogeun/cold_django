from django.conf.urls import url
from . import views

urlpatterns = [url(r'^file_list/$', views.file_list, name='file_list'), url(r'^upload/$', views.upload, name='upload'), url(r'^download/$', views.download, name='download')]