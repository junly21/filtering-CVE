# Theori-Recruit-assignment

## Description
https://www.cvedetails.com 사이트의 데이터를 크롤링하 DB에 저장 후 api에 따라 기간/점수로 filtering하는 코드입니다.

## Environment
실행환경

## Prerequisite
1. FastAPI
2. requests
3. BeautifulSoup
4. pymongo

## Usage

1. http://127.0.0.1:8000/crawl_since_2022 로 접속하면 크롤링을 통해 2022년도부터 2023년도까지의 cve data를 수집합니다.</br></br>
2. 이 때 생성되는 last_page_{year}.txt는 네트워크 혹은 컴퓨터가 down 될 경우를 고려해 몇년도의 몇페이지까지 정보를 저장하였는지 작성합니다.</br></br>
4. http://127.0.0.1:8000/findby_publish_date/?start_date={시작날짜}&end_date={종료날짜}를 통해 publish date filter를 설정하여 데이터를 조회할 수 있습니다. 시작일과 종료일 둘 다 입력해도 괜찮고, 둘 중 하나만 입력해도 괜찮습니다. 단,  이 때 날짜의 형식이 맞지 않거나 시작 날짜보다 종료일이 빠르면 오류를 반환합니다.</br></br>
5. publish_date를 update_date로 바꾸어 업데이트 일에 따른 filtering이 가능합니다.</br></br>
6. #http://127.0.0.1:8000/findby_cvss_score/?min_score={점수입력}&max_score={점수입력}을 통해 score로 filtering을 할 수 있습니다.</br></br>