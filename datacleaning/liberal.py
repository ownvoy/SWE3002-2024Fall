import json
import os
import pandas as pd
from sqlalchemy import create_engine


class Cleaning2:
    def __init__(self):
        self.collumnName = [
            "course_code",
            "type_of_field",
            "course_title",
            "course_title_english",
            "instructor",
            "campus",
            "degree_courses",
            "classtime",
            "type_of_class1",
            "credits(Hrs)",
            "type_of_class2",
            "remarks",
        ]
        self.df = pd.DataFrame(columns=self.collumnName)

    def clean_course(self, course):

        # '담기', '보기' 제거 및 기타 정제
        course = [item for item in course if item not in ["담기", "보기"]]

        # 조건에 따른 수정
        if len(course) == 11:
            course.insert(10, "nan")
            course.insert(10, "nan")
        elif len(course) == 12:
            course.insert(10, "nan")

        # 국제어수업 위치 변경
        if len(course) > 7 and course[7] == "국제어수업":
            course[7], course[8] = course[8], course[7]

        # 문제해결, 혁신수업, 국제어 조건 확인 및 변경
        if len(course) > 10:
            if (
                "문제해결" in course[-2]
                or "혁신수업" in course[-2]
                or "국제어" in course[-2]
            ):
                if (
                    "문제해결" not in course[-3]
                    and "혁신수업" not in course[-3]
                    and "국제어" not in course[-3]
                ):
                    course[-2], course[-3] = course[-3], course[-2]

        return course[:13]  # 최대 13개 항목 반환

    def datacleaning(self, year):
        path = os.path.expanduser(
            rf"~/skku/2403skku/DSC3037-Fall-2022/2024_data/01교양/2024학년도 2학기.json"
        )
        with open(path, encoding="UTF8") as f:
            data = json.load(f)

        df2 = pd.DataFrame(data)
        df2["course"] = df2["course"].apply(self.clean_course)  # apply 함수 사용
        for idx, name in enumerate(self.collumnName):
            df2[name] = df2["course"].str[idx]  # 각 컬럼에 해당하는 데이터 추출
        df2 = df2.drop(["course"], axis=1)  # 원본 리스트 컬럼 삭제
        df2 = df2.dropna(subset=["credits(Hrs)"])  # 'credits(Hrs)'가 Null인 행 삭제

        return df2


result = Cleaning2()
season_list = ["2024학년도 2학기"]

for season in season_list:
    temp = result.datacleaning(season)
    result.df = pd.concat([result.df, temp], ignore_index=True)

engine = create_engine("mysql+pymysql://root:1234@localhost/swe3002")
result.df.to_sql(
    name="liberal arts_subject", con=engine, if_exists="append", index=False
)
