from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Lesson_Days(models.Model):
    dayuz = models.CharField(max_length=255)
    dayeng = models.IntegerField()

    def __str__(self) -> str:
        return self.dayuz

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    money = models.IntegerField()
    lesson_days = models.ManyToManyField(Lesson_Days)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=255)
    money = models.IntegerField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    phone = models.IntegerField(unique=True)
    extra_phone = models.IntegerField(null=True, blank=True, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    location = models.CharField(max_length=255)


    def __str__(self) -> str:
        return self.name

class Pupil(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    phone = models.IntegerField(unique=True)
    extra_phone = models.IntegerField(null=True, blank=True, unique=True)
    debt = models.IntegerField(default=0)
    group = models.ManyToManyField(Group)
    date_joined = models.DateField(null=True, blank=True, auto_now=True)

    # def __str__(self) -> str:
    #     return self.name

class Director(models.Model):
    name = models.CharField(max_length=255)
    telegram_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Payment_A(models.Model):
    money = models.IntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE)


class Payment_B(models.Model):
    money = models.IntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Lesson(models.Model):
    time = models.DateField(auto_now=True)
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.BooleanField()

class Parents(models.Model):
    name = models.CharField(max_length=255)
    child = models.ManyToManyField(Pupil)
    tg_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name