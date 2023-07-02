from django.urls import path
from django.views.decorators.http import require_http_methods

from . import views

urlpatterns = [
    path('report_card', views.Report_card.as_view()),
    path('courseInfo', views.Courses_info.as_view()),
    path('rollcall', views.rollcall),
    path('professorschedule',views.professor_schedule),
]