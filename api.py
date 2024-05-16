from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import asyncio
import uvicorn
import subprocess
from main import parallel_main, parallel_one_news_source, scrape_article_given_url, scrape_urls_one_category_given_news_source
from typing import Annotated

app = FastAPI()

security = HTTPBasic()

def authenticate(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    correct_username = "newsfetcher"
    correct_password = "s1i1n1a1"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post("/scrape/all")
async def scrape_all(credentials: Annotated[HTTPBasicCredentials, Depends(authenticate)]):
    try:
        await parallel_main()
        return {"message": "Scraping all sources completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape/source/{news_source}")
async def scrape_source(news_source: str, credentials: Annotated[HTTPBasicCredentials, Depends(authenticate)]):
    try:
        await parallel_one_news_source(news_source)
        return {"message": f"Scraping source {news_source} completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape/article")
async def scrape_article(news_source: str, article_url: str, credentials: Annotated[HTTPBasicCredentials, Depends(authenticate)]):
    try:
        await scrape_article_given_url(news_source, article_url)
        return {"message": "Scraping article completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape/category/{news_source}")
def scrape_category(news_source: str, credentials: Annotated[HTTPBasicCredentials, Depends(authenticate)]):
    try:
        scrape_urls_one_category_given_news_source(news_source)
        return {"message": f"Scraping one category for source {news_source} completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/run-tests")
def run_tests(credentials: Annotated[HTTPBasicCredentials, Depends(authenticate)]):
    try:
        result = subprocess.run(["pytest"], capture_output=True, text=True)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
