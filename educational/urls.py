from django.urls import path

from . import views

urlpatterns = [

    path('report_card/', views.report_card),
    path('rollcall/', views.rollcall),
    path('courseInfo/', views.courses_info),
    path('CourseSchedule/', views.CourseSchedule.as_view()),
    path('EntranceFieldStudent', views.EntranceFieldStudent.as_view()),
]