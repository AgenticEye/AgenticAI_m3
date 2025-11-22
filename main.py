from fastapi import FastAPI
from pipelines.youtube import get_youtube_comments
from pipelines.tiktok import get_tiktok_comments
from pipelines.reddit_post import get_reddit_post

app = FastAPI(title="ViralEdge Backend", version="1.0")


@app.get("/")
async def root():
    return {"message": "ViralEdge Engine Live"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/youtube-comments")
async def youtube_comments(url: str):
    comments = get_youtube_comments(url)
    return {"video_url": url, "comments": comments[:50]}


@app.get("/tiktok-comments")
async def tiktok_comments(url: str):
    comments = await get_tiktok_comments(url)
    return {"video_url": url, "comments": comments[:50]}


@app.get("/reddit-post")
async def reddit_post(url: str):
    return get_reddit_post(url)
