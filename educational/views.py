import json
from service.models import *
from django.db.models import Count
from django.shortcuts import render
from django.core import serializers
from .models import *
from django.http import HttpResponse, JsonResponse
from django.views import View

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

class Averege_of_professor(View):
    def get(self, request, *args, **kwargs):
        average = Professor.objects\
                      .values('personnelCode', 'firstName', 'lastName').annotate(
                      average_grade=models.Avg('course__takecourses__student_grade'))

        result = []
        for x in average:
            result.append(x)
        re = {
            "data": result
        }

        return HttpResponse(json.dumps(re), content_type="application/json")


class High_degree_professor(View):
    def get(self, request, *args, **kwargs):
        professors = Professor.objects.filter(degree='professor') \
            .values('personnelCode', 'firstName', 'lastName', 'degree')

        result = []
        for x in professors:
            result.append(x)
            re = {
            "data": result
            }

        return HttpResponse(json.dumps(re), content_type="application/json")

    class Departman_manager(View):
        def get(self, request, *args, **kwargs):
            departmanmanager = Professor.objects.filter(department_manager_flag= True) \
                .values('personnelCode', 'firstName', 'lastName', 'departmentNo__field' , 'departmentNo')

            result = []
            for x in departmanmanager:
                result.append(x)
            print(result)
            re = {
                "data": result
            }

            return HttpResponse(json.dumps(re), content_type="application/json")


class Student_leisure_registration(View):
    def get(self, request, *args, **kwargs):
        StudentLeisureRegistration = Student.objects\
        .values('firstName', 'lastName', 'leisureclass__leisure_class__SportName')

        result = []
        for x in StudentLeisureRegistration:
            result.append(x)
            print(result)
            re = {
            "data": result
            }
        return HttpResponse(json.dumps(re), content_type="application/json")


class CurrentTermCoursesView(View):
    def get(self, request):
        term_id = '14012'
        courses = Course.objects.\
        filter(term__term_id=term_id)\
        .values( 'course_subject', 'course_code','profNo__firstName' ,'profNo__lastName' , 'term__term_id')
        result = []
        for x in courses:
            result.append(x)
        print(result)
        re = {
            "data": result
        }
        return HttpResponse(json.dumps(re), content_type="application/json")


def update_balance(request):
    update = Student.objects\
    .filter(studentNo=request.GET.get("studentNo")) \
    # .filter(balance=request.GET.get("studentNo")) \

            # student_id =  # Retrieve the student ID from request or any other source

    result = []
    for x in update:
        result.append(x)
    print(result)
    re = {
        "data": result
    }
    return HttpResponse(json.dumps(re), content_type="application/json")


def Assessment_professors (request):
    assessment = TakeCourses.objects\

    result = []
    for x in assessment:
        result.append(x)
    print(result)
    re = {
        "data": result
    }
    return HttpResponse(json.dumps(re), content_type="application/json")
