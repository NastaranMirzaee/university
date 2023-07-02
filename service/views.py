from django.http import HttpResponse, JsonResponse
import json
from django.views import View

from .models import *


class ReserveFood(View):

    @staticmethod
    def post(request, *args, **kwargs):
        student_no = request.GET.get("studentNo")
        food = request.GET.get("food")

        student = Student.objects.get(studentNo=student_no)
        food_id = Food.objects.get(food_name=food)
        new_food_reservation = FoodReservation(
                                                studentNo=student,
                                                food_id=food_id,
                                                food_reservation_date=request.GET.get("date")
                                               )
        new_food_reservation.save()

        food_reservations = FoodReservation.objects.values('studentNo__studentNo', 'food_id__food_name',
                                                           'food_reservation_date')
        result = []
        for x in food_reservations:
            studentNo = x['studentNo__studentNo']
            food = x['food_id__food_name']
            date = str(x['food_reservation_date'])
            result.append({'studentNo': studentNo, 'food': food, 'date': date})

        re = {
            "data": result
        }
        return HttpResponse(json.dumps(re), content_type="application/json")

class DeleteFood(View):

    @staticmethod
    def delete(request, *args, **kwargs):
        student_no = request.GET.get("studentNo")
        food = request.GET.get("food")
        date = request.GET.get("date")

        student = Student.objects.get(studentNo=student_no)
        food_id = Food.objects.get(food_name=food)
        FoodReservation.objects.get(studentNo=student, food_id=food_id, food_reservation_date=date).delete()

        food_reservations = FoodReservation.objects.values('studentNo__studentNo', 'food_id__food_name',
                                                           'food_reservation_date')
        result = []
        for x in food_reservations:
            studentNo = x['studentNo__studentNo']
            food = x['food_id__food_name']
            date = str(x['food_reservation_date'])
            result.append({'studentNo': studentNo, 'food': food, 'date': date})

        re = {
            "data": result
        }
        return HttpResponse(json.dumps(re), content_type="application/json")