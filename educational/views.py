import json

from django.db.models import Count
from django.shortcuts import render
from django.core import serializers
from .models import *
from django.http import HttpResponse, JsonResponse

from .models import *

def entrance_field_student(request):
    students = Student.objects.filter(entranceYear=request.GET.get("entranceYear"), deptNo__field=request.GET.get("field"))\
                        .values(
                                    'studentNo', 'firstName', 'lastName', 'email', 'phoneNumber',
                                    'supervisor__firstName', 'supervisor__lastName', 'gpa'
                                )

    result = []
    for x in students:
        result.append(x)
    print(result)
    re = {
        "data": result
    }
    return HttpResponse(json.dumps(re), content_type="application/json")



def course_schedule(request):
    courses = TakeCourses.objects.filter(studentNo=request.GET.get("studentNo")) \
                .values(
                         'course__course_group', 'course__course_subject',
                         'course__classNo', 'course__profNo__firstName',
                         'course__profNo__lastName', 'course__courseschedule__course_day',
                         'course__courseschedule__course_time'
                        )


    result = []
    for x in courses:
        course_group = x['course__course_group']
        course_subject = x['course__course_subject']
        course_day = x['course__courseschedule__course_day']
        course_time = str(x['course__courseschedule__course_time'])
        course_classNo = x['course__classNo']
        course_prof_firstName = x['course__profNo__firstName']
        course_prof_lastName = x['course__profNo__lastName']
        result.append({'course_group': course_group, 'course_subject': course_subject, 'course_day': course_day,
                       'course_time': course_time, 'course_classNo': course_classNo,
                       'course_prof_firstName' : course_prof_firstName, 'course_prof_lastName': course_prof_lastName})

    re = {
        "data": result
    }
    return HttpResponse(json.dumps(re), content_type="application/json")


def report_card(request):
    # absent = RollCall.objects\
    #         .filter(studentNo=request.GET.get("studentNo"))\
    #         .filter(isPresent=0).values('session__course')\
    #         .annotate(count=Count('session__course')).values('session__course__course_subject', 'count')
    takecourses = TakeCourses.objects.filter(studentNo=request.GET.get("studentNo"))\
                  .filter(course__is_digital_signature=1)\
                  .values(
                        'course', 'course__course_subject', 'course__profNo__firstName',
                        'course__profNo__lastName', 'student_grade'
                        )

    result = []
    for x in takecourses:
        result.append(x)
    print(result)
    re = {
        "data": result
    }
    return HttpResponse(json.dumps(re), content_type="application/json")


def rollcall(request):
    absent = RollCall.objects\
            .filter(studentNo=request.GET.get("studentNo"))\
            .filter(isPresent=0).values('session__course')\
            .annotate(count=Count('session__course')).values('session__course__course_subject', 'count')

    result = []
    for x in absent:
        result.append(x)
    print(result)
    re = {
        "data": result
    }
    return HttpResponse(json.dumps(re), content_type="application/json")


def courses_info(request):
    coursesinfo = Course.objects\
                  .values('course_code', 'course_subject', 'profNo__firstName', 'profNo__lastName', 'classNo', 'deptNo')
    result = []
    for x in coursesinfo:
        result.append(x)
    print(result)
    re = {
        "data": result
    }

    return HttpResponse(json.dumps(re), content_type="application/json")
