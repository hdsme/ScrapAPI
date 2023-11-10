from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import httpx
import os
import uvicorn

app = FastAPI(title='ScrapAPI')
load_dotenv()
SCRAPY_HOST = 'http://localhost:9080'


@app.get("/api/spider")
def crawl(request):
    try:
        with httpx.AsyncClient() as client:
            base_url = os.getenv('SCRAPY_HOST', SCRAPY_HOST)
            headers = request.headers
            params = request.query_params
            response = client.get(base_url, headers, params)
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail="External API Error")
    return response.json()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
