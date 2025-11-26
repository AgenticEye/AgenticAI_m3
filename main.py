# main.py — FINAL FIXED VERSION (NO MORE ERRORS)
from fastapi import FastAPI, Query, HTTPException
import asyncio
from datetime import datetime
from pipelines.youtube import fetch_youtube_comments
from utils.nlp_utils import analyze_comments
from m3_ideas import generate_m3
import os
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="ViralEdge M3 Engine",
    description="Professional AI-powered viral content generator",
    version="3.0"
)


# Add CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows Vercel, localhost, etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Render port binding (fixes the error)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use Render's $PORT or fallback to 8000
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)  # Bind to 0.0.0.0 for Render
@app.get("/")
async def root():
    return {
        "engine": "ViralEdge-M3",
        "status": "LIVE",
        "model": "DeepSeek-V3",
        "endpoint": "/m3/analyze?url=https://youtube.com/watch?v=..."
    }

@app.get("/m3/analyze")
async def m3_analyze(url: str = Query(..., description="YouTube URL")):
    comments_data = await asyncio.to_thread(fetch_youtube_comments, url, limit=500)
    if "error" in comments_data:
        raise HTTPException(500, comments_data["error"])

    m2 = analyze_comments(comments_data["comments"], url)

    try:
        m3 = generate_m3(m2)  # ← 100% DeepSeek, no dummy
    except Exception as e:
        raise HTTPException(500, str(e))

    return {
        "engine": "ViralEdge-M3",
        "model_used": "DeepSeek-V3",
        "video_url": url,
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "m2_analysis": {
            "topics": m2["topics"],
            "questions": m2["questions"][:10],
            "sentiment": m2["sentiment"],
            "engagement": m2["engagement"],
            "trend_probability": m2["viral_score"]
        },
        "m3_generation": m3
    }

@app.get("/health")
async def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat() + "Z"}
