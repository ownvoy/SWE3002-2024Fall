import copy
import json
from subject.models import Fix, SkkuSubject

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from django.views import View
from sql import SQL
from timetabling import Timetabling

from .models import Info

import hashlib


def get_color_class(course_id):
    if isinstance(course_id, int):
        course_id = str(course_id)
    hash_object = hashlib.md5(course_id.encode())
    return f"fixed-course{int(hash_object.hexdigest(), 16) % 13 + 1}"


class History(View):
    def get(self, request):
        student_id = request.session.get("student_id")

        # 로그인 시 학번 정보로 수강한 course_id 가져오기
        sql = SQL()
        course_ids = sql.get_history_of_student(student_id)
        print(course_ids)

        # 학번에 따른 수강가능한 과목 리스트 가져오기
        possible_subjects = sql.subject_available(student_id)
        possible_course_titles = list(
            {entry["course_title"] for entry in possible_subjects}
        )
        possible_course_titles_json = json.dumps(
            possible_course_titles, ensure_ascii=False
        )

        # course_id로 강의 이름 가져오기
        history_titles = list({sql.find_title_by_courseid(course_id) for course_id in course_ids})
        history_titles_json = json.dumps(history_titles, ensure_ascii=False)
        
        return render(request, "history.html", {"titles": history_titles_json, "subjects": possible_course_titles_json})

    def post(self, request):
        student_id = request.session.get("student_id", 0)
        subject = request.POST.get("subject")

        sql = SQL()
        # 입력받은 강의 이름으로 course_id 찾기
        course_ids = sql.find_courseids_by_title(subject)

        if course_ids == -1:
            return HttpResponseRedirect("/history/?alert=Invalid+subject+name")

        print("history post: ", course_ids)
        sql.register_subject_history(".", course_ids, student_id)
        return HttpResponseRedirect("/history/")

    def delete(self, request):
        try:
            data = json.loads(request.body)
            course_title = data.get("course_title")[:-1]
            student_id = request.session.get("student_id", 0)

            sql = SQL()
            course_ids = sql.find_courseids_by_title(course_title)
            success = sql.delete_history(student_id, course_ids)

            if success:
                return JsonResponse(
                    {"success": True, "message": "Course deleted successfully."}
                )
            else:
                return JsonResponse({"success": False, "message": "Failed to delete."})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)


class Registration(View):
    def get(self, request):
        return render(request, "registration.html")

    def post(self, request):
        login_id = request.POST.get("login_id")
        request.session["login_id"] = login_id
        login_password = request.POST.get("login_password")
        student_name = request.POST.get("student_name")
        student_id = request.POST.get("student_id")
        major = request.POST.get("major")
        double_major = request.POST.get("double_major")
        triple_major = request.POST.get("triple_major")
        student_grade = request.POST.get("student_grade")
        # double_major와 triple_major 값이 "X"이거나 빈칸일 때 None으로 처리
        double_major = None if not double_major else double_major
        triple_major = None if not triple_major else triple_major
        sql = SQL()
        result = sql.register_user(
            login_id,
            login_password,
            student_name,
            student_id,
            major,
            double_major,
            triple_major,
            student_grade,
        )

        if (result == -1):
            # 에러가 발생했을 때, 알림을 띄운 후 리다이렉트
            return HttpResponse("""
                <script>
                    alert('이미 존재하는 학번입니다. 다시 입력해주세요.');
                    window.location.href = '/registration/';  // 리다이렉트 할 URL
                </script>
            """)
        else:
            return HttpResponseRedirect("/")


all_time = [
    "Mon11",
    "Mon12",
    "Mon21",
    "Mon22",
    "Mon31",
    "Mon32",
    "Mon41",
    "Mon42",
    "Mon51",
    "Mon52",
    "Mon61",
    "Mon62",
    "Mon71",
    "Mon72",
    "Mon81",
    "Mon82",
    "Mon91",
    "Mon92",
    "Mon101",
    "Mon102",
    "Mon111",
    "Mon112",
    "Mon121",
    "Mon122",
    "Tue11",
    "Tue12",
    "Tue21",
    "Tue22",
    "Tue31",
    "Tue32",
    "Tue41",
    "Tue42",
    "Tue51",
    "Tue52",
    "Tue61",
    "Tue62",
    "Tue71",
    "Tue72",
    "Tue81",
    "Tue82",
    "Tue91",
    "Tue92",
    "Tue101",
    "Tue102",
    "Tue111",
    "Tue112",
    "Tue121",
    "Tue122",
    "Wed11",
    "Wed12",
    "Wed21",
    "Wed22",
    "Wed31",
    "Wed32",
    "Wed41",
    "Wed42",
    "Wed51",
    "Wed52",
    "Wed61",
    "Wed62",
    "Wed71",
    "Wed72",
    "Wed81",
    "Wed82",
    "Wed91",
    "Wed92",
    "Wed101",
    "Wed102",
    "Wed111",
    "Wed112",
    "Wed121",
    "Wed122",
    "Thu11",
    "Thu12",
    "Thu21",
    "Thu22",
    "Thu31",
    "Thu32",
    "Thu41",
    "Thu42",
    "Thu51",
    "Thu52",
    "Thu61",
    "Thu62",
    "Thu71",
    "Thu72",
    "Thu81",
    "Thu82",
    "Thu91",
    "Thu92",
    "Thu101",
    "Thu102",
    "Thu111",
    "Thu112",
    "Thu121",
    "Thu122",
    "Fri11",
    "Fri12",
    "Fri21",
    "Fri22",
    "Fri31",
    "Fri32",
    "Fri41",
    "Fri42",
    "Fri51",
    "Fri52",
    "Fri61",
    "Fri62",
    "Fri71",
    "Fri72",
    "Fri81",
    "Fri82",
    "Fri91",
    "Fri92",
    "Fri101",
    "Fri102",
    "Fri111",
    "Fri112",
    "Fri121",
    "Fri122",
]


class Login(APIView):
    # when get started button is clicked, this function is called
    def get(self, request):
        return render(request, "login.html")

    # when sign in button is clicked, this function is called
    # if user successfully signed in, we will find the course that user can take
    # Then, redirect to survey page
    def post(self, request):
        action = request.POST.get("action")
        if action == "signup":
            return HttpResponseRedirect("/registration/")

        login_id = request.POST.get("login_id")
        request.session["login_id"] = login_id
        login_password = request.POST.get("login_password")
        print(login_id, login_password)

        if login_id == "" or login_password == "":
            messages.error(request, "Please enter your login ID and password")
            return render(
                request, "login.html", {"message": "Please enter your ID and password"}
            )

        # using ORM
        user = Info.objects.filter(login_id=login_id).first()
        if user is None:
            messages.info(request, message="Password or ID is wrong")
            return render(request, "login.html", {"message": "Password or ID is wrong"})
        if user.login_password != login_password:
            messages.info(request, message="Password or ID is wrong")
            return render(request, "login.html", {"message": "Password or ID is wrong"})
        print(user)
        request.session["student_id"] = user.serializable_value("student_id")
        print(request.session["student_id"])
        sql = SQL()
        possible = sql.subject_available(request.session["student_id"])
        request.session["possible"] = possible
        return HttpResponseRedirect("/survey/")


class Survey(APIView):
    def get(self, request):
        login_id = request.session.get("login_id")
        student_id = request.session.get("student_id")
        print(student_id, "asdf")
        possible = request.session.get("possible")

        if login_id is None:
            return HttpResponseRedirect("/login/")
        sql = SQL()
        result = sql.return_userinfo(login_id)
        request.session["student_id"] = result[0]["student_id"]
        return render(request, "survey.html", {"user": result[0]})
        # using ORM
        # user = Info.objects.filter(login_id=login_id).first()

        # return render(request, 'survey.html', context={'user': user})

    # We will collect user's information and save it in database
    def post(self, request):
        action = request.POST.get("action")
        if action == "history":
            return HttpResponseRedirect("/history/")

        credit = request.POST.get("credit")
        print(credit)
        course = request.POST.get("course")
        density = request.POST.get("density")
        print(density)
        morning = request.POST.get("morning")
        print(morning)
        professor = request.POST.get("professor")
        print(professor)
        day_list = ["mon", "tue", "wed", "thu", "fri"]
        day_map = {"mon": "Mon", "tue": "Tue", "wed": "Wed", "thu": "Thu", "fri": "Fri"}
        mon = request.POST.get("mon")
        tue = request.POST.get("tue")
        wed = request.POST.get("wed")
        thu = request.POST.get("thu")
        fri = request.POST.get("fri")
        day_list = [mon, tue, wed, thu, fri]
        except_day = []
        for day in day_list:
            if day is not None:
                except_day.append(day_map[day])
        print(except_day)
        day_go = []
        for day in day_list:
            if day is not None:
                if day not in except_day:
                    day_go.append(day_map[day])

        day_str = ",".join(day_go)
        # list to concate string
        ratio = request.POST.get("ratio")
        print(ratio)
        sql = SQL()
        sql.insert_survey(
            request.session.get("login_id"),
            credit,
            course,
            density,
            morning,
            professor,
            day_str,
            ratio,
        )
        student_id = request.session.get("student_id")
        student_info = sql.student_info_join(student_id)[0]
        request.session["student_info"] = student_info

        return HttpResponseRedirect("/timetable/")


from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.views import APIView


@method_decorator(never_cache, name="dispatch")
class Timetable(APIView):
    # we will show user's timetable
    # class_list is the list of html class name
    # text_list is the list of  courses' name, professor, etc.
    def get(self, request):
        possible = request.session.get("possible")
        student_id = request.session.get("student_id")
        student_info = request.session.get("student_info")
        timetabling = Timetabling(student_info)
        fixed_courses = Fix.objects.filter(student_id=student_id).values_list(
            "course_id", flat=True
        )

        # course_id 목록에 맞는 SkkuSubject 테이블에서 모든 필드 정보를 가져오기
        fix_course = SkkuSubject.objects.filter(course_id__in=fixed_courses)

        # SkkuSubject의 모든 필드를 딕셔너리 형태로 변환하여 `course_info` 리스트에 추가
        fix_course_infos = [
            {
                field.name: getattr(subject, field.name)
                for field in subject._meta.fields
                if field.name != "_state"
            }
            for subject in fix_course
        ]

        # Django ORM이 추가한 _state 필드를 제거하여 순수한 필드만 남김
        timetable = timetabling.timetable(possible, fix_course_infos)
        text_dict = {}
        icampus = []

        for course in timetable:
            if "i-Campus" in course["campus"]:
                icampus.append(course)

        icam_text_dict = {}
        for course in icampus:
            icam_text_dict[course["course_title"]] = course["course_title"]
        icam_class_dict = {}
        for idx, course in enumerate(icampus):
            icam_class_dict[course["course_title"]] = (
                f"relative flex w-full text{str(idx+8)} adobe" + str(idx + 8)
                # f"relative flex w-full px-2 py-1 text{str(idx+8)} adobe" + str(idx + 8)
            )

        icam_text_list = icam_text_dict.values()
        icam_class_list = icam_class_dict.values()

        icam_zipped = zip(icam_text_list, icam_class_list)

        for t in all_time:
            text_dict[t] = " "

        for course in timetable:
            for idx, time in enumerate(course["classtime2"]):
                course_title_english = course["course_title_english"].split(" ")
                new_english_title = []
                for index, s in enumerate(course_title_english):
                    if index == 0:
                        new_english_title.append(s)
                    else:
                        if len(new_english_title[-1] + s) <= 18:
                            new_english_title[-1] = new_english_title[-1] + " " + s
                        else:
                            new_english_title.append(s)

                if idx == 0:
                    text_dict[time] = course["course_title"][0:20]
                elif idx == 1:
                    text_dict[time] = course["instructor"]
                elif idx == 2:
                    text_dict[time] = course["type_of_field"]
                elif idx == 3:
                    text_dict[time] = new_english_title[0]
                elif idx == 4:
                    if len(new_english_title) > 1:
                        text_dict[time] = new_english_title[1]
                elif idx == 5:
                    if len(new_english_title) > 2:
                        text_dict[time] = new_english_title[2]

        text_list = text_dict.values()

        class_dict = {}

        for t in all_time:
            class_dict[t] = "border-t border-r border-gray-400 h-8 w-full"
            if "122" in t:
                class_dict[t] += " border-b"

        for idx, course in enumerate(timetable):
            for idx2, t in enumerate(course["classtime2"]):
                if idx2 == 0:
                    class_dict[t] = (
                        "adobe"
                        + str(idx + 1)
                        + " "
                        + "w-full"  # 반응형 너비 설정
                        + " "
                        + "h-8"
                        + " "
                        + "font-semibold"
                        + " "
                        + "text"
                        + str(idx + 1)
                        + " "
                        + "pt-2 px-1"
                    )
                else:
                    class_dict[t] = (
                        "adobe"
                        + str(idx + 1)
                        + " "
                        + "w-full"
                        + " "
                        + "h-8"
                        + " "
                        + "text"
                        + str(idx + 1)
                        + " "
                        + "py-2 px-1 pb-2"
                    )

        class_list = class_dict.values()

        # print("aa")
        # print()
        # print(course["course_id"])

        id_dict = {}
        for t in all_time:
            id_dict[t] = " "

        for course in timetable:
            for idx, time in enumerate(course["classtime2"]):
                id_dict[time] = course["course_id"]

        id_list = id_dict.values()

        print(f"fixed-course:{fixed_courses}")
        zipped = zip(all_time, class_list, text_list, id_list)
        zipped_list = list(zip(all_time, class_list, text_list, id_list))
        # print(list(zipped))
        # 템플릿에서 사용하기 위해 다시 zip 형태로 변환
        updated_zipped = [
            (
                time,
                class_name
                + (
                    f" {get_color_class(course_id)}"
                    if course_id in fixed_courses
                    else ""
                ),
                text,
                course_id,
            )
            for i, (time, class_name, text, course_id) in enumerate(zipped_list)
        ]

        #
        # updated_zipped = [
        #     (
        #         time,
        #         class_name + (" fixed-course" if course_id in fixed_courses else ""),
        #         text,
        #         course_id,
        #     )
        #     for i, (time, class_name, text, course_id) in enumerate(zipped_list)
        # ]
        #
        # 템플릿에서 반복 사용 가능하도록 리스트 형태로 변환
        updated_zipped_list = list(updated_zipped)
        print(list(updated_zipped))
        print(updated_zipped)
        zipped2 = copy.deepcopy(updated_zipped_list)
        zipped3 = copy.deepcopy(updated_zipped_list)
        zipped4 = copy.deepcopy(updated_zipped_list)
        zipped5 = copy.deepcopy(updated_zipped_list)

        return render(
            request,
            "timetable.html",
            context={
                "timetable": timetable,
                "zipped": updated_zipped_list,
                "zipped2": zipped2,
                "zipped3": zipped3,
                "zipped4": zipped4,
                "zipped5": zipped5,
                "icampus": icam_zipped,
            },
        )

    def post(self, request):
        return render(request, "timetable.html")


# Create your views here.
