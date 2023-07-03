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


def response(message):
    return HttpResponse(json.dumps(message), content_type="application/json")

#def error_message()


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
            lastName=F('course__profNo__lastName'),
            firstName=F('course__profNo__firstName'),
            subject=F('course__course_subject'),
            grade=F('student_grade'),
        ).values(
            'course',
            'lastName',
            'firstName',
            'subject',
            'grade'
        )
        return serialize_data(takecourses)


class Courses_info(View):

    def get(self, request, *args, **kwargs):
        coursesinfo = Course.objects \
            .annotate(
            course=F('course_code'),
            subject=F('course_subject'),
            lastName=F('profNo__lastName'),
            firstName=F('profNo__firstName'),
            department=F('deptNo__faculty'),
            classNumber=F('classNo')

        ).values(
            'course',
            'subject',
            'lastName',
            'firstName',
            'classNo',
            'deptNo'
        )
        return serialize_data(coursesinfo)


class Rollcall(View):

    def get(self, request, *args, **kwargs):
        student_no = request.GET.get("studentNo")
        if not Student.objects.filter(studentNo=student_no).exists():
            error_message = {

                "error": "Invalid student number"
            }
            return JsonResponse(error_message)

        absent = RollCall.objects \
            .filter(studentNo=student_no, isPresent=0) \
            .values('session__course') \
            .annotate(count=Count('session__course'))\
            .values('session__course', 'session__course__course_subject','count',)

        return serialize_data(absent)


class Professor_schedule(View):

    def get(self, request, *args, **kwargs):
        first_name = request.GET.get("firstName")
        last_name = request.GET.get("lastName")

        if not Professor.objects.filter(firstName=first_name, lastName=last_name).exists():
            error_message = {
                "error": "There is no professor with such a name"
            }
            return JsonResponse(error_message)

        professor = Professor.objects.get(firstName=first_name, lastName=last_name)
        professor_No = professor.personnelCode
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


class PersonInfo(View):
    def put(self, request, *args, **kwargs):
        body = json.loads(request.body)
        personId = body['id']
        record = None
        if Student.objects.filter(studentNo=personId).exists():
            record = Student.objects.get(studentNo=personId)
            print(record)

        elif Professor.objects.filter(personnelCode=personId).exists():
            record = Professor.objects.get(personnelCode=personId)
            print(record)

        if record is not None:
            if body['firstName'] is not None:
                record.firstName = body['firstName']

            if body['lastName'] is not None:
                record.lastName = body['lastName']

            record.save()
            return JsonResponse({"status": "succes"})

        else:
            error_message = {

                "error": "Invalid input number"
            }
            return JsonResponse(error_message)




        # if  body[''] is not None:
        # student_no = body['student_no']
        # record = Student.objects.get(studentNo=student_no)
        # record.firstName = body['firstName']
        # record.save()
        # return response({"status": "succes"})


