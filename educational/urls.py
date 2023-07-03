from django.urls import path

from . import views

urlpatterns = [

    path('CourseSchedule', views.CourseSchedule.as_view()),
    path('EntranceFieldStudent', views.EntranceFieldStudent.as_view()),
    path('TakeCourse', views.TakeCourse.as_view()),
    path('DeleteCourseUnitSelection', views.DeleteCourseUnitSelection.as_view()),
    path('DeleteSingleCourse', views.DeleteCourseUnitSelection.as_view()),
    path('PassedCourses', views.PassedCourses.as_view()),
    path('TermPlan', views.TermPlan.as_view()),

]