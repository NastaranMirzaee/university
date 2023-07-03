import json
from datetime import datetime

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

def str_to_date(date_string):
    date_format = '%Y-%m-%d'

    try:
        date_obj = datetime.strptime(date_string, date_format).date()
        return date_obj
    except ValueError:
        return None

class PassedCourses(View):

    def get(self, request, *args, **kwargs):
        studentNo = request.GET.get("studentNo")
        passed_courses = TakeCourses.objects.filter(studentNo=studentNo, student_grade__gte=10)\
            .values('course__course_subject')

        return serialize_data(passed_courses)




class DeleteSingleCourse(View):

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        studentNo = body['studentNo']

        date = str_to_date(body['date'])
        course_code = body['course_code']
        course_subject = body['course_subject']

        this_term = Term.objects.last()
        end_selection_unit_date = this_term.selection_unit_end_date
        delete_lesson_end_date = this_term.delete_lesson_end_date
        # print("end_selection_unit_date",end_selection_unit_date)
        # print("date",date)
        # print("delete_lesson_end_date",delete_lesson_end_date)

        if not (end_selection_unit_date < date < delete_lesson_end_date):
            error_message = {

                "error": "You can't delete your course today",

            }
            return JsonResponse(error_message)

        if TakeCourses.objects.filter(
                                        studentNo__studentNo=studentNo,
                                        course__course_code=course_code,
                                        course__course_subject=course_subject
                                      ).exists():

            TakeCourses.objects.get(
                                        studentNo__studentNo=studentNo,
                                        course__course_code=course_code,
                                        course__course_subject=course_subject
                                    ).delete()

        This_term_lessons = TakeCourses.objects.filter(studentNo__studentNo=studentNo, course__term=this_term) \
            .values('studentNo__studentNo', 'course__course_subject')

        return serialize_data(This_term_lessons)



class DeleteCourseUnitSelection(View):

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        studentNo = body['studentNo']

        date = str_to_date(body['date'])
        course_code = body['course_code']
        course_subject = body['course_subject']

        this_term = Term.objects.last()
        start_selection_unit_date = this_term.selection_unit_start_date
        end_selection_unit_date = this_term.selection_unit_end_date
        if not (start_selection_unit_date < date < end_selection_unit_date):
            error_message = {

                "error": "You can't take course today"
            }
            return JsonResponse(error_message)

        if TakeCourses.objects.filter(
                                        studentNo__studentNo=studentNo,
                                        course__course_code=course_code,
                                        course__course_subject=course_subject
                                      ).exists():

            TakeCourses.objects.get(
                                        studentNo__studentNo=studentNo,
                                        course__course_code=course_code,
                                        course__course_subject=course_subject
                                    ).delete()

        This_term_lessons = TakeCourses.objects.filter(studentNo__studentNo=studentNo, course__term=this_term) \
            .values('studentNo__studentNo', 'course__course_subject')

        return serialize_data(This_term_lessons)

class TakeCourse(View):

    def put(self, request, *args, **kwargs):
        body = json.loads(request.body)
        studentNo = body['studentNo']
        student = Student.objects.get(studentNo=studentNo)
        date = str_to_date(body['date'])

        course_code = body['course_code1']
        course_subject = body['course_subject1']

        this_term = Term.objects.last()
        start_selection_unit_date = this_term.selection_unit_start_date
        end_selection_unit_date = this_term.selection_unit_end_date
        if not (start_selection_unit_date < date < end_selection_unit_date):
            error_message = {

                "error": "You can't take courses today"
            }
            return JsonResponse(error_message)

        if course_code is not None and course_subject is not None\
                and not TakeCourses.objects.filter(
                                                        studentNo__studentNo=studentNo,
                                                        course__course_code=course_code
                                                    ).exists():
                course = Course.objects.get(course_code=course_code)
                new_lesson = TakeCourses(
                                            student_grade=None,
                                            professor_grade=None,
                                            studentNo=student,
                                            course=course
                                        )
                new_lesson.save()


        This_term_lessons = TakeCourses.objects.filter(studentNo__studentNo=studentNo, course__term=this_term)\
            .values('studentNo__studentNo', 'course__course_subject')

        return serialize_data(This_term_lessons)



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


