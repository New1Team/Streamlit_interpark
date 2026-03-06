from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup as bs
from requests import get
import json
import asyncio
import streamlit as st

app = FastAPI()

origins = [ "http://localhost","http://localhost:5173" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 통계 정보 실시간 수집 함수
def get_statistic(id:str, placeCode:str):
  url = f"https://tickets.interpark.com/contents/api/statistics/booking/{id}?placeCode={placeCode}"
  res = get(url)
  if res.status_code == 200:
    return json.loads(res.text).get('ageGender',{})
  return {}

# API 작동 확인용
@app.get("/")
def read():
    return {"status": True}

# 데이터 수집
@app.get('/getData')
async def getData(genre:str):
  if 'link_index' not in st.session_state:
    st.session_state.link_index = 0
  # 인터파크 장르별 URL
  # option = ["MUSICAL", "CONCERT", "CLASSIC", "KIDS", "DRAMA", "EXHIBIT", "SPORTS", "LEISURE"]
  key = f'@"/ranking","?period=D&page=1&pageSize=50&rankingTypes={genre}",'
  # code = option[st.session_state.link_index]
  url = f"https://tickets.interpark.com/contents/ranking?genre={genre}"
  res = get(url)
  if res.status_code != 200:
    return {"error":"접속 실패"}
  if res.status_code == 200:
    tickets = [] # { 장르, 티켓이름, 장소, 시작날짜, 종료날짜, 예매율 }
    soup = bs(res.text, "html.parser")
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
    if not script_tag:
      return {"error": "데이터를 찾을 수 없습니다."}
    json_data = json.loads(script_tag.string)
    st.json(json_data, expanded=False)
    tickets = json_data.get('props', {}).get('pageProps', {}).get('fallback', {}).get(key, [])
    
    # 실시간 통계에 따른 상위 10개 작품 추출
    top_10 = tickets[:10]
    results = []
    for v in top_10:
      # 실시간 통계 데이터 추출
      statistic = get_statistic(v['goodsCode'], v['placeCode'])
      # 공연 정보 데이터 + 통계 데이터
      data = {
        "id": v['goodsCode'],
          "title": v['goodsName'],
          "placeName": v['placeName'],
          "playStartDate": v['playStartDate'],
          "playEndDate": v['playEndDate'],
          "bookingPercent": float(v['bookingPercent']) if v['bookingPercent'] else 0,
          "genre": genre,
          # 통계 데이터 없으면 0으로 처리
          "age10Rate": statistic.get("age10Rate", 0),
          "age20Rate": statistic.get("age20Rate", 0),
          "age30Rate": statistic.get("age30Rate", 0),
          "age40Rate": statistic.get("age40Rate", 0),
          "age50Rate": statistic.get("age50Rate", 0),
          "maleRate": statistic.get("maleRate", 0),
          "femaleRate": statistic.get("femaleRate", 0),
      }
      results.append(data)

    # 전체 기준 가공데이터인데 이부분은 잘 모르겠음
    avg_booking = sum(float(t['bookingPercent']) for t in tickets if t['bookingPercent']) / len(tickets) if tickets else 0
    return {
      "summary":{
        "totalCount": len(tickets),
        "avgBooking": round(avg_booking, 1)
      },
      "top10":results
    }

# def crawlingMelon(code: str):
#   # if head is None:
#   #   head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
#   url = f"https://tickets.interpark.com/contents/ranking?genre={code}"
#   res = get(url)
#   arr = []
#   if res.status_code == 200:
#     data = bs(res.text)
#     arr = getData(data)
#     if len(arr) > 0:
#       sql2 = f"""
#           INSERT INTO edu.`ticket` 
#           (`id`, `title`,`placeCode`, `genre`, `placeName`, `playStartDate`, `playEndDate`, `bookingPercent`)
#           VALUE
#           (%s, %s, %s, %s, %s, %s, %s, %s)
#           ON DUPLICATE KEY UPDATE
#             id=VALUES(id),
#             title=VALUES(title),
#             placeCode=VALUES(placeCode),
#             genre=VALUES(genre),
#             placeName=VALUES(placeName),
#             playStartDate=VALUES(playStartDate),
#             playEndDate=VALUES(playEndDate),
#             bookingPercent=VALUES(bookingPercent)
#       """
#       values = [(row["goodsCode"], row["goodsName"], row["placeCode"], row["genre"], row["placeName"], row["playStartDate"], row["playEndDate"], row["bookingPercent"]) for row in arr]
#       saveMany(sql2, values)
#   return arr

# def statistic():
#   sql1 = "SELECT id, placeCode FROM edu.ticket;"
#   data = findAll(sql1)

#   #  이미 있는 데이터 중복처리 방지용입니당
#   sql_exist = "SELECT id FROM edu.statistic;"
#   exist_ids = set(row["id"] for row in findAll(sql_exist))

#   for i in range(len(data)):
#     row = data[i]
#     id = row["id"]
#     placeCode = row["placeCode"]

#     #  이미 있는 데이터 중복처리 방지용입니당
#     if id in exist_ids:
#       continue

#     url = f"https://tickets.interpark.com/contents/api/statistics/booking/{id}?placeCode={placeCode}"
#     res = get(url)
#     if res.status_code == 200:
#       json_data = json.loads(res.text)
#       jData = json_data['ageGender']
#       sql =  f"""
#           INSERT INTO edu.`statistic` 
#           (`id`, `age10Rate`,`age20Rate`, `age30Rate`, `age40Rate`, `age50Rate`, `maleRate`, `femaleRate`)
#           VALUE
#           (%s, %s, %s, %s, %s, %s, %s, %s)
#           ON DUPLICATE KEY UPDATE
#             age10Rate=VALUES(age10Rate),
#             age20Rate=VALUES(age20Rate),
#             age30Rate=VALUES(age30Rate),
#             age40Rate=VALUES(age40Rate),
#             age50Rate=VALUES(age50Rate),
#             maleRate=VALUES(maleRate),
#             femaleRate=VALUES(femaleRate)
#       """
#       values = [(id, jData["age10Rate"], jData["age20Rate"], jData["age30Rate"], jData["age40Rate"], jData["age50Rate"], jData["maleRate"], jData["femaleRate"])]
#       saveMany(sql, values)

# selected = st.selectbox(
#   label="음원 장르를 선택하세요",
#   options=option,
#   index=None,
#   placeholder="수집 대상을 선택하세요."
# )

# if st.button("통계 수집"):
#   statistic()

# if selected:
#   st.write("선택한 장르 :", selected)
#   st.session_state.link_index = option.index(selected)
#   if st.button(f"'{option[st.session_state.link_index]}' 수집"):
#     crawlingMelon(f"{option[st.session_state.link_index]}")
#     # if getData() == 0:
#     #   st.text("수집된 데이터가 없습니다.")