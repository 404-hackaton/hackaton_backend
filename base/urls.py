from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # path('login', views.login, name='login'),
    path('user-group-members/<str:user_id>/', views.user_group_members, name='usergroup_members'),
    path('user/<str:user_id>', views.user_data, name='user_data'),
    path('schedule/<str:user_id>/<str:date>', views.schedule_day, name='schedule_day'),
    path('schedule-info/<str:schedule_id>', views.schedule_info, name='schedule_info'),
    path('attendence/<str:user_id>/<str:date>', views.attendence_day, name='attendence_day'),
    path('attendence-status/<str:user_id>/<str:date>', views.attendence_status_day, name='attendence_status_day'),
    path('gpa/<str:user_id>/', views.gpa_calculate, name='gpa_calculate'),
    path('fill', views.fill, name='fill'),
]
