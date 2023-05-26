from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
print('Start')

app = FastAPI()

@app.get("/")
def home():
    return{"data":"test"}

@app.get("/")
def home():
    return{"data":"test"}

@app.get("/findby/{year}")
def findBy(year: str):
    base_url = "https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year="+str(year)+"&month=0&cweid=0&order=1&trc=25227&sha=45d566efbc1f55ce107b057217e11d794a7bc4fb"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # how_many_pages라는 변수에 몇 페이지까지 있는지 담아둡니다.
    paging = soup.find('div', {'id': 'pagingb'})
    paging_elements = paging.find_all("a")
    how_many_pages = len(paging_elements)
    data = []

    for i in range(1, 3):
        response = requests.get("https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page="+str(i)+"&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year=2022&month=0&cweid=0&order=1&trc=25227&sha=45d566efbc1f55ce107b057217e11d794a7bc4fb")
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table', {'class': 'searchresults sortable'})
        tr_elements = table.find_all("tr")
        for idx, tr in enumerate(tr_elements):
            td_elements = tr.find_all('td')
            if idx == 0:
                continue
            if idx % 2 == 1:
                cve_id = td_elements[1].text.strip()
                cvss = td_elements[7].text.strip()
                data.append([cve_id, cvss])

    #return{"data":data}
    return{"data":data, "p":how_many_pages}