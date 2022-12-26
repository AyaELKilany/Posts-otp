from .views import *
from django.urls import path

urlpatterns = [
    path('' , all_Users , name='all_Users'),
]

