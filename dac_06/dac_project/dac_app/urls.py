from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("", views.upload_file),
    path("upload/",views.upload_success),
    path("download/",views.download)

]