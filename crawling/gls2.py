import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Gls2:
    def login(self):
        url = "https://kingoinfo.skku.edu/gaia/nxui/index.html?ticket=GVVsR0gJcOQeScyA"
        browser = webdriver.Chrome()
        browser.get(url)
        browser.implicitly_wait(3)
        # 로그인 수동으로 하기
        sleep(13)
        return browser

    def get_into_all(self, browser):
        browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[16]/div/div[1]/input",
        ).send_keys("전체과목 검색")

        browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[16]/div/div[1]/input",
        ).send_keys(Keys.ENTER)
        browser.implicitly_wait(3)

    def click_humanities(self, browser):
        check = browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[5]/div/div[1]/div/img",
        )
        check.click()
        sleep(1)

    def click_science(self, browser):
        check = browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[5]/div/div[2]/div/img",
        )
        check.click()
        sleep(1)

    def click_icampus(self, browser):
        check = browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[5]/div/div[3]/div/img",
        )
        check.click()
        sleep(1)

    def get_info(self, semester, codelist, browser):
        result = []
        year = browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[2]/div/div[1]/input",
        )
        sleep(2)
        year.clear()
        sleep(2)
        year.click()
        sleep(2)
        year.send_keys(semester)
        sleep(2)
        year.send_keys(Keys.ENTER)
        sleep(2)

        for i, code in enumerate(codelist):
            code = browser.find_element(
                By.XPATH,
                "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[9]/input",
            )
            code.click()
            sleep(2)
            code.clear()
            sleep(2)
            code.send_keys(codelist[i])
            for j in range(3):
                if j == 0:
                    self.click_humanities(browser)
                elif j == 1:
                    self.click_science(browser)
                else:
                    self.click_icampus(browser)
                browser.find_element(
                    By.XPATH,
                    "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[3]/div/div/div/div[8]/div",
                ).click()
                sleep(3)
                duplicated = 0
                for h in range(130):
                    print(h)
                    table = browser.find_elements(
                        By.XPATH,
                        "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[1]/div[2]/div/div/div",
                    )
                    # duplicated = 0
                    for tab in table:
                        a = tab.text.split("\n")
                        if len(a) <= 8:
                            continue
                        if a in result:
                            duplicated += 1
                        else:
                            print(a)
                            result.append(a)
                    if duplicated > 4:
                        break
                    scroll = browser.find_element(
                        By.XPATH,
                        "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[3]/div/div[2]/div",
                    )
                    if scroll.is_displayed():
                        for _ in range(9):
                            scroll.click()
                        sleep(2)
                    else:
                        break
        data = {}
        data["semester"] = semester
        data["course"] = result
        path = "./2024_data/01교양/" + semester + ".json"
        with open(path, "w", encoding="utf-8") as make_file:
            json.dump(data, make_file, ensure_ascii=False, indent="\t")


gls2 = Gls2()
browser = gls2.login()
gls2.get_into_all(browser)
subjectmap = {
    "고전명저": "GEDM",
    "글로벌": "GEDG",
    "인성": "GEDC",
    "리더쉽": "GEDR",
    "의사소통": "GEDW",
    "창의": "GEDT",
    "BSM": "GEDB",
    "기인사": "GEDI",
    "핵균-인간-문화": "GEDH",
    "핵균-사회-역사": "GEDS",
    "핵균-자연-과학-기술": "GEDN",
    "일반선택": "GELT",
    "DS과목": "DASF",
}
codelist = list(subjectmap.values())

year_list = [
    "2024학년도 2학기",
    # "2022학년도 1학기",
    # "2021학년도 2학기",
    # "2021학년도 1학기",
    # "2020학년도 2학기",
    # "2020학년도 1학기",
    # "2019학년도 2학기",
    # "2019학년도 1학기",
]
print(codelist)
for year in year_list:
    gls2.get_info(year, codelist, browser)
