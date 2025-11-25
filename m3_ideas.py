# m3_ideas.py — MODIFIED FOR AI/ML API (aimlapi.com) with DeepSeek
import json
import re
import requests
import time
from config import CONFIG
from datetime import datetime

# Rate limiting (AI/ML API free tier: 50 RPM)
last_call = 0
DELAY = 1.2

def call_aimlapi_deepseek(prompt: str) -> str:
    global last_call
    while time.time() - last_call < DELAY:
        time.sleep(0.1)
    
    if not CONFIG.AIMLAPI_API_KEY:
        raise ValueError("AI/ML API key missing in .env")

    url = "https://api.aimlapi.com/v1/chat/completions"  # AI/ML API endpoint
    headers = {
        "Authorization": f"Bearer {CONFIG.AIMLAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",  # DeepSeek via AI/ML API (free tier supported)
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        last_call = time.time()
        
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        elif r.status_code == 402:
            raise ValueError("Free tier quota exhausted — top up at https://aimlapi.com/app/billing")
        elif r.status_code == 429:
            time.sleep(10)
            return call_aimlapi_deepseek(prompt)  # Retry
        else:
            raise ValueError(f"AI/ML API error {r.status_code}: {r.text}")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Network error: {str(e)}")

def generate_m3(analysis: dict) -> dict:
    topics = [t["topic"] for t in analysis.get("topics", [])[:12]]
    questions = [q["text"][:140] for q in analysis.get("questions", [])[:10]]
    sentiment = analysis["sentiment"]["positive"]
    viral_score = analysis.get("viral_score", 80)

    prompt = f'''You are ViralEdge-M3 — advanced viral content engine.

Real data from video comments:
- Topics: {", ".join(topics)}
- Top questions: {" | ".join(questions)}
- Positive sentiment: {sentiment}%
- Viral score: {viral_score}/100

Return ONLY this exact JSON structure. No markdown, no extra text. Fill all fields with creative, data-driven ideas based on the topics/questions.

{{
  "viral_prediction_engine": {{
    "score": {viral_score},
    "category": "High",
    "reasons": ["High question intent", "Strong topic relevance", "Positive audience vibe"]
  }},
  "content_category_classifier": {{
    "best_format": "",
    "alternative_formats": ["YouTube Long-form", "Instagram Reel", "X Thread"],
    "reason": ""
  }},
  "viral_pattern_detection": {{
    "detected_patterns": [],
    "confidence": 0.92
  }},
  "ai_recommendations": {{
    "next_best_content": []
  }},
  "seo_keyword_generator": {{
    "primary_keywords": [],
    "secondary_keywords": [],
    "search_volume": {{}}
  }}
}}

Generate real titles, hooks, keywords, etc. from the data. START JSON NOW:'''

    raw = call_aimlapi_deepseek(prompt)
    
    # Extract JSON
    match = re.search(r"\{.*\}", raw.replace("\n", " ").replace("```", ""), re.DOTALL)
    if not match:
        raise ValueError(f"No valid JSON in response: {raw[:800]}")

    try:
        result = json.loads(match.group(0))
        result["generated_by"] = "DeepSeek via AI/ML API (Your Key)"
        return result
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parse error: {str(e)}. Raw: {raw[:800]}")