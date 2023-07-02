from django.urls import path
from django.views.decorators.http import require_http_methods

from . import views

urlpatterns = [
    path('report_card', views.Report_card.as_view()),
    path('rollcall/', views.rollcall),
    path('courseInfo/', views.courses_info),
    path('professorschedule/',views.professor_schedule),
]