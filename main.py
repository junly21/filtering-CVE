from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import os
client = MongoClient('mongodb', 27017)
db = client.crawlingDb
app = FastAPI()

def get_page_counts(year):
    response = requests.get(f"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=64&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year={year}&month=0&cweid=0&order=1")
    soup = BeautifulSoup(response.content, "html.parser")
    paging = soup.find('div', {'id': 'pagingb'})
    paging_elements = paging.find_all("a")
    return len(paging_elements)

def extract_text_from_element(element):
    return element.text.strip()

def extract_float_from_element(element):
    return float(element.text.strip())

def process_table_row(row):
    td_elements = row.find_all('td')
    cve_id = extract_text_from_element(td_elements[1])
    vulnerability_type = extract_text_from_element(td_elements[4])
    publish_date = extract_text_from_element(td_elements[5])
    update_date = extract_text_from_element(td_elements[6])
    cvss = extract_float_from_element(td_elements[7])

    existing_data = db.data.find_one({"cve_id": cve_id})
    if existing_data:
        return None

    doc = {
        'cve_id': cve_id,
        'vulnerability_type': vulnerability_type,
        'publish_date': publish_date,
        'update_date': update_date,
        'score': cvss
    }
    db.data.insert_one(doc)
    doc.pop('_id', None)
    return doc
def save_last_page_to_file(year, page_number):
    filename = f"last_page_{year}.txt"  # 해당 연도에 대한 파일명 생성
    with open(filename, "w") as file:
        file.write(str(page_number))  # 현재 페이지 번호를 파일에 저장

def load_last_page_from_file(year):
    filename = f"last_page_{year}.txt"  # 해당 연도에 대한 파일명 생성
    if os.path.exists(filename):  # 파일이 존재하는 경우
        with open(filename, "r") as file:
            last_page = int(file.read())  # 저장된 페이지 번호를 읽어옴
        return last_page
    else:  # 파일이 존재하지 않는 경우
        return None

@app.get("/")
def home():
    return{"data":"test2ㅇㅇ"}
@app.get("/crawl_since_2022")
def crawl_since_2022():
    data = []

    for year in range(2022, 2024):
        response = requests.get(f"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=64&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year={year}&month=0&cweid=0&order=1")
        soup = BeautifulSoup(response.content, "html.parser")

        # page_counts라는 변수에 각 년도의 cve_id가 몇 페이지까지 있는지 담아둡니다.
        paging = soup.find('div', {'id': 'pagingb'})
        paging_elements = paging.find_all("a")
        page_counts = get_page_counts(year)

        # 네트워크 중단고려. 어디까지 저장했는지
        last_page = load_last_page_from_file(year)  # 이전에 저장한 마지막 페이지 번호를 불러옵니다.
        if last_page is not None and last_page > 0:
            start_page = last_page + 1
        else: #저장된 중단 백업용 파일이 없다면
            start_page = 1

        #연도별로 데이터 수집하는 구간. 우선은 테스트를 위해 주석처리 후 연도별 200개씩만 수집
        # for i in range(start_page, page_counts + 1):
        for i in range(start_page, 5):
            try:
                href = paging_elements[i-1].attrs['href']
                response = requests.get(f"https://www.cvedetails.com"+href)
                soup = BeautifulSoup(response.content, "html.parser")
                table = soup.find('table', {'class': 'searchresults sortable'})
                tr_elements = table.find_all("tr")
                for idx, tr in enumerate(tr_elements):
                    td_elements = tr.find_all('td')
                    #0번 tr은 칼럼명을 담고있어서 스킵
                    if idx == 0:
                        continue
                    #짝수번째 tr은 summary를 담고잇어서 제외.
                    if idx % 2 == 1:
                        doc = process_table_row(tr)
                        if doc is not None:
                            data.append(doc)
                save_last_page_to_file(year, i)  # 현재 페이지 번호를 파일에 저장
            except requests.exceptions.RequestException as e:
                # 네트워크 연결이 끊겼거나 요청에 오류가 발생한 경우에 대한 예외 처리
                print(f"An error occurred: {e}")
                # 로그에 에러 메시지를 출력하거나, 예외를 적절하게 처리할 수 있습니다.

            except Exception as e:
                # 다른 예외 상황에 대한 예외 처리
                print(f"An unexpected error occurred: {e}")
                # 로그에 에러 메시지를 출력하거나, 예외를 적절하게 처리할 수 있습니다.



    return {"message": "완" }


@app.get("/findby_publish_date/") #publish date로 filtering
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

    #시작일, 끝일 둘다 설정된 경우
    if start_date and end_date:
        query["publish_date"] = {
            "$gte": start_date,
            "$lte": end_date
        }
    elif start_date: #하나씩만 설정된 경우
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
@app.get("/findby_cvss_score/") #score기준 filtering
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