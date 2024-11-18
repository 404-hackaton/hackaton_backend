from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('user-group-members/<str:user_id>/', views.user_group_members, name='usergroup_members'),
    path('<str:user_id>/schedule/<str:date>', views.user_group_members, name='usergroup_members'),
    path('user/<str:user_id>', views.user_data, name='user_data'),
    path('schedule/<str:user_id>/<str:date>', views.schedule_day, name='schedule_day'),
    path('schedule/<str:user_id>/<str:date>', views.schedule_day, name='schedule_day'),
    path('attendence/<str:user_id>/<str:date>', views.schedule_day, name='attendence_day'),
]
