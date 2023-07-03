from django.urls import path

from . import views

urlpatterns = [
    path('leisureclasses', views.leisure_classes),
    path('Reservebook', views.Reservebook.as_view()),
    ]