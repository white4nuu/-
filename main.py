from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import requests

app = FastAPI()

app.mount("/templates", StaticFiles(directory="templates"), name="templates")

KEY = "x6o2i4Y68c81u2i6el5F37V2xc6cpQbo58EWWgZi"
URL = "https://apis.openapi.sk.com/transit/routes"
HEADERS = {"appKey": KEY}

@app.get("/")
def root():
    return FileResponse("templates/index.html")

@app.get("/search")
def search_transit_routes(startX: float, startY: float, endX: float, endY: float, reqDttm: Optional[str] = None, locale: str = "ko"):
    """
    대중교통 경로를 조회합니다.
    """
    params = {
        "startX": startX,
        "startY": startY,
        "endX": endX,
        "endY": endY,
        "reqDttm": reqDttm,
        "locale": locale
    }

    response = requests.get(URL, headers=HEADERS, params=params).text

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="API 요청에 실패했습니다.")
    
    data = response.json()


    if "itineraries" not in data or not data["itineraries"]:
        raise HTTPException(status_code=404, detail="경로 데이터를 찾을 수 없습니다.")
    
    itinerary = data["itineraries"][0]

    return {
        "totalTime": itinerary["totalTime"],
        "transferCount": itinerary["transferCount"],
        "totalWalkDistance": itinerary["totalWalkDistance"],
        "totalDistance": itinerary["totalDistance"],
        "totalFare": itinerary["fare"]["regular"]["totalFare"],
        "legs": itinerary["legs"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
