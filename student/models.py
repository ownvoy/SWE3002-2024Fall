from django.db import models

from skku.models import Subject


class Academic(models.Model):
    student_id = models.IntegerField(primary_key=True)
    student_name = models.CharField(max_length=50)
    student_grade = models.IntegerField()
    major = models.CharField(
        max_length=100,
    )
    double_major = models.CharField(max_length=100, null=True, blank=True)
    triple_major = models.CharField(max_length=100, null=True, blank=True)

class Preference(models.Model):
    student_id = models.ForeignKey(Academic, on_delete=models.CASCADE, primary_key=True)
    instructor = models.CharField(max_length=50, null=True)
    morningclass = models.BooleanField()
    courseRatio = models.FloatField()


class Mandatory(models.Model):
    student_id = models.ForeignKey(Academic, on_delete=models.CASCADE, primary_key=True)
    course = models.CharField(max_length=50, null=True)
    credit = models.IntegerField()
    time = models.CharField(max_length=50, null=True)
    five_days_a_week = models.IntegerField(null=True)


class History(models.Model):
    history_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Academic, on_delete=models.CASCADE, db_column='student_id', to_field='student_id')
    course_id = models.ForeignKey(Subject, on_delete=models.CASCADE, db_column='course_id', to_field='course_id')
    semester = models.CharField(max_length=50)

# Create your models here.
