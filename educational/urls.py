from django.urls import path

from . import views

urlpatterns = [

    path('report_card/', views.report_card),
    path('rollcall/', views.rollcall),
    path('courseInfo/', views.courses_info),
    path('average_of_professor/', views.Averege_of_professor.as_view()),
    path('high_degree_professor/', views.High_degree_professor.as_view()),
]