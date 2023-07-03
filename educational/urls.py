from django.urls import path

from . import views

urlpatterns = [

    path('CourseSchedule', views.CourseSchedule.as_view()),
    path('EntranceFieldStudent', views.EntranceFieldStudent.as_view()),
    path('TakeCourse', views.TakeCourse.as_view()),
    path('DeleteCourseUnitSelection', views.DeleteCourseUnitSelection.as_view()),

]