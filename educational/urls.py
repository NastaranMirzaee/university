from django.urls import path

from . import views

urlpatterns = [

    path('report_card/', views.report_card),
    path('rollcall/', views.rollcall),
    path('courseInfo/', views.courses_info),
    path('courseSchedule/', views.course_schedule),
    path('sortStudent/', views.entrance_field_student),

]