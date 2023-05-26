from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.crawlingDb

print('Start')

app = FastAPI()

@app.get("/")
def home():
    return{"data":"test"}


@app.get("/findby_year/{year}")
def findby_year(year: str):
    response = requests.get("https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year="+str(year)+"&month=0&cweid=0&order=1")
    soup = BeautifulSoup(response.content, "html.parser")

    # how_many_pages라는 변수에 몇 페이지까지 있는지 담아둡니다.
    paging = soup.find('div', {'id': 'pagingb'})
    paging_elements = paging.find_all("a")
    how_many_pages = len(paging_elements)
    data = []

    for i in range(1, 4):
        response = requests.get("https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page="+str(i)+"&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year="+str(year)+"&month=0&cweid=0&order=1")
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table', {'class': 'searchresults sortable'})
        tr_elements = table.find_all("tr")
        for idx, tr in enumerate(tr_elements):
            td_elements = tr.find_all('td')
            if idx == 0:
                continue
            if idx % 2 == 1:
                cve_id = td_elements[1].text.strip()
                publish_date = td_elements[5].text.strip()
                update_date = td_elements[5].text.strip()
                cvss = td_elements[7].text.strip()
                #data.append([cve_id, cvss])
                doc = {
                    'cve_id': cve_id,
                    'publish_date': publish_date,
                    'update_date': update_date,
                    'score': cvss
                }
                db.data.insert_one(doc)


    return {"message" : "done"}
    #return{"data":data}
    #return{"data":data, "p":how_many_pages}

@app.get("/findby_publish_date/")
def find_by_publish_date(start_date: str = None, end_date: str = None):
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
    data = []
    for item in result:
        item.pop('_id', None)  # 'ObjectId' 필드 제거
        data.append(item)

    return data
    return list(result)


@app.get("/findby_update_date/")
def find_by_update_date(start_date: str = None, end_date: str = None):
    query = {}

    #시작일, 끝일 둘다 설정
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
    for item in result:
        item.pop('_id', None)  # 'ObjectId' 필드 제거
        data.append(item)

    return data
    return list(result)