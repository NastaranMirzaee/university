from django.urls import path

from . import views

urlpatterns = [

    path('reserveFood/', views.reserve_food)

]