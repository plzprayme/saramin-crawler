from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from bs4 import BeautifulSoup as bs4

from time import sleep

from datetime import date, timedelta

def filter_recruitment(rows):
    rows = filter_career_condition(rows)
    print("AFTER FILTER CAREER LEN", len(rows))
    rows = filter_deadline_condition(rows)
    print("AFTER DEADLINE CAREER LEN", len(rows))
    return rows

def filter_career_condition(rows):
    result = []
    for row in rows:
        career_condition = row.find_element_by_css_selector(".career").text

        if "신입" in career_condition or "경력무관" in career_condition:
            print("FILTERED CAREER CONDITION", career_condition)
            result.append(row)
        else:
            print("UNFILTERED CAREER CONDITION", career_condition)

    
    return result

def filter_deadline_condition(rows):
    result = []
    for row in rows:
        deadline = row.find_element_by_css_selector('.deadlines').text
        try:
            if is_deadline_over_ten_days(deadline):
                print("FILTERED DEADLINE OVER 10 DAYS", deadline)
                result.append(row)
        except:
            print("CATCH ERROR", deadline)
    
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

with webdriver.Chrome("C:/Users/prayme/chromedriver") as driver:
    wait = WebDriverWait(driver, 10)

    driver.get("http://www.saramin.co.kr/zf_user/jobs/list/domestic?loc_mcd=105000&cat_cd=404%2C407%2C408%2C402%2C409%2C416%2C413%2C411%2C417%2C410&panel_type=&search_optional_item=n&search_done=y&panel_count=y")
    
    rows = driver.find_elements_by_css_selector("#default_list_wrap > section > div.list_body > .list_item")
    print("BEFORE", len(rows))
    rows = filter_recruitment(rows)
    print("AFTER", len(rows))
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