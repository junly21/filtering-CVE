# Theori-Recruit-assignment

## Description
You can crawl data at https://www.cvedetails.com and store in database. Each api help you search data filtering by date/score.

## Environment
Python3</br>
Fastapi</br>
mongoDB


## Prerequisite
all you need are in requirements.txt

## Usage

1. open your terminal and install all packages </br> ``` pip install -r requirements.txt ``` </br>*if you want, you can build docker-compose* </br></br>
2.  you can run project by type ```uvicorn main:app --reload``` in your terminal </br></br>
3. http://127.0.0.1:8000/crawl_since_2022 this URL crawl cve list since 2002</br></br>
4. **last_page_{year}.txt** writes number of finished pages to consider situation where the network might go down in the middle of a crawl, or the
computer the crawler is running on might suddenly turn off.</br></br> 
5. by using http://127.0.0.1:8000/findby_publish_date/?start_date={start_date}&end_date={end_date}, you can search data filtered by puplished date. you can input only start date or end date. you can also input both of them. but it returns error in this cases: <ol>1.date type error</br>2.if end date is faster than start date  </ol></br> 
6. you can change **publish_date** in URL to **update_date** to filter data by update date.</br></br> 
7. by using http://127.0.0.1:8000/findby_cvss_score/?min_score={점수입력}&max_score={점수입력}을 you can filter data by cvss score range.</br></br>