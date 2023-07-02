from django.db import models
from django.db import connection


class Department(models.Model):
    departmentNo = models.IntegerField(primary_key=True)
    field = models.CharField(max_length=45, null=True)
    faculty = models.CharField(max_length=45, null=True)


class Professor(models.Model):
    personnelCode = models.IntegerField(primary_key=True)
    nationalCode = models.CharField(unique=True, max_length=10)
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=12)
    email = models.CharField(max_length=45)
    address = models.CharField(max_length=100, null=True)
    lastEducationCertificate = models.CharField(max_length=45)
    gender = models.CharField(max_length=6)
    degree = models.CharField(max_length=45)
    supervisor_flag = models.BooleanField()
    department_manager_flag = models.BooleanField()
    departmentNo = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)


class Term(models.Model):
    term_id = models.IntegerField(primary_key=True)
    year = models.IntegerField(null=True)
    semesterNo = models.IntegerField(null=True)
    selection_unit_start_date = models.DateField(null=True)
    selection_unit_end_date = models.DateField(null=True)
    delete_lesson_end_date = models.DateField(null=True)


class Student(models.Model):
    studentNo = models.IntegerField(primary_key=True)
    nationalCode = models.CharField(unique=True, max_length=10)
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=12)
    email = models.CharField(max_length=45)
    address = models.CharField(max_length=100, null=True)
    entranceYear = models.IntegerField()
    gender = models.CharField(max_length=6)
    birthdate = models.DateField(null=True)
    nationality = models.CharField(max_length=45, null=True)
    gpa = models.FloatField(null=True)
    passed_credit = models.IntegerField(null=True)
    balance = models.IntegerField(null=True)
    taken_credit = models.IntegerField(null=True)
    deptNo = models.ForeignKey(Department, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Professor, on_delete=models.CASCADE)



class Course(models.Model):
    course_code = models.IntegerField(primary_key=True)
    course_group = models.IntegerField()
    course_subject = models.CharField(max_length=45)
    credit = models.IntegerField()
    classNo = models.CharField(max_length=45)
    examDate = models.DateField()
    examTime = models.TimeField()
    chart_presented_term = models.IntegerField()
    is_digital_signature = models.BooleanField()
    deptNo = models.ForeignKey(Department, on_delete=models.CASCADE)
    profNo = models.ForeignKey(Professor, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, through='TakeCourses')


class CourseSchedule(models.Model):
    cs_id = models.IntegerField(primary_key=True)
    course_time = models.TimeField(null=True)
    course_day = models.CharField(max_length=45, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)



class Session(models.Model):
    session_id = models.IntegerField(primary_key=True)
    session_No = models.IntegerField()
    session_date = models.DateField(null=True)
    topic = models.CharField(max_length=45, null=True)
    students = models.ManyToManyField(Student, through='RollCall')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class RollCall(models.Model):
    isPresent = models.BooleanField(null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    studentNo = models.ForeignKey(Student, on_delete=models.CASCADE)



class TakeCourses(models.Model):
    student_grade = models.FloatField(null=True)
    professor_grade = models.IntegerField(null=True)
    studentNo = models.ForeignKey(Student, on_delete=models.CASCADE, unique=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)



