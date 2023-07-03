import json

from django.db.models import Count
from django.shortcuts import render
from django.core import serializers
from .models import *
from django.http import HttpResponse, JsonResponse

from .models import *




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

def exam_schedule(request):
    # examschedule = Course.objects \
    #     .filter(studentNo=request.GET.get("studentNo")) \
    #     .values('course_subject', 'examDate ', 'examTime')
    a = TakeCourses.objects\
    .filter(studentNo=request.GET.get("studentNo"))\
    .values('course','course__course_subject','course__examDate','course__examTime')


    result = []
    for x in a:
        course = x['course']
        course_subject = x['course__course_subject']
        course_date = str(x['course__examDate'])
        course_time = str(x['course__examTime'])
        result.append({'course': course,'course_subject': course_subject, 'course_date': course_date,
                       'course_time': course_time, })
    re = {
        "data": result
    }

    return HttpResponse(json.dumps(re), content_type="application/json")
def session_topic(request):
    sessiontopic = Session.objects \
        .filter(course__course_subject=request.GET.get("course_subject")) \
        .values('course__course_subject','session_date','topic')
    result = []
    for x in sessiontopic:
        course_subject = x['course__course_subject']
        session_date = str(x['session_date'])
        session_topic = (x['topic'])
        result.append({ 'course_subject': course_subject, 'session_date': session_date,
                       'session_topic': session_topic, })
    re = {
        "data": result
    }

    return HttpResponse(json.dumps(re), content_type="application/json")
