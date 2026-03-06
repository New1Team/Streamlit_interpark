from fastapi import FastAPI, Query
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from Streamlit_interpark.backend.pages.db import findAll
from bs4 import BeautifulSoup as bs
from requests import get
import json

app = FastAPI(title="Interpark Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": True}

# -----------------------------
# 1) DB에서 JOIN 데이터 로드
# -----------------------------
sql = """
    SELECT
        t.id,
        t.title,
        t.genre,
        t.placeName,
        t.playStartDate,
        t.playEndDate,
        t.bookingPercent,
        s.age10Rate,
        s.age20Rate,
        s.age30Rate,
        s.age40Rate,
        s.age50Rate,
        s.maleRate,
        s.femaleRate
    FROM edu.ticket t
    JOIN edu.statistic s
    ON t.id = s.id
"""

def loadDf():
    rows = findAll(sql)
    dfAll = pd.DataFrame(rows)

    if len(dfAll) == 0:
        return dfAll

    dfAll["playStartDate"] = pd.to_datetime(dfAll["playStartDate"], errors="coerce")
    dfAll["playEndDate"] = pd.to_datetime(dfAll["playEndDate"], errors="coerce")

    dfAll["bookingPercent"] = (
        dfAll["bookingPercent"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )
    dfAll["bookingPercent"] = pd.to_numeric(dfAll["bookingPercent"], errors="coerce")

    rate_cols = ["age10Rate", "age20Rate", "age30Rate", "age40Rate", "age50Rate", "maleRate", "femaleRate"]
    for c in rate_cols:
        dfAll[c] = pd.to_numeric(dfAll[c], errors="coerce")

    dfAll = dfAll.dropna(subset=["genre", "title", "playEndDate", "bookingPercent"])

    today = pd.Timestamp(datetime.today())
    dfAll["remainDays"] = (dfAll["playEndDate"] - today).dt.days

    return dfAll

# -----------------------------
# 2) 장르 필터
# -----------------------------
def genreFilter(dfAll: pd.DataFrame, genre: str):
    df = dfAll.copy()
    if genre != "전체":
        df = df[df["genre"] == genre].copy()
    return df

def cleanCode(df: pd.DataFrame):
    out = df.copy()

    if "playStartDate" in out.columns:
        out["playStartDate"] = out["playStartDate"].astype(str)

    if "playEndDate" in out.columns:
        out["playEndDate"] = out["playEndDate"].astype(str)

    return out.to_dict(orient="records")

@app.get("/statistic/genres")
def genres():
    dfAll = loadDf()
    if len(dfAll) == 0:
        return {"genres": ["전체"]}

    genreList = ["전체"] + sorted(dfAll["genre"].unique().tolist())
    return {"genres": genreList}

@app.get("/statistic/kpi")
def kpi(genre: str = Query("전체")):
    dfAll = loadDf()

    if len(dfAll) == 0:
        return {
            "count": 0,
            "avg": 0.0,
            "deadlineCount": 0
        }

    df = genreFilter(dfAll, genre)

    today = pd.Timestamp(datetime.today())
    deadline = df[
        (df["playEndDate"] >= today) &
        (df["playEndDate"] <= today + pd.Timedelta(days=7))
    ]

    return {
        "count": len(df),
        "avg": round(df["bookingPercent"].mean(), 1) if len(df) else 0.0,
        "deadlineCount": len(deadline)
    }

# -----------------------------
# 3) 실시간 통계 API 호출
# -----------------------------
def get_statistic(id: str, placeCode: str):
    url = f"https://tickets.interpark.com/contents/api/statistics/booking/{id}?placeCode={placeCode}"
    res = get(url)

    if res.status_code == 200:
        return json.loads(res.text).get("ageGender", {})
    return {}

# -----------------------------
# 4) 실시간 top10 조회
# -----------------------------
@app.get("/statistic/realtime-top10")
def realtime_top10(genre: str = Query(...)):
    key = f'@"/ranking","?period=D&page=1&pageSize=50&rankingTypes={genre}",'
    url = f"https://tickets.interpark.com/contents/ranking?genre={genre}"
    res = get(url)

    if res.status_code != 200:
        return {"error": "접속 실패"}

    soup = bs(res.text, "html.parser")
    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    if not script_tag:
        return {"error": "데이터를 찾을 수 없습니다."}

    json_data = json.loads(script_tag.string)
    tickets = (
        json_data.get("props", {})
        .get("pageProps", {})
        .get("fallback", {})
        .get(key, [])
    )

    top_10 = tickets[:10]
    results = []

    for v in top_10:
        statistic = get_statistic(v["goodsCode"], v["placeCode"])

        data = {
            "id": v["goodsCode"],
            "title": v["goodsName"],
            "placeName": v["placeName"],
            "playStartDate": v["playStartDate"],
            "playEndDate": v["playEndDate"],
            "bookingPercent": float(v["bookingPercent"]) if v["bookingPercent"] else 0,
            "genre": genre,
            "age10Rate": statistic.get("age10Rate", 0),
            "age20Rate": statistic.get("age20Rate", 0),
            "age30Rate": statistic.get("age30Rate", 0),
            "age40Rate": statistic.get("age40Rate", 0),
            "age50Rate": statistic.get("age50Rate", 0),
            "maleRate": statistic.get("maleRate", 0),
            "femaleRate": statistic.get("femaleRate", 0),
        }
        results.append(data)

    valid_booking = [
        float(t["bookingPercent"]) for t in tickets
        if t.get("bookingPercent")
    ]
    avg_booking = round(sum(valid_booking) / len(valid_booking), 1) if valid_booking else 0

    return {
        "summary": {
            "totalCount": len(tickets),
            "avgBooking": avg_booking,
        },
        "top10": results
    }