import json
from django.views import View
from django.db.models import Count
from django.shortcuts import render
from django.core import serializers
from .models import *
from django.http import HttpResponse, JsonResponse

from .models import *

def serialize_data(datas):
    result = []
    for data in datas:
        result.append(data)
    result_dictionary = {
        "data": result
    }
    return HttpResponse(json.dumps(result_dictionary), content_type="application/json")


class TakeCourse(View):

    def put(self, request, *args, **kwargs):
        student = Student.objects.get(studentNo=request.GET.get("studentNo"))
        date = request.GET.get("date")
        course_code1 = request.GET.get("course_code1")
        course_group1 = request.GET.get("course_group1")
        course_subject1 = request.GET.get("course_subject1")
        this_term = Term.objects.last()
        start_selection_unit_date = this_term.selection_unit_start_date
        end_selection_unit_date = this_term.selection_unit_end_date
        if not (start_selection_unit_date < date < end_selection_unit_date):
            error_message = {

                "error": "You can't take courses today"
            }
            return JsonResponse(error_message)

        if course_code1 is not None and course_group1 is not None and\
            course_subject1 is not None:
                course = Course.objects.get(course_code1)
                new_lesson = TakeCourses(
                                            student_grade=None,
                                            professor_grade=None,
                                            studentNo=student,
                                            course=course
                                        )
                new_lesson.save()



class EntranceFieldStudent(View):

    def get(self, request, *args, **kwargs):
        entranceYear = request.GET.get("entranceYear")
        field = request.GET.get("field")
        if not Student.objects.filter(entranceYear=entranceYear).exists() or \
                not Student.objects.filter(deptNo__field=field).exists():
            error_message = {

                "error": "Invalid input"
            }
            return JsonResponse(error_message)

        students = Student.objects.filter(entranceYear=request.GET.get("entranceYear"),
                                          deptNo__field=request.GET.get("field")) \
            .values(
            'studentNo', 'firstName', 'lastName', 'email', 'phoneNumber',
            'supervisor__firstName', 'supervisor__lastName', 'gpa'
        )

        return serialize_data(students)


class CourseSchedule(View):

    def get(self, request, *args, **kwargs):
        student_no = request.GET.get("studentNo")
        if not Student.objects.filter(studentNo=student_no).exists():
            error_message = {

                "error": "Invalid student number"
            }
            return JsonResponse(error_message)

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
                           'course_prof_firstName': course_prof_firstName,
                           'course_prof_lastName': course_prof_lastName})

        re = {
            "data": result
        }
        return HttpResponse(json.dumps(re), content_type="application/json")


