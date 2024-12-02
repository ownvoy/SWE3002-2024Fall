from django.test import TestCase
from .models import Subject

class SubjectModelTestCase(TestCase):
    
    def setUp(self):
        """테스트 전에 실행될 설정 코드"""
        # 기본 Subject 인스턴스를 생성하여 저장
        self.subject = Subject.objects.create(
            semester='2024 Fall',
            college='Engineering',
            major='Computer Science',
            degree_courses='Undergraduate',
            course_code='CS101',
            course_title='Introduction to Computer Science',
            course_title_english='Introduction to Computer Science',
            credit='3',
            classtime='MWF 10:00-11:00',
            instructor='Prof. John Doe',
            campus='Main',
            type_of_field2='Core',
            type_of_field3='Lecture',
            type_of_class1='Lecture',
            type_of_class2='Theory',
            remarks='No remarks'
        )
    
    def test_subject_creation(self):
        """Subject 모델의 필드가 올바르게 저장되는지 확인"""
        self.assertEqual(self.subject.semester, '2024 Fall')
        self.assertEqual(self.subject.college, 'Engineering')
        self.assertEqual(self.subject.major, 'Computer Science')
        self.assertEqual(self.subject.degree_courses, 'Undergraduate')
        self.assertEqual(self.subject.course_code, 'CS101')
        self.assertEqual(self.subject.course_title, 'Introduction to Computer Science')
        self.assertEqual(self.subject.course_title_english, 'Introduction to Computer Science')
        self.assertEqual(self.subject.credit, '3')
        self.assertEqual(self.subject.classtime, 'MWF 10:00-11:00')
        self.assertEqual(self.subject.instructor, 'Prof. John Doe')
        self.assertEqual(self.subject.campus, 'Main')
        self.assertEqual(self.subject.type_of_field2, 'Core')
        self.assertEqual(self.subject.type_of_field3, 'Lecture')
        self.assertEqual(self.subject.type_of_class1, 'Lecture')
        self.assertEqual(self.subject.type_of_class2, 'Theory')
        self.assertEqual(self.subject.remarks, 'No remarks')

    def test_unique_together_constraint(self):
        """unique_together 제약 조건이 제대로 동작하는지 확인"""
        # 동일한 `course_code`, `semester`, `major` 값을 가진 Subject를 다시 생성하면 오류가 발생해야 함
        with self.assertRaises(Exception):  # IntegrityError가 발생해야 합니다
            Subject.objects.create(
                semester='2024 Fall',
                college='Engineering',
                major='Computer Science',
                degree_courses='Undergraduate',
                course_code='CS101',  # 동일한 course_code
                course_title='Introduction to Computer Science',
                course_title_english='Introduction to Computer Science',
                credit='3',
                classtime='MWF 10:00-11:00',
                instructor='Prof. Jane Doe',
                campus='Main',
                type_of_field2='Core',
                type_of_field3='Lecture',
                type_of_class1='Lecture',
                type_of_class2='Theory',
                remarks='No remarks'
            )
    
    def test_subject_string_representation(self):
        """모델의 __str__ 메서드가 올바르게 동작하는지 확인"""
        # __str__ 메서드가 `name`을 반환하려고 하지만 `name` 필드는 존재하지 않으므로,
        # course_title을 반환하는 것으로 변경해야 합니다.
        self.assertEqual(str(self.subject), self.subject.course_title)
