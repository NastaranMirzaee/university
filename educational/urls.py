from django.urls import path

from . import views

urlpatterns = [

    path('CourseSchedule', views.CourseSchedule.as_view()),
    path('EntranceFieldStudent', views.EntranceFieldStudent.as_view()),
]