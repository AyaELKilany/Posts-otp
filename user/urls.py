from .views import *
from django.utils import path , include

urlpatterns = [
    path('' , all_Users , name='all_Users'),
]