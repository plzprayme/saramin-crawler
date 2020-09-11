from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from bs4 import BeautifulSoup as bs4

from time import sleep

from datetime import date, timedelta

from time import sleep

# def filter_recruitment(rows):
#     rows = filter_by_condition(rows)
#     return rows

def filter_by_condition2(rows):
    result = []
    for row in rows:
        location_condition = row.find_element_by_css_selector(".work_place")
        career_condition = row.find_element_by_css_selector(".career").text
        deadline = row.find_element_by_css_selector('.deadlines').text
        # url = row.find_element_by_css_selector('.str_tit').get_attribute('href')
        
        try:
            if is_deadline_over_ten_days(deadline):
                print("FILTERED DEADLINE ROW", deadline)
                result.append(row)
            elif "대전" in location_condition:
                print("FILTERED LOCATION CONDITION ROW", location_condition)
                result.append(row)
            elif "신입" in career_condition or "경력무관" in career_condition:
                print("FILTERED CAREER CONDITION ROW", career_condition)
                result.append(row)
        except:
            print("UNFILTERED CAREER ROW", deadline)

    return result

def filter_by_condition(rows):
    result = []
    for row in rows:
        location_condition = row.find_element_by_css_selector(".work_place")
        career_condition = row.find_element_by_css_selector(".career").text
        deadline = row.find_element_by_css_selector('.deadlines').text
        url = row.find_element_by_css_selector('.str_tit').get_attribute('href')
        
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
    deadline = soup.select(selector)[0].text # YYYY.MM.DD tt:mm
    return deadline.split(" ")[0] # YYYY.MM.DD

with webdriver.Chrome("C:/Users/prayme/chromedriver") as driver:
    wait = WebDriverWait(driver, 10)

    driver.get("http://www.saramin.co.kr/zf_user/jobs/list/domestic?loc_mcd=105000&cat_cd=404%2C407%2C408%2C402%2C409%2C416%2C413%2C411%2C417%2C410&panel_type=&search_optional_item=n&search_done=y&panel_count=y")
    

    rows = driver.find_elements_by_css_selector("#default_list_wrap > section > div.list_body > .list_item")
    print("BEFORE", len(rows))
    rows = filter_by_condition(rows)
    print("AFTER", len(rows))

    for row in rows:
        print("ROW", row)
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

        print(soup)

        sleep(5)

        # # 각 아이템의 회사 이름 가져오기
        company_name = get_column_value(soup, ".company_name", default_parser)
        print("COMPANY NAME", company_name)

        url = row 

        # # 각 아이템의 모집 집종 가져오기
        # print("JOB SECTOR", row.find_element_by_css_selector('.job_sector').text) 


        # # # 각 아이템의 근무 주소 가져오기
        work_location = get_column_value(soup, "#map_0 > div > address > span", default_parser)
        print("WORK LOCATION", work_location)

        # # # 각 아이템의 이력서 제출 형식 가져오기
        resume_submission_format = get_column_value(soup, '.template', default_parser)
        print("RESUME SUBMISSION FORMAT", resume_submission_format)

        # # 각 아이템의 모집 마감 날짜 가져오기
        deadline = get_column_value(soup, '.info_period > dd:nth-child(4)', deadline_parser)
        print("DEADLINE", deadline)
        
        # # # 각 아이템의 복리후생 가져오기
        benefit = get_column_value(soup, '.jv_benefit', default_parser)
        print("BENEFIT", benefit)
        
        # driver.back()

    # for row in rows:
    #     deadline = row.find_element_by_css_selector('.deadlines').text
    #     if is_recruit_junior():
    #         career = row.find_element_by_css_selector(".career").text
    #         if "신입" in career:
    #             return true
    #         elif "경력무관" in career:
    #             return true
    #         return false

    #     if is_deadline_over_ten_days(deadline):
    #         print(url)
    #         url = row.find_element_by_css_selector('.str_tit').get_attribute('href')
    #         driver.get(url)

    # row = driver.find_element_by_css_selector("a[id*='rec_link']")
    # print(row.get_attribute("href"))
    
    
    # driver.get(row.get_attribute("href"))
    # print(row.click())


    # driver.get(row.get_attribute("href"))
    # driver.implicitly_wait(10)

    # html = driver.page_source
    # soup = bs4(html, 'html.parser')

    # print(soup)


    # WebDriverWait(driver, 10)
    # html = driver.page_source
    # soup = bs4(html, 'html.parser')
    # print(soup)



    # sleep(1000)    


    # row = driver.find_element_by_css_selector("#default_list_wrap > section > div.list_body > .list_item")
    # print(row)
    # driver.find_element(By.NAME, q).send_keys("cheese" + Keys.RETURN)
    # first_result = wait.until(presence_of_element_located(By.CSSSELECTOR, "h3>div"))
    # print(first_result.get_attribute("textContent"))