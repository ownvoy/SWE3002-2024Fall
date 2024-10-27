import json
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Gls:
    def __init__(self):
        self.trial = 0

    def login(self):
        url = "https://kingoinfo.skku.edu/gaia/nxui/index.html?ticket=GVVsR0gJcOQeScyA"
        browser = webdriver.Chrome()
        browser.get(url)
        browser.implicitly_wait(3)
        # 로그인 수동으로 하기
        sleep(13)
        return browser

    def get_into_major(self, browser):
        browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[16]/div/div[1]/input",
        ).send_keys("학사-전공")
        browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[16]/div/div[1]/input",
        ).send_keys(Keys.ENTER)
        browser.implicitly_wait(3)

    def click_humanities(self, browser):
        check = browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[4]/div/div[1]/div/img",
        )
        check.click()
        sleep(1)

    def click_science(self, browser):
        check = browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[4]/div/div[2]/div/img",
        )
        check.click()
        sleep(1)

    def click_icampus(self, browser):
        check = browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[4]/div/div[3]/div/img",
        )
        check.click()
        sleep(1)

    def get_info(self, semester, college, majorlist, number, browser):
        year = browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[2]/div/div[1]/input",
        )
        sleep(3)
        year.clear()
        sleep(3)
        year.click()
        year.send_keys(semester)
        sleep(2)
        year.send_keys(Keys.ENTER)
        sleep(2)

        coll = browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[7]/div/div[1]/input",
        )
        sleep(2)
        coll.clear()
        sleep(2)
        coll.click()
        coll.click()
        sleep(2)
        coll.send_keys(college)
        sleep(3)
        coll.send_keys(Keys.ENTER)
        sleep(4)

        # 대학 선택하기
        # choose college
        for i in range(number):
            result = []
            major = browser.find_element(
                By.XPATH,
                "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[9]/div/div[1]/input",
            )
            major.clear()
            sleep(2)
            major.click()
            sleep(2)
            major.send_keys(majorlist[i])
            # if i == 0:
            #     pass
            # else:
            #     major.send_keys(Keys.DOWN)
            sleep(2)
            major.send_keys(Keys.ENTER)
            sleep(5)
            # if i != 10:
            #     continue
            for j in range(3):

                if j == 0:
                    self.click_humanities(browser)
                elif j == 1:
                    self.click_science(browser)
                else:
                    self.click_icampus(browser)

                browser.find_element(
                    By.XPATH,
                    "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[12]/div",
                ).click()
                sleep(3)
                duplicated = 0
                for h in range(60):
                    table = browser.find_elements(
                        By.XPATH,
                        "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[1]/div[2]/div/div/div",
                    )
                    # 정보 가져오기
                    print(len(table))
                    for tab in table:
                        a = tab.text.split("\n")
                        if len(a) == 1:
                            continue
                        if a in result:
                            duplicated += 1
                        else:
                            result.append(a)
                            print(a)
                    # 같은 정보 나오면 그만하기
                    # if information is duplicated, break
                    if duplicated > 4:
                        break
                    # 밑으로 내려가기 (스크롤)
                    scroll = browser.find_element(
                        By.XPATH,
                        "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[3]/div/div[2]/div",
                    )
                    sleep(2)
                    if scroll.is_displayed():
                        for _ in range(10):
                            scroll.click()
                        sleep(2)
                    else:
                        break
            data = {}
            data["major"] = majorlist[i]
            data["semester"] = semester
            data["college"] = college
            data["course"] = result

            path = "./2024_data2/" + majorlist[i] + "/" + semester + ".json"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as make_file:
                json.dump(data, make_file, ensure_ascii=False, indent="\t")


gls = Gls()
browser = gls.login()
gls.get_into_major(browser)
year_list = [
    "2024학년도 2학기",
]
#
# for year in year_list:
#     gls.get_info(
#         year,
#         "예술대학",
#         ["디자인학과", "연기예술학과", "무용학과", "영상학과", "미술학과", "의상학과"],
#         6,
#         browser=browser,
#     )
#

# for year in year_list:
#     gls.get_info(
#         year,
#         "문과대학",
#         [
#             "프랑스어문학과",
#             "여성학전공",
#             "유라시아지역문화경제전공",
#             "중어중문학과",
#             "고전학연계전공",
#             "러시아어문학과",
#             "글로컬문화콘텐츠전공",
#             "한문학과",
#             "비교문화전공",
#             "융합언어학연계전공",
#             "미래인문학연계전공",
#             "영어영문학과",
#             "독어독문학과",
#             "문헌정보학과",
#             "사학과",
#             "철학과",
#             "중국학전공",
#             "국어국문학과",
#             "일본학전공",
#         ],
#         19,
#         browser=browser,
#     )
#
# for year in year_list:
#     gls.get_info(
#         year,
#         "경영대학",
#         ["앙트레프레너십연계전공", "경영학과", "글로벌경영학과"],
#         3,
#         browser=browser,
#     )
#
# sleep(2)
for year in year_list:
    gls.get_info(year, "의과대학", ["의예과", "의학과"], 2, browser)

sleep(2)
for year in year_list:
    gls.get_info(
        year,
        "경제대학",
        ["통계학과", "국제통상학전공", "경제학과", "글로벌경제학과"],
        4,
        browser,
    )

sleep(2)
for year in year_list:
    gls.get_info(
        year,
        "사범대학",
        ["한문교육과", "교육학과", "수학교육과", "컴퓨터교육과"],
        4,
        browser,
    )

sleep(2)

for year in year_list:
    gls.get_info(year, "법과대학", ["법학과"], 1, browser)

sleep(2)

for year in year_list:
    gls.get_info(
        year, "자연과학대학", ["물리학과", "화학과", "수학과", "생명과학과"], 4, browser
    )

sleep(2)

for year in year_list:
    gls.get_info(year, "스포츠과학대학", ["스포츠과학과"], 1, browser)

sleep(2)

for year in year_list:
    gls.get_info(year, "약학대학", ["약학부", "약학과"], 2, browser)

sleep(2)

for year in year_list:
    gls.get_info(year, "유학대학", ["유학-동양학과"], 1, browser)

sleep(2)


for year in year_list:
    gls.get_info(
        year,
        "사회과학대학",
        [
            "정치외교학과",
            "미디어커뮤니케이션학과",
            "아동-청소년학과",
            "법무정책학연계전공",
            "심리학과",
            "사회학과",
            "소비자학과",
            "공익과법연계전공",
            "사회복지학과",
            "글로벌리더학부",
            "행정학과",
        ],
        11,
        browser,
    )
sleep(2)

for year in year_list:
    gls.get_info(
        year,
        "공과대학",
        [
            "마이크로시스템기술전공",
            "사회환경시스템공학과",
            "건축학과",
            "시스템경영공학과",
            "건설환경공학부",
            "텍스타일시스템공학전공",
            "화학공학-고분자공학부",
            "텍스타일시스템공학과",
            "신소재공학부",
            "나노공학과",
            "기계공학부",
            "건축공학과",
            "조경학과",
            "고분자시스템공학과",
            "건축토목공학부",
        ],
        15,
        browser,
    )
sleep(2)

for year in year_list:
    gls.get_info(year, "동아시아학술원", ["한국학전공", "한국학연계전공"], 2, browser)
sleep(2)
# mlist2 = ["2021학년도 2학기", "2021학년도 1학기", "2020학년도 2학기"]
#
# mlist3 = ["2020학년도 1학기"]
for year in year_list:
    gls.get_info(
        year,
        "소프트웨어융합대학",
        [
            "글로벌융합학부",
            "데이터사이언스융합전공",
            "소프트웨어학과",
            "융합소프트웨어연계전공-SCSC",
            "융합소프트웨어연계전공-SW융합",
            "융합소프트웨어전공",
            "인공지능융합전공",
            "인포매틱스융합전공",
            "지능형소프트웨어학과",
            "컬처앤테크놀로지융합전공",
            "컴퓨터공학과",
        ],
        11,
        browser,
    )
sleep(2)

# for year in mlist3:
#     gls.get_info(
#         year,
#         "소프트웨어융합대학",
#         [
#             "융합소프트웨어전공",
#             "데이터사이언스융합전공",
#             "소프트웨어학과",
#             "융합소프트웨어연계전공-SCSC",
#             "인공지능융합전공",
#             "컬처앤테크놀로지융합전공",
#             "컴퓨터공학과",
#             "인포매틱스융합전공",
#             "융합소프트웨어연계전공-SW융합",
#         ],
#         9,
#         browser,
#     )
# sleep(2)

for year in year_list:
    gls.get_info(
        year,
        "생명공학대학",
        [
            "식품생명공학과",
            "유전공학과",
            "생명산업공학전공",
            "융합생명공학과",
            "차세대바이오헬스 융합트랙",
            "바이오메카트로닉스학과",
            "컴바이오믹스연계전공",
        ],
        7,
        browser,
    )
sleep(2)

# for year in mlist3:
#     gls.get_info(
#         year, "생명공학대학", ["식품생명공학과", "유전공학과", "생명산업공학전공", "융합생명공학과", "바이오메카트로닉스학과"], 5, browser
#     )

for year in year_list:
    gls.get_info(
        year,
        "정보통신대학",
        [
            "전자전기컴퓨터공학전공",
            "반도체소자회로설계및시스템 융합트랙",
            "반도체소재부품장비패키징 융합트랙",
            "전자전기컴퓨터공학전공",
            "차세대반도체공학연계전공",
            "첨단반도체 융합트랙",
            "소프트웨어학과",
            "반도체시스템공학과",
            "소재부품융합공학과",
            "전자전기공학부",
            "융합소프트웨어연계전공",
        ],
        11,
        browser,
    )

# sleep(2)

# for year in mlist3:
#     gls.get_info(
#         year,
#         "정보통신대학",
#         ["전자전기컴퓨터공학전공", "소프트웨어학과", "반도체시스템공학과", "전자전기공학부", "융합소프트웨어연계전공"],
#         5,
#         browser,
#     )

# sleep(2)

# mlist4 = [
#     "2022학년도 2학기",
#     "2022학년도 1학기",
#     "2021학년도 2학기",
#     "2021학년도 1학기",
# ]

# mlist5 = ["2020학년도 2학기"]
# mlist6 = ["2020학년도 1학기", "2019학년도 2학기", "2019학년도 1학기"]
for year in year_list:
    gls.get_info(
        year, "학부대학", ["정보통신계열", "경영학(글로벌)전공", "공학계열"], 3, browser
    )

sleep(2)
# for year in mlist5:
#     gls.get_info(
#         year, "학부대학", ["정보통신계열", "전자전기 컴퓨터공학계열", "경영학(글로벌)전공", "공학계열", "자연과학계열"], 5, browser
#     )

# sleep(2)
# for year in mlist6:
#     gls.get_info(year, "학부대학", ["정보통신계열", "전자전기 컴퓨터공학계열", "경영학(글로벌)전공", "공학계열"], 4, browser)
