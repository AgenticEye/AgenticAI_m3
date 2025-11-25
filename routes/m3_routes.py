# routes/m3_routes.py
from fastapi import APIRouter
from pipelines.youtube import fetch_youtube_comments
from analysis import aggregate_signals
from m3_ideas import generate_content_ideas
import asyncio

router = APIRouter(prefix="/m3", tags=["M3 - Content Ideas"])

@router.get("/generate")
async def generate_ideas(url: str, limit: int = 400):
    # Step 1: Fetch YouTube comments
    comments_data = await asyncio.to_thread(fetch_youtube_comments, url, limit)
    
    # Step 2: Run M2 analysis
    analysis = aggregate_signals({"youtube": comments_data})
    
    # Step 3: Generate M3 ideas
    ideas = generate_content_ideas(analysis)
    
    return {
        "status": "M3 Complete",
        "input": url,
        "analysis_summary": {
            "trend_score": analysis["summary"]["trend_probability"],
            "top_topics": [t["topic"] for t in analysis["nlp"].get("topics", [])[:5]],
            "sentiment": analysis["nlp"]["sentiment"]
        },
        "best_format": ideas.get("recommended_format", "youtube"),
        "ideas": ideas
    }