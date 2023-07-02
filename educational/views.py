import json
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import *

from django.db.models import F

def serialize_data(datas):
    result = []
    for data in datas:
        result.append(data)
    result_dictionary = {
        "data": result
    }
    return HttpResponse(json.dumps(result_dictionary), content_type="application/json")


class Report_card(View):
    def get(self, request, *args, **kwargs):
        # Code for GET method
        student_no = request.GET.get("studentNo")
        if not Student.objects.filter(studentNo=student_no).exists():
            error_message = {

                "error": "Invalid student number"
            }
            return JsonResponse(error_message)

        takecourses = TakeCourses.objects.filter(studentNo=student_no) \
            .filter(course__is_digital_signature=1) \
            .annotate(
            grade=F('student_grade'),
            lastName=F('course__profNo__lastName'),
            firstName=F('course__profNo__firstName'),
            subject=F('course__course_subject')
        ).values(
            'course',
            'lastName',
            'firstName',
            'subject',
            'grade'
        )
        return serialize_data(takecourses)


def courses_info(request):
    coursesinfo = Course.objects \
        .values('course_code', 'course_subject', 'profNo__firstName', 'profNo__lastName', 'classNo', 'deptNo')
    return serialize_data(coursesinfo)


def rollcall(request):
    student_no = request.GET.get("studentNo")

    if not Student.objects.filter(studentNo=student_no).exists():
        error_message = {

            "error": "Invalid student number"
        }
        return JsonResponse(error_message)

    absent = RollCall.objects \
        .filter(studentNo=student_no, isPresent=0) \
        .values('session__course') \
        .annotate(count=Count('session__course')).values('session__course', 'session__course__course_subject',
                                                         'count', )

    return serialize_data(absent)


def professor_schedule(request):
    first_name = request.GET.get("firstName")
    last_name = request.GET.get("lastName")

    if not Professor.objects.filter(firstName=first_name, lastName=last_name).exists():
        error_message = {
            "error": "There is no professor with such a name"
        }
        return JsonResponse(error_message)

    professor_No = Professor.objects.filter(firstName=first_name, lastName=last_name).values('personnelCode')
    schedual = Course.objects.filter(profNo=professor_No) \
        .values('course_subject', 'courseschedule__course_day', 'courseschedule__course_time')

    result = []
    for course in schedual:
        Name = course['course_subject']
        Day = course['courseschedule__course_day']
        Time = str(course['courseschedule__course_time'])

        result.append({'Name': Name, 'Day': Day, 'Time': Time})

    result_dictionary = {
        "data": result
    }
    return HttpResponse(json.dumps(result_dictionary), content_type="application/json")


def exam_schedule(request):
    a = TakeCourses.objects \
        .filter(studentNo=request.GET.get("studentNo")) \
        .values('course', 'course__course_subject')

    result = []
    for x in a:
        result.append(x)
    print(result)
    re = {
        "data": result
    }

    return HttpResponse(json.dumps(re), content_type="application/json")
