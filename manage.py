from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import httpx
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi_directory_routing import DirectoryRouter


app = FastAPI(title='ScrapAPI')
load_dotenv()
SCRAPY_HOST = 'http://localhost:9080'
allow_origins = [
    "http://localhost:80",
    "localhost:80",
    "http://0.0.0.0:80",
    "0.0.0.0:9080",
    "http://localhost:9080"
] + os.getenv('', [])
allow_methods = os.getenv('', ['*'])
allow_headers = os.getenv('', ['*'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount("/", StaticFiles(directory="build", html=True), name="build")
# Router based on directory
api_routers = DirectoryRouter(base_directory='routers')
app.include_router(prefix="/api", router=api_routers)


@app.get("/")
async def index():
    return RedirectResponse(url="/index.html")


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
