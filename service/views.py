import json
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.views import View

from educational.views import serialize_data
from .models import *
from django.db.models import *




class ReservedFood(View):

    def get(self, request, *args, **kwargs):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        foods_info = FoodReservation.objects.filter(food_reservation_date__gt=start_date, food_reservation_date__lt=end_date)\
            .values('food_id__food_name').values('studentNo').annotate(count=Count('studentNo'))
        return serialize_data(foods_info)

