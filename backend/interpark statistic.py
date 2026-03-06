from fastapi import FastAPI, Query
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from db import findAll

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

    # -----------------------------
    # 2) 타입 정리 (DB가 VARCHAR여도 안전하게)
    # -----------------------------
    dfAll["playStartDate"] = pd.to_datetime(dfAll["playStartDate"], errors="coerce")
    dfAll["playEndDate"] = pd.to_datetime(dfAll["playEndDate"], errors="coerce")

    # bookingPercent가 "72%" 형태면 숫자로
    dfAll["bookingPercent"] = (
        dfAll["bookingPercent"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )
    dfAll["bookingPercent"] = pd.to_numeric(dfAll["bookingPercent"], errors="coerce")

    rate_cols = ["age10Rate","age20Rate","age30Rate","age40Rate","age50Rate","maleRate","femaleRate"]
    for c in rate_cols:
        dfAll[c] = pd.to_numeric(dfAll[c], errors="coerce")

    # 날짜/숫자 핵심 컬럼 결측치 제거(차트 안정성)
    dfAll = dfAll.dropna(subset=["genre", "title", "playEndDate", "bookingPercent"])

    today = pd.Timestamp(datetime.today())
    dfAll["remainDays"] = (dfAll["playEndDate"] - today).dt.days
   
    return dfAll

# -----------------------------
# 3) 장르 선택
# -----------------------------
def genreFliter(dfAll: pd.DataFrame, genre: str)
    df = dfAll.copy()
    if genre != "전체":
        df =df[df["genre_"] == genre].copy()
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
    dfAll = loadDf
    if len(dfAll) ==0:
        return {"genres": ["전체"]}
    genreList = ["전체"] + sorted(dfAll["genre"].unique().tolist())
    return {"genres":genreList }

@app.get("/statistic/kpi")
def kpi(genre: str = Query("전체")):
    dfAll = loadDf
    if genre != "전체":
        df = dfAll[dfAll["genre"] == genre]
    else:
        df = dfAll
    today = pd.Timestamp(datetime.today())
    deadlin = df[
        (df["playEndDate"] >= today) &
        (df["playEndDate"] <= today + pd.Timedelta(day=7))
    ]
    return {
        "count" : len(df),
        "avg": round(df["bookingPercent"].mean(), 1),
        "deadlinCount": len(deadlin)
    }
