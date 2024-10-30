# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


#
# class LiberalArts(models.Model):
#     course_code = models.CharField(max_length=255, primary_key=True)
#     type_of_field = models.CharField(max_length=255, blank=True, null=True)
#     course_title = models.CharField(max_length=255, blank=True, null=True)
#     course_title_english = models.CharField(max_length=255, blank=True, null=True)
#     instructor = models.CharField(max_length=255, blank=True, null=True)
#     campus = models.CharField(max_length=255, blank=True, null=True)
#     degree_courses = models.CharField(max_length=255, blank=True, null=True)
#     classtime = models.CharField(max_length=255, blank=True, null=True)
#     type_of_class1 = models.CharField(max_length=255, blank=True, null=True)
#     credits_hrs_field = models.CharField(
#         max_length=255, db_column="credits(Hrs)", blank=True, null=True
#     )  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
#     type_of_class2 = models.CharField(max_length=255, blank=True, null=True)
#     remarks = models.CharField(max_length=255, blank=True, null=True)
#     type_of_class3 = models.CharField(max_length=255, blank=True, null=True)
#     semester = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = "subject_liberal arts"
#         unique_together = (("course_code", "semester"),)
#
#
# class Major(models.Model):
#     semester = models.CharField(max_length=255, blank=True, null=True)
#     major = models.CharField(max_length=255, blank=True, null=True)
#     college = models.CharField(max_length=255, blank=True, null=True)
#     degree_courses = models.CharField(max_length=255, blank=True, null=True)
#     course_code = models.CharField(max_length=255, primary_key=True)
#     course_title = models.CharField(max_length=255, blank=True, null=True)
#     course_title_english = models.CharField(max_length=255, blank=True, null=True)
#     instructor = models.CharField(max_length=255, blank=True, null=True)
#     campus = models.CharField(max_length=255, blank=True, null=True)
#     type_of_field2 = models.CharField(max_length=255, blank=True, null=True)
#     type_of_field3 = models.CharField(max_length=255, blank=True, null=True)
#     credits_hrs_field = models.CharField(
#         max_length=255, db_column="credits(Hrs)", blank=True, null=True
#     )  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
#     classtime = models.CharField(max_length=255, blank=True, null=True)
#     type_of_class1 = models.CharField(max_length=255, blank=True, null=True)
#     type_of_class2 = models.CharField(max_length=255, blank=True, null=True)
#     remarks = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = "major_subject"
#         unique_together = (("course_code", "semester", "major"),)
#
#
#
class SkkuSubject(models.Model):
    degree_courses = models.CharField(max_length=100, blank=True, null=True)
    type_of_field3 = models.CharField(max_length=100, blank=True, null=True)
    course_code = models.CharField(max_length=100)
    course_title = models.CharField(max_length=100)
    course_title_english = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100, blank=True, null=True)
    campus = models.CharField(max_length=100, blank=True, null=True)
    type_of_field2 = models.CharField(max_length=100, blank=True, null=True)
    credit = models.CharField(max_length=100)
    classtime = models.TextField(blank=True, null=True)
    type_of_class1 = models.CharField(max_length=100, blank=True, null=True)
    type_of_class2 = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=100, blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    semester = models.CharField(max_length=100)
    college = models.CharField(max_length=100, blank=True, null=True)
    type_of_field = models.CharField(max_length=100, blank=True, null=True)
    course_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "skku_subject"
        unique_together = (("course_code", "semester", "major"),)


class Fix(models.Model):
    fix_id = models.AutoField(primary_key=True)  # Primary key
    student_id = models.CharField(max_length=100)  # 학생 ID 필드
    course_id = models.ForeignKey(
        "SkkuSubject", on_delete=models.CASCADE
    )  # ForeignKey 설정

    class Meta:
        db_table = "fix"  # 테이블 이름을 'fix'로 지정
