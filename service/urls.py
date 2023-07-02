from django.urls import path

from . import views

urlpatterns = [

    path('ReserveFood', views.ReserveFood.as_view()),
    path('DeleteFood', views.DeleteFood.as_view())

]