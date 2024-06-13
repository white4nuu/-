from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

API_KEY = 'kzTCAvwcHnQy6ROEtwBwKCF2Kei61DUeLQe9OqqnzrE0FZiqIfIR6gvMX9UOwDtMMvaSGfZ3gDGc8lwBUabyIQ=='  # 데이터.go.kr에서 발급받은 API 키를 입력하세요

templates = Jinja2Templates(directory="templates")

AREA_CODES = {
    "서울": 1,
    "부산": 6,
    "대구": 4,
    "인천": 2,
    "광주": 5,
    "대전": 3,
    "울산": 7,
    "세종": 8,
    "경기": 31,
    "강원": 32,
    "충북": 33,
    "충남": 34,
    "경북": 35,
    "경남": 36,
    "전북": 37,
    "전남": 38,
    "제주": 39
}


COURSE_CODE = {
    "가족코스": "C0112",
    "나홀로코스": "C0113",
    "힐링코스": "C0114",
    "도보코스": "C0115",
    "캠핑코스": "C0116",
    "맛코스": "C0117"
}

def get_area_name_from_code(area_code: int) -> str:
    for name, code in AREA_CODES.items():
        if code == area_code:
            return name
    return ""

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/tourism-info")
async def get_tourism_info(
    areaCode: int = Query(..., description="지역코드"),
    contentTypeId: int = Query(None, description="관광타입 ID"),
    cat1: str = Query(None, description="대분류코드"),
    cat2: str = Query(None, description="중분류코드"),
    cat3: str = Query(None, description="소분류코드")
):
    numeric_area_code = get_area_name_from_code(areaCode)
    if not numeric_area_code:
        return JSONResponse(status_code=400, content={"error": "올바르지 않은 지역 이름입니다."})
    url = (
        f"http://apis.data.go.kr/B551011/KorService1/areaBasedList1"
        f"?serviceKey={API_KEY}&pageNo=1&numOfRows=10&MobileApp=AppTest"
        f"&MobileOS=ETC&arrange=A&_type=json&listYN=Y"
        f"&areaCode={areaCode}"
        f"&contentTypeId=25"
        f"&cat1=C01"
    )
    
    if cat2:
        url += f"&cat2={cat2}"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or 'response' not in data:
        return JSONResponse(status_code=500, content={"error": "Failed to fetch data"})

    return data

"""
def get_area_code_from_name(area_name: str) -> int:
    if area_name in AREA_CODES:
        return AREA_CODES[area_name]
    else:
        raise HTTPException(status_code=400, detail="Invalid area name")
"""
@app.get("/tourism-info")
async def get_tourism_info(
    areaCode: str = Query(..., description="지역코드"),
    contentTypeId: int = Query(None, description="관광타입 ID"),
    cat1: str = Query(None, description="대분류코드"),
    cat2: str = Query(None, description="중분류코드"),
    cat3: str = Query(None, description="소분류코드")
):
    try:
        numeric_area_code = int(areaCode)
    except ValueError:
        numeric_area_code = get_area_code_from_name(areaCode)
    
    
    if cat2:
        url += f"&cat2={cat2}"

    response = requests.get(url)
    data = response.json()
    # Here you would proceed with using numeric_area_code for further logic
    
    return data


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
