import operator
import random
import re
from random import randint

random.seed(randint(0, 19999))

morning = [
    "Mon11",
    "Mon12",
    "Tue11",
    "Tue12",
    "Wed11",
    "Wed12",
    "Thu11",
    "Thu12",
    "Fri11",
    "Fri12",
]

day_map = {"Mon": "월", "Tue": "화", "Wed": "수", "Thu": "목", "Fri": "금"}
time_map3 = {
    "월09:00-10:15": ["Mon11", "Mon12", "Mon21"],
    "월09:00-9:50": ["Mon11", "Mon12"],
    "월10:30-11:45": ["Mon22", "Mon31", "Mon32"],
    "월10:00-10:50": ["Mon21", "Mon22"],
    "월11:00-11:50": ["Mon31", "Mon32"],
    "월12:00-13:15": ["Mon41", "Mon42", "Mon51"],
    "월12:00-12:50": ["Mon41", "Mon42"],
    "월13:00-13:50": ["Mon51", "Mon52"],
    "월13:30-14:45": ["Mon52", "Mon61", "Mon62"],
    "월14:00-14:50": ["Mon61", "Mon62"],
    "월15:00-16:15": ["Mon71", "Mon72", "Mon81"],
    "월15:00-15:50": ["Mon71", "Mon72"],
    "월16:00-16:50": ["Mon81", "Mon82"],
    "월16:30-17:45": ["Mon82", "Mon91", "Mon92"],
    "월17:00-17:50": ["Mon91", "Mon92"],
    "월18:00-19:15": ["Mon101", "Mon102", "Mon111"],
    "월18:00-18:50": ["Mon101", "Mon102"],
    "월19:00-19:50": ["Mon111", "Mon112"],
    "월19:30-20:45": ["Mon112", "Mon121", "Mon122"],
    "월20:00-20:50": ["Mon121", "Mon122"],
    "화09:00-10:15": ["Tue11", "Tue12", "Tue21"],
    "화09:00-9:50": ["Tue11", "Tue12"],
    "화10:30-11:45": ["Tue22", "Tue31", "Tue32"],
    "화10:00-10:50": ["Tue21", "Tue22"],
    "화11:00-11:50": ["Tue31", "Tue32"],
    "화12:00-13:15": ["Tue41", "Tue42", "Tue51"],
    "화12:00-12:50": ["Tue41", "Tue42"],
    "화13:00-13:50": ["Tue51", "Tue52"],
    "화13:30-14:45": ["Tue52", "Tue61", "Tue62"],
    "화14:00-14:50": ["Tue61", "Tue62"],
    "화15:00-16:15": ["Tue71", "Tue72", "Tue81"],
    "화15:00-15:50": ["Tue71", "Tue72"],
    "화16:00-16:50": ["Tue81", "Tue82"],
    "화16:30-17:45": ["Tue82", "Tue91", "Tue92"],
    "화17:00-17:50": ["Tue91", "Tue92"],
    "화18:00-19:15": ["Tue101", "Tue102", "Tue111"],
    "화18:00-18:50": ["Tue101", "Tue102"],
    "화19:00-19:50": ["Tue111", "Tue112"],
    "화19:30-20:45": ["Tue112", "Tue121", "Tue122"],
    "화20:00-20:50": ["Tue121", "Tue122"],
    "수09:00-10:15": ["Wed11", "Wed12", "Wed21"],
    "수09:00-9:50": ["Wed11", "Wed12"],
    "수10:30-11:45": ["Wed22", "Wed31", "Wed32"],
    "수10:00-10:50": ["Wed21", "Wed22"],
    "수11:00-11:50": ["Wed31", "Wed32"],
    "수12:00-13:15": ["Wed41", "Wed42", "Wed51"],
    "수12:00-12:50": ["Wed41", "Wed42"],
    "수13:00-13:50": ["Wed51", "Wed52"],
    "수13:30-14:45": ["Wed52", "Wed61", "Wed62"],
    "수14:00-14:50": ["Wed61", "Wed62"],
    "수15:00-16:15": ["Wed71", "Wed72", "Wed81"],
    "수15:00-15:50": ["Wed71", "Wed72"],
    "수16:00-16:50": ["Wed81", "Wed82"],
    "수16:30-17:45": ["Wed82", "Wed91", "Wed92"],
    "수17:00-17:50": ["Wed91", "Wed92"],
    "수18:00-19:15": ["Wed101", "Wed102", "Wed111"],
    "수18:00-18:50": ["Wed101", "Wed102"],
    "수19:00-19:50": ["Wed111", "Wed112"],
    "수19:30-20:45": ["Wed112", "Wed121", "Wed122"],
    "수20:00-20:50": ["Wed121", "Wed122"],
    "목09:00-10:15": ["Thu11", "Thu12", "Thu21"],
    "목09:00-9:50": ["Thu11", "Thu12"],
    "목10:30-11:45": ["Thu22", "Thu31", "Thu32"],
    "목10:00-10:50": ["Thu21", "Thu22"],
    "목11:00-11:50": ["Thu31", "Thu32"],
    "목12:00-13:15": ["Thu41", "Thu42", "Thu51"],
    "목12:00-12:50": ["Thu41", "Thu42"],
    "목13:00-13:50": ["Thu51", "Thu52"],
    "목13:30-14:45": ["Thu52", "Thu61", "Thu62"],
    "목14:00-14:50": ["Thu61", "Thu62"],
    "목15:00-16:15": ["Thu71", "Thu72", "Thu81"],
    "목15:00-15:50": ["Thu71", "Thu72"],
    "목16:00-16:50": ["Thu81", "Thu82"],
    "목16:30-17:45": ["Thu82", "Thu91", "Thu92"],
    "목17:00-17:50": ["Thu91", "Thu92"],
    "목18:00-19:15": ["Thu101", "Thu102", "Thu111"],
    "목18:00-18:50": ["Thu101", "Thu102"],
    "목19:00-19:50": ["Thu111", "Thu112"],
    "목19:30-20:45": ["Thu112", "Thu121", "Thu122"],
    "목20:00-20:50": ["Thu121", "Thu122"],
    "금09:00-10:15": ["Fri11", "Fri12", "Fri21"],
    "금09:00-9:50": ["Fri11", "Fri12"],
    "금10:30-11:45": ["Fri22", "Fri31", "Fri32"],
    "금10:00-10:50": ["Fri21", "Fri22"],
    "금11:00-11:50": ["Fri31", "Fri32"],
    "금12:00-13:15": ["Fri41", "Fri42", "Fri51"],
    "금12:00-12:50": ["Fri41", "Fri42"],
    "금13:00-13:50": ["Fri51", "Fri52"],
    "금13:30-14:45": ["Fri52", "Fri61", "Fri62"],
    "금14:00-14:50": ["Fri61", "Fri62"],
    "금15:00-16:15": ["Fri71", "Fri72", "Fri81"],
    "금15:00-15:50": ["Fri71", "Fri72"],
    "금16:00-16:50": ["Fri81", "Fri82"],
    "금16:30-17:45": ["Fri82", "Fri91", "Fri92"],
    "금17:00-17:50": ["Fri91", "Fri92"],
    "금18:00-19:15": ["Fri101", "Fri102", "Fri111"],
    "금18:00-18:50": ["Fri101", "Fri102"],
    "금19:00-19:50": ["Fri111", "Fri112"],
    "금19:30-20:45": ["Fri112", "Fri121", "Fri122"],
    "금20:00-20:50": ["Fri121", "Fri122"],
}


class Timetabling:
    def __init__(self, student_info):
        self.course_must = student_info["course"]
        self.credit = student_info["credit"]
        self.student_grade = student_info["student_grade"]
        self.five_days_a_week = student_info["five_days_a_week"]
        self.morningclass = student_info["morningclass"]
        self.course_ratio = student_info["courseRatio"]
        self.instructor = student_info["instructor"]
        self.day_list = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        self.not_time = student_info["time"]
        self.exceptday = []
        self.recommend = []
        self.temp_credit = 0
        self.daycount = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0}

    # This function is deciding the day when the student goes to school.
    def school_day(self, possible):
        print("not time", self.not_time)
        print("day_list", self.day_list)

        remove_idx = []
        for i, day in enumerate(self.day_list):
            if day in self.not_time:
                remove_idx.append(i)
        remove_idx_reverse = sorted(remove_idx, reverse=True)
        for i in remove_idx_reverse:
            self.exceptday.append(self.day_list[i])
            self.day_list.pop(i)
        print("Possible day: ", self.day_list)
        if self.five_days_a_week == 0:
            random.shuffle(self.day_list)
            if len(self.day_list) == 5:
                for i in range(2):
                    for day in self.day_list:
                        if self.daycount[day] > 0:
                            continue
                        else:
                            self.day_list.remove(day)
                            self.exceptday.append(day)
                            break
            elif len(self.day_list) == 4:
                for day in self.day_list:
                    if self.daycount[day] > 0:
                        continue
                    else:
                        self.day_list.remove(day)
                        self.exceptday.append(day)
                        break
        # print(self.exceptday)
        remove_idx = []
        for del_day in self.exceptday:
            for idx, course in enumerate(possible):
                for each_time in course["classtime2"]:
                    if del_day in each_time:
                        if idx not in remove_idx:
                            remove_idx.append(idx)
                        break
        remove_idx_reverse = sorted(remove_idx, reverse=True)
        for idx in remove_idx_reverse:
            del possible[idx]
        return possible

    # If the student doesn't want to go to school in the morning, this function is removing the morning class.
    def morning(self, possible):
        if self.morningclass == 0:
            remove_idx = []
            for time in morning:
                for idx, course in enumerate(possible):
                    if time in course["classtime2"]:
                        if idx not in remove_idx:
                            remove_idx.append(idx)
            remove_idx_reverse = sorted(remove_idx, reverse=True)
            for idx in remove_idx_reverse:
                del possible[idx]
        return possible

    # This function is removing the duplicate class.
    def duplicate_remove(self, same_course, possible):
        remove_idx = []
        for idx, course in enumerate(possible):
            if same_course in course["course_title"]:
                if idx not in remove_idx:
                    remove_idx.append(idx)
        remove_idx_reverse = sorted(remove_idx, reverse=True)
        for idx in remove_idx_reverse:
            del possible[idx]
        return possible

    # This function is removing icampus class. But not used in this project.
    def icam_remove(self, possible):
        remove_idx = []
        for idx, course in enumerate(possible):
            if "i-Campus" in course["campus"]:
                if idx not in remove_idx:
                    remove_idx.append(idx)
        remove_idx_reverse = sorted(remove_idx, reverse=True)
        for idx in remove_idx_reverse:
            del possible[idx]
        return possible

    # This function is removing the liberal arts class.
    def liberal_remove(self, possible):
        remove_idx = []
        for idx, course in enumerate(possible):
            if course["type_of_field"] == "교양":
                if idx not in remove_idx:
                    remove_idx.append(idx)
        remove_idx_reverse = sorted(remove_idx, reverse=True)
        for idx in remove_idx_reverse:
            del possible[idx]
        return possible

    # This function is converting the time to timetable format.
    def preprocessing(self, possible):
        for course in possible:
            day = course["classtime"].split(" ,")
            time = []
            for d in day:
                for t in time_map3:
                    if t in d:
                        time += time_map3[t]
            course["classtime2"] = time
        return possible

    # This function set the credit of the class.
    def credit_classify(self):
        self.major_credit = int(self.credit * self.course_ratio)
        while self.major_credit % 3 != 0 and self.major_credit <= self.credit:
            self.major_credit += 1
        self.liberal_credit = self.credit - self.major_credit
        return 0

    def adjust_weight(self, user_time_map, time_day, time_class):
        time = time_day + time_class
        after_before = []
        if int(time_class) % 2 == 0:
            after_before.append(time_day + str(int(time_class) + 9))
            after_before.append(time_day + str(int(time_class) + 10))
            after_before.append(time_day + str(int(time_class) + 19))
            after_before.append(time_day + str(int(time_class) - 1))
            after_before.append(time_day + str(int(time_class) - 10))
            after_before.append(time_day + str(int(time_class) - 11))
        else:
            after_before.append(time_day + str(int(time_class) + 1))
            after_before.append(time_day + str(int(time_class) + 10))
            after_before.append(time_day + str(int(time_class) + 11))
            after_before.append(time_day + str(int(time_class) - 9))
            after_before.append(time_day + str(int(time_class) - 10))
            after_before.append(time_day + str(int(time_class) - 19))
        for time in after_before:
            if time in user_time_map and user_time_map[time] != 0:
                user_time_map[time] = 1
        return user_time_map

    def adjust_weight2(self, user_time_map, time_day, time_class):
        time = time_day + time_class
        after_before = []
        if int(time_class) % 2 == 0:
            after_before.append(time_day + str(int(time_class) + 30))
            after_before.append(time_day + str(int(time_class) - 30))
            after_before.append(time_day + str(int(time_class) + 39))
            after_before.append(time_day + str(int(time_class) - 31))
            after_before.append(time_day + str(int(time_class) + 40))
            after_before.append(time_day + str(int(time_class) - 40))
            after_before.append(time_day + str(int(time_class) + 49))
            after_before.append(time_day + str(int(time_class) - 41))
            after_before.append(time_day + str(int(time_class) + 50))
            after_before.append(time_day + str(int(time_class) - 50))
            after_before.append(time_day + str(int(time_class) + 59))
            after_before.append(time_day + str(int(time_class) - 51))
            after_before.append(time_day + str(int(time_class) + 60))
            after_before.append(time_day + str(int(time_class) - 60))
            after_before.append(time_day + str(int(time_class) + 69))
            after_before.append(time_day + str(int(time_class) - 61))
            after_before.append(time_day + str(int(time_class) + 70))
            after_before.append(time_day + str(int(time_class) - 70))
            after_before.append(time_day + str(int(time_class) + 79))
            after_before.append(time_day + str(int(time_class) - 71))
            after_before.append(time_day + str(int(time_class) + 80))
            after_before.append(time_day + str(int(time_class) - 80))
            after_before.append(time_day + str(int(time_class) + 89))
            after_before.append(time_day + str(int(time_class) - 81))
            after_before.append(time_day + str(int(time_class) + 90))
            after_before.append(time_day + str(int(time_class) - 90))
            after_before.append(time_day + str(int(time_class) + 99))
            after_before.append(time_day + str(int(time_class) - 91))
            after_before.append(time_day + str(int(time_class) + 100))
            after_before.append(time_day + str(int(time_class) - 100))
            after_before.append(time_day + str(int(time_class) + 109))
            after_before.append(time_day + str(int(time_class) - 101))
            after_before.append(time_day + str(int(time_class) + 110))
        else:
            after_before.append(time_day + str(int(time_class) + 30))
            after_before.append(time_day + str(int(time_class) - 30))
            after_before.append(time_day + str(int(time_class) + 31))
            after_before.append(time_day + str(int(time_class) - 39))
            after_before.append(time_day + str(int(time_class) + 40))
            after_before.append(time_day + str(int(time_class) - 40))
            after_before.append(time_day + str(int(time_class) + 41))
            after_before.append(time_day + str(int(time_class) - 49))
            after_before.append(time_day + str(int(time_class) + 50))
            after_before.append(time_day + str(int(time_class) - 50))
            after_before.append(time_day + str(int(time_class) + 51))
            after_before.append(time_day + str(int(time_class) - 59))
            after_before.append(time_day + str(int(time_class) + 60))
            after_before.append(time_day + str(int(time_class) - 60))
            after_before.append(time_day + str(int(time_class) + 61))
            after_before.append(time_day + str(int(time_class) - 69))
            after_before.append(time_day + str(int(time_class) + 70))
            after_before.append(time_day + str(int(time_class) - 70))
            after_before.append(time_day + str(int(time_class) + 71))
            after_before.append(time_day + str(int(time_class) - 79))
            after_before.append(time_day + str(int(time_class) + 80))
            after_before.append(time_day + str(int(time_class) - 80))
            after_before.append(time_day + str(int(time_class) + 81))
            after_before.append(time_day + str(int(time_class) - 89))
            after_before.append(time_day + str(int(time_class) + 90))
            after_before.append(time_day + str(int(time_class) - 90))
            after_before.append(time_day + str(int(time_class) + 91))
            after_before.append(time_day + str(int(time_class) - 99))
            after_before.append(time_day + str(int(time_class) + 100))
            after_before.append(time_day + str(int(time_class) - 100))
            after_before.append(time_day + str(int(time_class) + 101))
            after_before.append(time_day + str(int(time_class) - 109))
            after_before.append(time_day + str(int(time_class) + 110))
            after_before.append(time_day + str(int(time_class) - 110))
        for time in after_before:
            if time in user_time_map:
                if user_time_map[time] != 0 or user_time_map[time] != 1:
                    user_time_map[time] = 500 + 30 * after_before.index(time)
        return user_time_map

    def daycounting(self, course):
        day_list = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        day_idx = []
        for d in day_list:
            for day in course["classtime2"]:
                if d in day:
                    if day_list.index(d) not in day_idx:
                        day_idx.append(day_list.index(d))
        for idx in day_idx:
            self.daycount[day_list[idx]] += 1

    # This function allows students to listen to their favorite professors with a higher probability.
    def like_professor(self, user_time_map, user_time, possible):
        random_int = random.randint(0, 2)
        for course in possible:
            if self.instructor in course["instructor"]:
                if random_int == 0:
                    if course["type_of_field"] == "전공":
                        self.major_credit -= int(course["credit"][0])
                    else:
                        self.liberal_credit -= int(course["credit"][0])
                    for time in course["classtime2"]:
                        if time not in user_time:
                            return
                    for time in course["classtime2"]:
                        time_class = re.sub(r"[^0-9]", "", time)
                        time_day = re.sub(r"[0-9]", "", time)
                        user_time_map[time] = 0
                        user_time.remove(time)
                        user_time_map = self.adjust_weight2(
                            user_time_map, time_day, time_class
                        )
                        user_time_map = self.adjust_weight(
                            user_time_map, time_day, time_class
                        )
                    self.recommend.append(course)
                    print(course)
                    print("여기야?")
                    self.daycounting(course)
                    self.duplicate_remove(course["course_title"], possible)
                    break

    # This function makes students take the subjects they must take.
    def must_take(self, user_time_map, user_time, possible):
        must_list = self.course_must.split(sep=",")
        for must_course in must_list:
            if must_course[-1] == " ":
                must_course = must_course.replace(" ", "")
            if must_course[0] == " ":
                must_course = must_course.replace(" ", "")

            for course in possible:
                if (
                    must_course in course["course_title"]
                    or must_course in course["course_code"]
                ):
                    if course["type_of_field"] == "전공":
                        self.major_credit -= int(course["credit"][0])
                    else:
                        self.liberal_credit -= int(course["credit"][0])
                    for time in course["classtime2"]:
                        user_time_map[time] = 0
                        user_time.remove(time)
                        time_class = re.sub("[^0-9]", "", time)
                        time_day = re.sub("[0-9]", "", time)
                        user_time_map = self.adjust_weight2(
                            user_time_map, time_day, time_class
                        )
                        user_time_map = self.adjust_weight(
                            user_time_map, time_day, time_class
                        )

                    self.recommend.append(course)
                    print(course)
                    self.daycounting(course)
                    self.duplicate_remove(course["course_title"], possible)

    def timetable(self, possible):
        user_time_map = {
            "Mon11": randint(1, 500),
            "Mon12": randint(1, 500),
            "Mon21": randint(1, 500),
            "Mon22": randint(1, 500),
            "Mon31": randint(1, 500),
            "Mon32": randint(1, 500),
            "Mon41": randint(1, 500),
            "Mon42": randint(1, 500),
            "Mon51": randint(1, 500),
            "Mon52": randint(1, 500),
            "Mon61": randint(1, 500),
            "Mon62": randint(1, 500),
            "Mon71": randint(1, 500),
            "Mon72": randint(1, 500),
            "Mon81": randint(1, 500),
            "Mon82": randint(1, 500),
            "Mon91": randint(1, 500),
            "Mon92": randint(1, 500),
            "Mon101": randint(1, 500),
            "Mon102": randint(1, 500),
            "Mon111": randint(1, 500),
            "Mon112": randint(1, 500),
            "Mon121": randint(1, 500),
            "Mon122": randint(1, 500),
            "Tue11": randint(1, 500),
            "Tue12": randint(1, 500),
            "Tue21": randint(1, 500),
            "Tue22": randint(1, 500),
            "Tue31": randint(1, 500),
            "Tue32": randint(1, 500),
            "Tue41": randint(1, 500),
            "Tue42": randint(1, 500),
            "Tue51": randint(1, 500),
            "Tue52": randint(1, 500),
            "Tue61": randint(1, 500),
            "Tue62": randint(1, 500),
            "Tue71": randint(1, 500),
            "Tue72": randint(1, 500),
            "Tue81": randint(1, 500),
            "Tue82": randint(1, 500),
            "Tue91": randint(1, 500),
            "Tue92": randint(1, 500),
            "Tue101": randint(1, 500),
            "Tue102": randint(1, 500),
            "Tue111": randint(1, 500),
            "Tue112": randint(1, 500),
            "Tue121": randint(1, 500),
            "Tue122": randint(1, 500),
            "Wed11": randint(1, 500),
            "Wed12": randint(1, 500),
            "Wed21": randint(1, 500),
            "Wed22": randint(1, 500),
            "Wed31": randint(1, 500),
            "Wed32": randint(1, 500),
            "Wed41": randint(1, 500),
            "Wed42": randint(1, 500),
            "Wed51": randint(1, 500),
            "Wed52": randint(1, 500),
            "Wed61": randint(1, 500),
            "Wed62": randint(1, 500),
            "Wed71": randint(1, 500),
            "Wed72": randint(1, 500),
            "Wed81": randint(1, 500),
            "Wed82": randint(1, 500),
            "Wed91": randint(1, 500),
            "Wed92": randint(1, 500),
            "Wed101": randint(1, 500),
            "Wed102": randint(1, 500),
            "Wed111": randint(1, 500),
            "Wed112": randint(1, 500),
            "Wed121": randint(1, 500),
            "Wed122": randint(1, 500),
            "Thu11": randint(1, 500),
            "Thu12": randint(1, 500),
            "Thu21": randint(1, 500),
            "Thu22": randint(1, 500),
            "Thu31": randint(1, 500),
            "Thu32": randint(1, 500),
            "Thu41": randint(1, 500),
            "Thu42": randint(1, 500),
            "Thu51": randint(1, 500),
            "Thu52": randint(1, 500),
            "Thu61": randint(1, 500),
            "Thu62": randint(1, 500),
            "Thu71": randint(1, 500),
            "Thu72": randint(1, 500),
            "Thu81": randint(1, 500),
            "Thu82": randint(1, 500),
            "Thu91": randint(1, 500),
            "Thu92": randint(1, 500),
            "Thu101": randint(1, 500),
            "Thu102": randint(1, 500),
            "Thu111": randint(1, 500),
            "Thu112": randint(1, 500),
            "Thu121": randint(1, 500),
            "Thu122": randint(1, 500),
            "Fri11": randint(1, 500),
            "Fri12": randint(1, 500),
            "Fri21": randint(1, 500),
            "Fri22": randint(1, 500),
            "Fri31": randint(1, 500),
            "Fri32": randint(1, 500),
            "Fri41": randint(1, 500),
            "Fri42": randint(1, 500),
            "Fri51": randint(1, 500),
            "Fri52": randint(1, 500),
            "Fri61": randint(1, 500),
            "Fri62": randint(1, 500),
            "Fri71": randint(1, 500),
            "Fri72": randint(1, 500),
            "Fri81": randint(1, 500),
            "Fri82": randint(1, 500),
            "Fri91": randint(1, 500),
            "Fri92": randint(1, 500),
            "Fri101": randint(1, 500),
            "Fri102": randint(1, 500),
            "Fri111": randint(1, 500),
            "Fri112": randint(1, 500),
            "Fri121": randint(1, 500),
            "Fri122": randint(1, 500),
        }
        user_time = [
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
        self.preprocessing(possible)
        self.credit_classify()
        random.shuffle(possible)
        if self.course_must != "":
            self.must_take(user_time_map, user_time, possible)
        if self.instructor != "":
            self.like_professor(user_time_map, user_time, possible)
        self.school_day(possible)
        self.morning(possible)
        while self.major_credit >= 3 or self.liberal_credit >= 3:
            sorted_time_map = sorted(user_time_map.items(), key=operator.itemgetter(1))
            for time, weight in sorted_time_map:
                if time not in user_time:
                    continue
                if weight == 0:
                    continue
                time_class = re.sub(r"[^0-9]", "", time)
                time_day = re.sub(r"[0-9]", "", time)
                if self.five_days_a_week == 1:
                    if self.daycount[time_day] >= 2:
                        continue
                for course in possible:
                    temp = 0
                    for t in course["classtime2"]:
                        if t not in user_time:
                            temp = 1
                            break
                    if temp == 1:
                        continue
                    if course["type_of_field"] == "전공":
                        if self.major_credit <= 0:
                            continue
                        if int(course["credit"][0]) < 3:
                            continue
                        for time in course["classtime2"]:
                            time_class = re.sub(r"[^0-9]", "", time)
                            time_day = re.sub(r"[0-9]", "", time)
                            user_time_map[time] = 0
                            user_time.remove(time)
                            user_time_map = self.adjust_weight2(
                                user_time_map, time_day, time_class
                            )
                            user_time_map = self.adjust_weight(
                                user_time_map, time_day, time_class
                            )
                        self.recommend.append(course)
                        print(course)
                        self.daycounting(course)
                        self.duplicate_remove(course["course_title"], possible)
                        self.major_credit -= int(course["credit"][0])
                        print("major_credit: ", self.major_credit)
                        break
                    else:
                        if self.liberal_credit <= 0:
                            self.liberal_remove(possible)
                            continue
                        if self.liberal_credit <= 3:
                            if int(course["credit"][0]) != self.liberal_credit:
                                continue
                        for time in course["classtime2"]:
                            time_class = re.sub(r"[^0-9]", "", time)
                            time_day = re.sub(r"[0-9]", "", time)
                            user_time_map[time] = 0
                            user_time.remove(time)
                            user_time_map = self.adjust_weight2(
                                user_time_map, time_day, time_class
                            )
                            user_time_map = self.adjust_weight(
                                user_time_map, time_day, time_class
                            )
                        self.recommend.append(course)
                        print(course)
                        self.daycounting(course)
                        self.duplicate_remove(course["course_title"], possible)
                        self.liberal_credit -= int(course["credit"][0])
                        print("liberal_credit: ", self.liberal_credit)
                        break
                break

        return self.recommend
