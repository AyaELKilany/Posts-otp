from .views import *
from django.urls import path

urlpatterns = [
    path('' , all_Users , name='all_Users'),
    path('<int:id>' , get_User , name='get_User'),
    path('create', create_User , name='create_user'),
    path('update' , update_User , name='update_user'),
    path('delete/<int:id>' , delete_User , name='delete_user'),
    path('staff',all_Staff , name='all_staff'),
]

