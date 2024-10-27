import json
import os

import pandas as pd
from sqlalchemy import create_engine


class Cleaning:
    def __init__(self):
        self.courselist = [
            "온라인 (사전제작)",
            "온라인[사전제작]",
            "온라인 (사전제작+Real Time Streaming)",
            "온라인 (Real Time Streaming)",
            "온-오프혼합 (오프라인 순환출석+Real Time Streaming)",
            "온-오프혼합 (오프라인+Real Time Streaming)",
            "온-오프혼합 (오프라인+강의저장)",
            "온-오프[오프라인+강의저장,Real Time Streaming]",
            "온-오프[오프라인+강의저장]",
            "온-오프[오프라인+Real Time Streaming]",
            "오프라인",
            "오프라인 (일부 주차 오프라인+잔여 주차 Real Time Streaming)",
            "오프라인 (일부 주차 오프라인+잔여 주차 사전제작영상)",
            "온-오프혼합 (오프라인 순환출석+강의저장)",
            "글로벌-혁신[온라인사전강의 + 오프라인 또는 온라인 Real Time Streaming",
            "PBL(온라인[사전제작]+오프라인)",
            "플립러닝(온라인[사전제작]+오프라인)",
            "nan",
        ]
        self.collumnName = [
            "degree_courses",
            "type_of_field3",
            "course_code",
            "course_title",
            "course_title_english",
            "instructor",
            "campus",
            "type_of_field2",
            "credits(Hrs)",
            "classtime",
            "type_of_class1",
            "type_of_class2",
            "remarks",
        ]
        self.df = pd.DataFrame(columns=self.collumnName)

    def open_json(self, major, season):
        # json 파일이 없을 때 예외 처리
        path = os.path.expanduser(
            rf"~/skku/2403skku/DSC3037-Fall-2022/2024_data/{major}/{season}.json"
        )
        print(path)
        try:
            with open(
                path,
                encoding="UTF8",
            ) as f:
                js = json.load(f)
            df1 = pd.DataFrame(js)
            df1 = pd.read_json(
                path,
                encoding="UTF8",
            )
            return df1
        except FileNotFoundError:
            print("해당 파일이 없습니다.")
            return None

    def cleaning(self, df1):
        df1["course"] = df1["course"].apply(self.process_course)
        df1 = df1.dropna(subset=["course"])
        return df1

    def process_course(self, course_list):
        # Remove '보기'
        course_list = [item for item in course_list if item != "보기"]

        # Ensure length greater than 3
        if len(course_list) <= 3:
            return None

        # Add 'nan' for missing '영역구분'
        if course_list[1] not in ["전공코어", "전공심화", "실험실습"]:
            course_list.insert(1, "nan")

        # Insert 'nan' for missing professor name
        if len(course_list) >= 6 and course_list[5] in ["인문사회", "자연과학"]:
            course_list.insert(5, "nan")

        # Add 'nan' for missing '수업방식2'
        if len(course_list) == 11:
            course_list.append("nan")

        # Add 'nan' for missing remarks
        if len(course_list) == 12:
            course_list.append("nan")

        # Correct misplaced last column entries
        if course_list[-2] not in self.courselist:
            temp = course_list[-2]
            course_list[-1] = temp
            course_list[-2] = "nan"

        if len(course_list) <= 8:
            return None
        return course_list

    def make_df(self, df1):
        for idx, name in enumerate(self.collumnName):
            df1[name] = df1["course"].str.get(idx)
        df1 = df1.drop(["course"], axis="columns")
        self.df = pd.concat([self.df, df1], axis=0)


result = Cleaning()

major_list = [
    "건설환경공학부",
    "건축공학과",
    "건축토목공학부",
    "건축학과",
    "경영학과",
    "경제학과",
    "고분자시스템공학과",
    "고전학연계전공",
    "공익과법연계전공",
    # "공학계열",
    "교육학과",
    "국어국문학과",
    "국제통상학전공",
    "글로벌경영학과",
    "글로벌경제학과",
    "글로벌리더학부",
    "글로벌융합학부",
    "글로컬문화콘텐츠전공",
    "기계공학부",
    "나노공학과",
    # "나노과학공학전공",
    "데이터사이언스융합전공",
    "독어독문학과",
    # "디자인학과",
    "러시아어문학과",
    "마이크로시스템기술전공",
    # "무용학과",
    "문헌정보학과",
    "물리학과",
    "미디어커뮤니케이션학과",
    "미래인문학연계전공",
    # "미술학과",
    "바이오메카트로닉스학과",
    "반도체시스템공학과",
    "법무정책학연계전공",
    "법학과",
    "비교문화전공",
    "사학과",
    "사회복지학과",
    "사회학과",
    "사회환경시스템공학과",
    "생명과학과",
    "생명산업공학전공",
    "소비자학과",
    "소재부품융합공학과",
    "소프트웨어학과",
    "수학과",
    "스포츠과학과",
    "시스템경영공학과",
    "식품생명공학과",
    "신소재공학부",
    "심리학과",
    "아동-청소년학과",
    "앙트레프레너십연계전공",
    "약학과",
    "약학부",
    "여성학전공",
    # "연기예술학과",
    # "영상학과",
    "영어영문학과",
    "유라시아지역문화경제전공",
    "유전공학과",
    "유학-동양학과",
    "융합생명공학과",
    "융합소프트웨어연계전공",
    "융합소프트웨어연계전공-SCSC",
    "융합소프트웨어연계전공-SW융합",
    "융합소프트웨어전공",
    "융합언어학연계전공",
    # "의상학과",
    "의예과",
    "의학과",
    "인공지능융합전공",
    "인포매틱스융합전공",
    "일본학전공",
    "자연과학계열",
    "전자전기컴퓨터공학전공",
    "정보통신계열",
    "정치외교학과",
    "조경학과",
    "중국학전공",
    "차세대바이오헬스 융합트랙",
    "철학과",
    "컬처앤테크놀로지융합전공",
    "컴퓨터공학과",
    "컴퓨터교육과",
    "텍스타일시스템공학과",
    "텍스타일시스템공학전공",
    "통계학과",
    "프랑스어문학과",
    "한국학연계전공",
    "한국학전공",
    "한문교육과",
    "한문학과",
    "행정학과",
    "화학공학-고분자공학부",
    "화학과",
]
season_list = [
    "2024학년도 2학기",
]
for major in major_list:
    for season in season_list:
        df1 = result.open_json(major, season)
        if df1 is None:
            continue
        df1 = result.cleaning(df1)
        result.make_df(df1)

# store this dataframe in a table in the database
# you should create  and a new table named "major_subject" for this

engine = create_engine("mysql+pymysql://root:1234@localhost/swe3002")
result.df.to_sql(name="major_subject", con=engine, if_exists="append", index=False)
# engine = create_engine("mysql+pymysql://root:1234@localhost:3306/dsc3037", encoding='utf-8')
# conn = engine.connect()
# result.df.to_sql(name ="skku_subject",con=engine ,if_exists='append',index = False)
# conn.close()
