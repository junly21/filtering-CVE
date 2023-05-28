from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import os
client = MongoClient('localhost', 27017) #로컬환경
db = client.crawlingDb
app = FastAPI()

'''
it counts how many pages in each year(2022, 2023)
'''


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


'''
you can find information of cve_id ~ cvss score in each row. it extract data and insert to DB 
'''


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


'''
considering shut down,
.txt file write which page you crawled last.
if you start crawl again after shut down, load number from last page and crawl again 
'''


def save_last_page_to_file(year, page_number):
    filename = f"last_page_{year}.txt"
    with open(filename, "w") as file:
        file.write(str(page_number))


def load_last_page_from_file(year):
    filename = f"last_page_{year}.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            last_page = int(file.read())
        return last_page
    else:
        return None


def validate_date_format(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


@app.get("/")
def home():
    return{"hello, you can start crawl cve list"}


'''
it crawls list since 2022 and insert in database to search and filter data 
'''


# http://127.0.0.1:8000/
@app.get("/crawl_since_2022")
def crawl_since_2022():
    data = []

    for year in range(2022, 2024):
        response = requests.get(f"https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=64&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year={year}&month=0&cweid=0&order=1")
        soup = BeautifulSoup(response.content, "html.parser")

        # count pages each year
        paging = soup.find('div', {'id': 'pagingb'})
        paging_elements = paging.find_all("a")
        page_counts = get_page_counts(year)

        # considering shutdown
        last_page = load_last_page_from_file(year)
        if last_page is not None and last_page > 0:
            start_page = last_page + 1
        else:
            start_page = 1

        # find and insert data
        for i in range(start_page, page_counts + 1):
            try:
                href = paging_elements[i-1].attrs['href']
                response = requests.get(f"https://www.cvedetails.com"+href)
                soup = BeautifulSoup(response.content, "html.parser")
                table = soup.find('table', {'class': 'searchresults sortable'})
                tr_elements = table.find_all("tr")
                for idx, tr in enumerate(tr_elements):
                    if idx == 0:
                        continue
                    if idx % 2 == 1:
                        doc = process_table_row(tr)
                        if doc is not None:
                            data.append(doc)
                save_last_page_to_file(year, i)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    return {"message": "crawling finished" }


'''
you can search data filter by publish_date
'''


# http://127.0.0.1:8000/findby_publish_date/?start_date=2022-12-22&end_date=2022-12-29
@app.get("/findby_publish_date/") #publish date로 filtering
def findby_publish_date(start_date: str = None, end_date: str = None):

    if start_date and not validate_date_format(start_date):
        return {"error": "please input correct dataType. (ex: 2022-12-31)"}

    if end_date and not validate_date_format(end_date):
        return {"error": "please input correct dataType. (ex: 2022-12-31)"}

    if start_date and end_date and start_date > end_date:
        return {"error": "end_date cannot be faster than start_date."}

    query = {}

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
        item.pop('_id', None)
        data.append(item)
        count += 1

    return {
        "data": data,
        "count": count
    }


'''
you can search data filter by publish_date
'''


# http://127.0.0.1:8000/findby_update_date/?start_date=2022-12-22&end_date=2022-12-29
@app.get("/findby_update_date/")
def findby_update_date(start_date: str = None, end_date: str = None):

    if start_date and not validate_date_format(start_date):
        return {"error": "please input correct dataType. (ex: 2022-12-31)"}

    if end_date and not validate_date_format(end_date):
        return {"error": "please input correct dataType. (ex: 2022-12-31)"}

    if start_date and end_date and start_date > end_date:
        return {"error": "end_date cannot be faster than start_date."}

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
        item.pop('_id', None)
        data.append(item)
        count += 1

    return {
        "data": data,
        "count": count
    }


'''
you can search data filter cvss score
'''


# http://127.0.0.1:8000/findby_cvss_score/?min_score=0&max_score=0
@app.get("/findby_cvss_score/")
def findby_cvss_score(min_score: float = None, max_score: float = None):

    query = {}

    # 최소 점수와 최대 점수 설정
    if min_score is not None and max_score is not None:
        if min_score > max_score:
            return {"error": "max_score cannot be smaller than min_score"}
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
        item.pop('_id', None)
        data.append(item)
        count += 1

    return {
        "data": data,
        "count": count
    }