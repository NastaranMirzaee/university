from django.db import models
from educational.models import *

class Food(models.Model):
    food_id = models.IntegerField(primary_key=True)
    food_name = models.CharField(unique=True, max_length=45)
    meal = models.CharField(max_length=45)
    price = models.IntegerField()
    students = models.ManyToManyField(Student, through='FoodReservation')


class FoodReservation(models.Model):
    studentNo = models.ForeignKey(Student, on_delete=models.CASCADE)
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE)
    food_reservation_date = models.DateField()


class Sport(models.Model):
    sport_id = models.IntegerField(primary_key=True)
    SportPrice = models.IntegerField()
    SportCapacity = models.CharField(max_length=45)
    SportName = models.CharField(max_length=45, null=True)


class Pool(models.Model):
    address = models.CharField(max_length=100, null=True)
    pool = models.ForeignKey(Sport, on_delete=models.CASCADE, primary_key=True)
    students = models.ManyToManyField(Student, through='PoolReservation')


class PoolReservation(models.Model):
    poolReservation_id = models.IntegerField(primary_key=True)
    from_field = models.TimeField(null=True)
    to_field = models.TimeField(null=True)
    date_pool = models.DateField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)


class LeisureClass(models.Model):
    l_from = models.DateField(null=True)
    l_to = models.DateField(null=True)
    l_time = models.TimeField(null=True)
    day1 = models.CharField(max_length=45, null=True)
    day2 = models.CharField(max_length=45, null=True)
    leisure_class = models.ForeignKey(Sport, on_delete=models.CASCADE, primary_key=True)
    students = models.ManyToManyField(Student, through='RegisterLeisureClass')


class RegisterLeisureClass(models.Model):
    registerLeisureClass_id = models.IntegerField(primary_key=True)
    studentNo = models.ForeignKey(Student, on_delete=models.CASCADE)
    leisure_class = models.ForeignKey(LeisureClass, on_delete=models.CASCADE)


class Research(models.Model):
    research_id = models.IntegerField(primary_key=True)
    author = models.CharField(max_length=45, null=True)
    title = models.CharField(max_length=45, null=True)
    book_flag = models.BooleanField(null=True)
    paper_flag = models.BooleanField(null=True)
    students = models.ManyToManyField(Student, through='ResearchReservation')


class ResearchReservation(models.Model):
    r_from = models.DateField(null=True)
    r_to = models.DateField(null=True)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    studentNo = models.ForeignKey(Student, on_delete=models.CASCADE)






