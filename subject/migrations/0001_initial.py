# Generated by Django 4.1.3 on 2022-11-15 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Major",
            fields=[
                ("semester", models.CharField(blank=True, max_length=255, null=True)),
                ("major", models.CharField(blank=True, max_length=255, null=True)),
                ("college", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "degree_courses",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "course_code",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                (
                    "course_title",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "course_title_english",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("instructor", models.CharField(blank=True, max_length=255, null=True)),
                ("campus", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "type_of_field2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "type_of_field3",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "credits_hrs_field",
                    models.CharField(
                        blank=True, db_column="credits(Hrs)", max_length=255, null=True
                    ),
                ),
                ("classtime", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "type_of_class1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "type_of_class2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("remarks", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "db_table": "major_subject",
                "managed": False,
                "unique_together": {("course_code", "semester")},
            },
        ),
        migrations.CreateModel(
            name="LiberalArts",
            fields=[
                (
                    "course_code",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                (
                    "type_of_field",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "course_title",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "course_title_english",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("instructor", models.CharField(blank=True, max_length=255, null=True)),
                ("campus", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "degree_courses",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("classtime", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "type_of_class1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "credits_hrs_field",
                    models.CharField(
                        blank=True, db_column="credits(Hrs)", max_length=255, null=True
                    ),
                ),
                (
                    "type_of_class2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("remarks", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "type_of_class3",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("semester", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "db_table": "liberal arts_subject",
                "managed": False,
                "unique_together": {("course_code", "semester")},
            },
        ),
    ]
