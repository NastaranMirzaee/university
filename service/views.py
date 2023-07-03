from django.http import HttpResponse, JsonResponse
import json

from .models import *

def reserve_food(request):
    student = Student.objects.get(studentNo=request.GET.get("studentNo"))
    food_id = Food.objects.get(food_name=request.GET.get("food"))

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

    print(result)
    re = {
        "data": result
    }
    return HttpResponse(json.dumps(re), content_type="application/json")

def delete_food(request):
    student = Student.objects.get(studentNo=request.GET.get("studentNo"))
    food_id = Food.objects.get(food_name=request.GET.get("food"))
    date = request.GET.get("date")
    FoodReservation.objects.get(studentNo=student, food_id=food_id, food_reservation_date=date).delete()

    food_reservations = FoodReservation.objects.values('studentNo__studentNo', 'food_id__food_name',
                                                       'food_reservation_date')
    result = []
    for x in food_reservations:
        studentNo = x['studentNo__studentNo']
        food = x['food_id__food_name']
        date = str(x['food_reservation_date'])
        result.append({'studentNo': studentNo, 'food': food, 'date': date})

    print(result)
    re = {
        "data": result
    }
    return HttpResponse(json.dumps(re), content_type="application/json")