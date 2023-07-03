from django.shortcuts import render
import json
from django.views import View
from django.db.models import Count
from django.shortcuts import render
from django.core import serializers
from .models import *
from django.http import HttpResponse, JsonResponse

# Create your views here.
def leisure_classes(request):
    leisureclasses = LeisureClass.objects\
        .values('leisure_class__SportName','leisure_class__SportPrice','leisure_class__SportCapacity','l_from',
                'l_to','l_time','day1','day2')
    result = []
    for x in leisureclasses:
        SportName = x['leisure_class__SportName']
        SportPrice = x['leisure_class__SportPrice']
        SportCapacity = x['leisure_class__SportCapacity']
        l_from = str(x['l_from'])
        l_to = str(x['l_to'])
        l_time = str(x['l_time'])
        day1 = x['day1']
        day2 = x['day2']
        result.append({'SportName': SportName, 'SportPrice': SportPrice, 'SportCapacity': SportCapacity,
                       'from' : l_from,'to': l_to,'time': l_time,'Sport_day1' : day1,'Sport_day2': day2})
    re = {
        "data": result
    }

    return HttpResponse(json.dumps(re), content_type="application/json")



class Reservebook(View):

    def put(self, request, *args, **kwargs):

        body = json.loads(request.body)
        research_id = body['research_id']
        title = body['title']
        r_from = body['r_from']
        r_to = body['r_to']
        studentNo= body['studentNo']

        if Research.objects.filter(research_id=research_id, title=title).exists():
            research = Research.objects.get(research_id=research_id,title=title)
            student = Student.objects.get(studentNo=studentNo)
            new_book_reservation = ResearchReservation(
                                                    r_from = r_from ,
                                                    r_to = r_to,
                                                    research = research,
                                                    studentNo = student
                                                   )
            new_book_reservation.save()

            book_reservations = ResearchReservation.objects\
                .values('research__title', 'research','r_from', 'r_to', 'studentNo__studentNo')
            result = []
            for x in book_reservations:
                title = x['research__title']
                book_id = x['research']
                date_from = str(x['r_from'])
                date_to = str(x['r_to'])
                studentNo = x['studentNo__studentNo']
                result.append({'research__title': title, 'research': book_id,
                               'r_from': date_from,'r_to': date_to,'studentNo' : studentNo})

            re = {
                "data": result
            }
            return HttpResponse(json.dumps(re), content_type="application/json")

        else:

            return HttpResponse('Research not found', status=404)




