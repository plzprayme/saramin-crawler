from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from bs4 import BeautifulSoup as bs4

from time import sleep

from datetime import date, timedelta

from time import sleep

import pandas as pd

# def filter_recruitment(rows):
#     rows = filter_by_condition(rows)
#     return rows

# def filter_by_condition2(rows):
#     result = []
#     for row in rows:
#         location_condition = row.find_element_by_css_selector(".work_place")
#         career_condition = row.find_element_by_css_selector(".career").text
#         deadline = row.find_element_by_css_selector('.deadlines').text
#         # url = row.find_element_by_css_selector('.str_tit').get_attribute('href')

#         try:
#             if is_deadline_over_ten_days(deadline):
#                 print("FILTERED DEADLINE ROW", deadline)
#                 result.append(row)
#             elif "대전" in location_condition:
#                 print("FILTERED LOCATION CONDITION ROW", location_condition)
#                 result.append(row)
#             elif "신입" in career_condition or "경력무관" in career_condition:
#                 print("FILTERED CAREER CONDITION ROW", career_condition)
#                 result.append(row)
#         except:
#             print("UNFILTERED CAREER ROW", deadline)

#     return result


def filter_by_condition(rows):
    result = []
    for row in rows:
        location_condition = row.find_element_by_css_selector(".work_place")
        career_condition = row.find_element_by_css_selector(".career").text
        deadline = row.find_element_by_css_selector('.deadlines').text
        url = row.find_element_by_css_selector(
            '.str_tit').get_attribute('href')

        try:
            if is_deadline_over_ten_days(deadline):
                print("FILTERED DEADLINE ROW", deadline)
                result.append(url)
            elif "대전" in location_condition:
                print("FILTERED LOCATION CONDITION ROW", location_condition)
                result.append(url)
            elif "신입" in career_condition or "경력무관" in career_condition:
                print("FILTERED CAREER CONDITION ROW", career_condition)
                result.append(url)
        except:
            print("UNFILTERED CAREER ROW", deadline)

    return result


def is_deadline_over_ten_days(deadline):
    today = date.today()
    iso_format = get_deadline_for_iso(deadline)
    deadline_date = date.fromisoformat(iso_format)
    deadline = (deadline_date - today).days
    return deadline >= 10


def get_deadline_for_iso(deadline):
    iso_format = [str(date.today().year)]
    a = deadline.split(" ")
    b = a[1].split("(")
    c = b[0].split("/")
    d = iso_format + c
    return "-".join(d)


def get_column_value(soup, selector, parser_function):
    try:
        value = parser_function(soup, selector)
        return value
    except:
        return ""


def default_parser(soup, selector):
    return soup.select(selector)[0].text


def deadline_parser(soup, selector):
    deadline = soup.select(selector)[0].text  # YYYY.MM.DD tt:mm
    return deadline.split(" ")[0]  # YYYY.MM.DD


def href_parser(soup, selector):
    return soup.select(selector)[0].attrs["href"]


with webdriver.Chrome("C:/Users/prayme/chromedriver") as driver:
    wait = WebDriverWait(driver, 10)

    company_name_list = []
    content_list = []
    aa_list = []
    work_location_list = []
    url_list = []
    deadline_list = []
    imployee_list = []
    sales_list = []
    gender_list = []
    find_who_list = []
    income_list = []
    work_time_list = []
    benefit_list = []
    resume_format_list = []

    driver.get("http://www.saramin.co.kr/zf_user/jobs/list/domestic?loc_mcd=105000&cat_cd=404%2C407%2C408%2C402%2C309%2C302%2C301%2C308%2C303%2C314&panel_type=&search_optional_item=n&search_done=y&panel_count=y")

    rows = driver.find_elements_by_css_selector(
        "#default_list_wrap > section > div.list_body > .list_item")
    print("BEFORE", len(rows))
    rows = filter_by_condition(rows)
    print("AFTER", len(rows))

    for row in rows:
        # print("ROW", row)
        # row에서 해결할 수 있는 것들

        # 아이템 페이지로 이동하기
        driver.get(row)

        # DOM 로딩 기다리기
        wait.until(presence_of_element_located(
            (By.CSS_SELECTOR, ".info_period > dd:nth-child(4)")
        ))

        # HTML 얻기
        html = driver.page_source
        soup = bs4(html, 'html.parser')

        # # 각 아이템의 회사 이름 가져오기
        company_name = get_column_value(soup, ".company_name", default_parser)
        # print("COMPANY NAME", company_name)

        # 각 아이템의 URL 가져오기
        url = row

        # # 각 아이템의 모집 집종 가져오기
        # print("JOB SECTOR", row.find_element_by_css_selector('.job_sector').text)

        # # # 각 아이템의 근무 주소 가져오기
        work_location = get_column_value(
            soup, "#map_0 > div > address > span", default_parser)
        # print("WORK LOCATION", work_location)

        # # # 각 아이템의 이력서 제출 형식 가져오기
        resume_submission_format = get_column_value(
            soup, '.template', default_parser)
        # print("RESUME SUBMISSION FORMAT", resume_submission_format)

        # # 각 아이템의 모집 마감 날짜 가져오기
        deadline = get_column_value(
            soup, '.info_period > dd:nth-child(4)', deadline_parser)
        # print("DEADLINE", deadline)

        # # # 각 아이템의 복리후생 가져오기
        benefit = get_column_value(soup, '.jv_benefit', default_parser)
        # print("BENEFIT", benefit)

        cont = soup.select(".cont")[0]
        income = ""
        work_time = ""
        find_who = ""
        for column in cont:
            for dl in column.select("dl"):
                if "급여" == dl.dt.text:
                    # print("급여", dl.dd.text)
                    income = dl.dd.text
                elif "근무일시" == dl.dt.text:
                    # print("근무일시", dl.dd.text)
                    work_time = dl.dt.text
                elif "우대사항" == dl.dt.text:
                    # print("우대사항", dl.dd.text)
                    find_who = dl.dd.text

        # 사업내용 가져오기

        company_detail = get_column_value(
            soup, '.jv_header > a.company', href_parser)
        # print("COMPANY_DETAIL", company_detail)

        sleep(5)

        driver.get("http://www.saramin.co.kr" + company_detail)

        sleep(5)
        # wait.until(presence_of_element_located(
        #     (By.CSS_SELECTOR, "#company_info_introduce")
        # ))

        company_detail_html = driver.page_source
        company_detail_soup = bs4(company_detail_html, 'html.parser')

        # document.querySelector("#company_info_introduce").textContent.trim()[116:]
        content = ""
        imployee = ""
        sales = ""
        aa = ""
        gender = "무관"
        try:
            detail = company_detail_soup.select(
                '#company_info_introduce')[0].text.strip()
            # detail = company_detail_soup.select(".list_info")

            if "사업내용" in detail:
                index = detail.index("사업내용")
                content = detail[index:]
                # print("사업내용", content)
            elif "업종" in detail:
                index = detail.index("업종")
                content = detail[index:]
            # print("업종", content)

            boxes = company_detail_soup.select(".list_intro > li")

            for box in boxes:
                if "사원" in box.em:
                    # print("사원 수 ", box.select(".desc")[0].text)
                    imployee = box.select(".desc")[0].text
                elif "매출" in box.em:
                    # print("매출", box.select(".desc")[0].text)
                    sales = box.select(".desc")[0].text
        except:
            print("사업내용 쪽 에러 남")

        company_name_list.append(company_name)
        content_list.append(content)
        aa_list.append(aa)
        work_location_list.append(work_location)
        url_list.append(url)
        deadline_list.append(deadline)
        imployee_list.append(imployee)
        sales_list.append(sales)
        gender_list.append(gender)
        find_who_list.append(find_who)
        income_list.append(income)
        work_time_list.append(work_time)
        benefit_list.append(benefit)
        resume_format_list.append(resume_submission_format)

    df = pd.DataFrame({
        "사업장명(회사이름)": company_name_list,
        "사업내용": content_list,
        "모집직종": aa_list,
        "모집인원": aa_list,
        "직무내용": aa_list,
        "근무지주소": work_location_list,
        "소재지주소": work_location_list,
        "공지사이트": url_list,
        "서류마감": deadline_list,
        "근로자 수": imployee_list,
        "매출액": sales_list,
        "성별": gender_list,
        "우대조건": find_who,
        "임금액": income_list,
        "근무시간": work_time_list,
        "복리후생": benefit_list,
        "제출서류": resume_format_list
    })

    df.to_csv('utf_채용공고.csv', encoding='utf-8-sig')
    df.to_csv('euc_채용공고.csv', encoding='euc-kr')
