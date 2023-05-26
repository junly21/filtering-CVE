from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from fastapi import FastAPI
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
from fastapi import FastAPI
import requests
from pymongo import MongoClient
from datetime import datetime
import os
client = MongoClient('localhost', 27017)
db = client.crawlingDb
app = FastAPI()
@app.get("/crawl_since_2022")
def crawl_since_2022():
    for i in range(1,3):
        options = Options()
        options.binary_location = "/opt/homebrew/Caskroom/google-chrome/113.0.5672.126/Google Chrome.app"  # chrome binary location specified here
        options.add_argument("--start-maximized")  # open Browser in maximized mode
        options.add_argument("--no-sandbox")  # bypass OS security model
        options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome('chromedriver', options=options)
        driver.get('https://www.google.com/')

        # 페이지가 완전히 로딩되도록 3초동안 기다림
        time.sleep(3)

        pagingb_element = driver.find_element_by_class("ContentHeaderView-module__tab_list___BWrWe")
        a_tags = pagingb_element.find_elements_by_tag_name("li")
        how_many_pages = len(a_tags)


    # 웹 드라이버 종료
    driver.quit()

    return {"t":how_many_pages}
    # data = []
    # for year in range(2022, 2024):
    #     webdriver_service = Service('/Users/joon/Downloads/chromedriver_mac_arm64/chromedriver')
    #     # 웹 드라이버 옵션 설정
    #     options = Options()
    #     options.add_argument("--headless")  # 브라우저 창을 띄우지 않고 실행할 경우
    #
    #     driver = webdriver.Chrome(service=webdriver_service, options=options)
    #
    #     # 크롬 드라이버에 url 주소 넣고 실행
    #     driver.get('https://www.cvedetails.com/vulnerability-list/year'+{year}+'/vulnerabilities.html')
    #
    #     # 페이지가 완전히 로딩되도록 3초동안 기다림
    #     time.sleep(3)
    #
    #     pagingb_element = driver.find_element_by_id("pagingb")
    #     a_tags = pagingb_element.find_elements_by_tag_name("a")
    #     how_many_pages = len(a_tags)
    #
    #     #연도별로 데이터 수집하는 구간. 테스트를 위해 200개씩만 수집
    #     # for i in range(1, how_many_pages + 1):
    #     for i in range(1, 3):
    #         try:
    #             # i페이지로 이동
    #             driver.find_element_by_xpath('//*[@id="pagingb"]/a[' + {i} + ']').click()
    #             table = driver.find_element(By.CLASS_NAME, "searchresults")
    #             tr_elements = table.find_elements(By.TAG_NAME, "tr")
    #
    #             for idx, tr in enumerate(tr_elements):
    #                 td_elements = tr.find_elements(By.TAG_NAME, "td")
    #                 #0번 tr은 칼럼명을 담고있음
    #                 if idx == 0:
    #                     continue
    #                 #짝수번째 tr은 summary를 담고잇어서 제외.
    #                 if idx % 2 == 1:
    #                     cve_id = td_elements[1].text.strip()
    #                     publish_date = td_elements[5].text.strip()
    #                     update_date = td_elements[6].text.strip()
    #                     cvss = float(td_elements[7].text.strip())
    #
    #                     #중단된 경우를 위해 데이터베이스에 이미 존재하는 cve_id인지 확인
    #                     existing_data = db.data.find_one({"cve_id": cve_id})
    #                     if existing_data:
    #                         continue  # 이미 존재하는 경우 데이터 삽입을 건너뜁니다.
    #
    #                     doc = {
    #                         'cve_id': cve_id,
    #                         'publish_date': publish_date,
    #                         'update_date': update_date,
    #                         'score': cvss
    #                     }
    #                     db.data.insert_one(doc)
    #         except requests.exceptions.RequestException as e:
    #             # 네트워크 연결이 끊겼거나 요청에 오류가 발생한 경우에 대한 예외 처리
    #             print(f"An error occurred: {e}")
    #             # 로그에 에러 메시지를 출력하거나, 예외를 적절하게 처리할 수 있습니다.
    #
    #         except Exception as e:
    #             # 다른 예외 상황에 대한 예외 처리
    #             print(f"An unexpected error occurred: {e}")
    #             # 로그에 에러 메시지를 출력하거나, 예외를 적절하게 처리할 수 있습니다.
    #
    # # 웹 드라이버 종료
    # driver.quit()
    #
    # return {"message": "done"}



    # data = []
    # driver = webdriver.Chrome('./chromedriver')
    # for year in range(2022, 2024):
    #     # response = requests.get(f"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year={year}&month=0&cweid=0&order=1")
    #     # soup = BeautifulSoup(response.content, "html.parser")
    #
    #     # 크롬 드라이버에 url 주소 넣고 실행
    #     driver.get('https://www.cvedetails.com/vulnerability-list/year'+{year}+'/vulnerabilities.html')
    #
    #     # 페이지가 완전히 로딩되도록 3초동안 기다림
    #     time.sleep(3)
    #
    #     # how_many_pages라는 변수에 각 년도의 cve_id가 몇 페이지까지 있는지 담아둡니다.
    #     # paging = soup.find('div', {'id': 'pagingb'})
    #     # paging_elements = paging.find_all("a")
    #     #how_many_pages = len(paging_elements)
    #
    #     pagingb_element = driver.find_element_by_id("pagingb")
    #     a_tags = pagingb_element.find_elements_by_tag_name("a")
    #     how_many_pages = len(a_tags)
    #
    #     # # 네트워크 중단을 위해 어디까지 저장했는지
    #     # last_page = load_last_page_from_file(year)  # 이전에 저장한 마지막 페이지 번호를 불러옵니다.
    #     # if last_page is not None and last_page > 0:
    #     #     start_page = last_page + 1
    #     # else: #저장된 중단 백업용 파일이 없다면
    #     #     start_page = 1
    #
    #
    #     #연도별로 데이터 수집하는 구간. 테스트를 위해 200개씩만 수집
    #     # for i in range(1, how_many_pages + 1):
    #     for i in range(1, 5):
    #         try:
    #             # i페이지로 이동
    #             driver.find_element_by_xpath('//*[@id="pagingb"]/a[' + {i} + ']').click()
    #             # response = requests.get(f"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page={i}&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year={year}&month=0&cweid=0&order=1")
    #             # soup = BeautifulSoup(response.content, "html.parser")
    #             # table = soup.find('table', {'class': 'searchresults sortable'})
    #             table = driver.find_element(By.CLASS_NAME, "searchresults")
    #             tr_elements = table.find_elements(By.TAG_NAME, "tr")
    #             # tr_elements = table.find_all("tr")
    #
    #             for idx, tr in enumerate(tr_elements):
    #                 #td_elements = tr.find_all('td')
    #                 td_elements = tr.find_elements(By.TAG_NAME, "td")
    #                 #0번 tr은 칼럼명을 담고있음
    #                 if idx == 0:
    #                     continue
    #                 #짝수번째 tr은 summary를 담고잇어서 제외.
    #                 if idx % 2 == 1:
    #                     cve_id = td_elements[1].text.strip()
    #                     publish_date = td_elements[5].text.strip()
    #                     update_date = td_elements[6].text.strip()
    #                     cvss = float(td_elements[7].text.strip())
    #
    #                     #중단된 경우를 위해 데이터베이스에 이미 존재하는 cve_id인지 확인
    #                     existing_data = db.data.find_one({"cve_id": cve_id})
    #                     if existing_data:
    #                         continue  # 이미 존재하는 경우 데이터 삽입을 건너뜁니다.
    #
    #                     doc = {
    #                         'cve_id': cve_id,
    #                         'publish_date': publish_date,
    #                         'update_date': update_date,
    #                         'score': cvss
    #                     }
    #                     db.data.insert_one(doc)
    #             #save_last_page_to_file(year, i)  # 현재 페이지 번호를 파일에 저장합니다.
    #         except requests.exceptions.RequestException as e:
    #             # 네트워크 연결이 끊겼거나 요청에 오류가 발생한 경우에 대한 예외 처리
    #             print(f"An error occurred: {e}")
    #             # 로그에 에러 메시지를 출력하거나, 예외를 적절하게 처리할 수 있습니다.
    #
    #         except Exception as e:
    #             # 다른 예외 상황에 대한 예외 처리
    #             print(f"An unexpected error occurred: {e}")
    #             # 로그에 에러 메시지를 출력하거나, 예외를 적절하게 처리할 수 있습니다.
    #
    #
    #
    # return {"message": "done"}

#http://127.0.0.1:8000/findby_publish_date/?start_date=2022-12-22&end_date=2022-12-29
@app.get("/findby_publish_date/")
def findby_publish_date(start_date: str = None, end_date: str = None):

    if start_date and end_date:
        try:
            # 날짜 형식이 올바른지 확인
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")

            # 시작일이 끝일보다 이전인지 확인
            if start_date > end_date:
                return {"error": "시작일은 끝일보다 이전이어야 합니다."}

        except ValueError:
            return {"error": "올바른 날짜 형식을 입력해야 합니다. (예: 2022-12-31)"}

    elif start_date and not end_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            return {"error": "올바른 날짜 형식을 입력해야 합니다. (예: 2022-12-31)"}

    elif end_date and not start_date:
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return {"error": "올바른 날짜 형식을 입력해야 합니다. (예: 2022-12-31)"}

    query = {}

    #시작일, 끝일 둘다 설정
    if start_date and end_date:
        query["publish_date"] = {
            "$gte": start_date,
            "$lte": end_date
        }
    elif start_date:
        query["publish_date"] = {
            "$gte": start_date
        }
    elif end_date:
        query["publish_date"] = {
            "$lte": end_date
        }

    result = db.data.find(query)
    data=[]
    count = 0
    for item in result:
        item.pop('_id', None)  # 'ObjectId' 필드 제거
        data.append(item)
        count += 1

    return {
        "data": data,
        "count": count
    }

#http://127.0.0.1:8000/findby_update_date/?start_date=2022-12-22&end_date=2022-12-29
@app.get("/findby_update_date/")
def findby_update_date(start_date: str = None, end_date: str = None):

    if start_date and end_date:
        try:
            # 날짜 형식이 올바른지 확인
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")

            # 시작일이 끝일보다 이전인지 확인
            if start_date > end_date:
                return {"error": "시작일은 끝일보다 이전이어야 합니다."}

        except ValueError:
            return {"error": "올바른 날짜 형식을 입력해야 합니다. (예: 2022-12-31)"}

    elif start_date and not end_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            return {"error": "올바른 날짜 형식을 입력해야 합니다. (예: 2022-12-31)"}

    elif end_date and not start_date:
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return {"error": "올바른 날짜 형식을 입력해야 합니다. (예: 2022-12-31)"}

    query = {}
    if start_date and end_date:
        query["update_date"] = {
            "$gte": start_date,
            "$lte": end_date
        }
    elif start_date:
        query["update_date"] = {
            "$gte": start_date
        }
    elif end_date:
        query["update_date"] = {
            "$lte": end_date
        }

    result = db.data.find(query)
    data = []
    count = 0
    for item in result:
        item.pop('_id', None)  # 'ObjectId' 필드 제거
        data.append(item)
        count += 1

    return {
        "data": data,
        "count": count
    }

#http://127.0.0.1:8000/findby_cvss_score/?min_score=0&max_score=0
@app.get("/findby_cvss_score/")
def findby_cvss_score(min_score: float = None, max_score: float = None):
    query = {}

    # 최소 점수와 최대 점수 설정
    if min_score is not None and max_score is not None:
        query["score"] = {
            "$gte": min_score,
            "$lte": max_score
        }
    elif min_score is not None:
        query["score"] = {
            "$gte": min_score
        }
    elif max_score is not None:
        query["score"] = {
            "$lte": max_score
        }

    result = db.data.find(query)
    data = []
    count = 0
    for item in result:
        item.pop('_id', None)  # 'ObjectId' 필드 제거
        data.append(item)
        count += 1

    return {
        "data": data,
        "count": count
    }