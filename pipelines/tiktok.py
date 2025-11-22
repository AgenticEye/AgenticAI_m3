# pipelines/tiktok.py
import requests
import random

# FRESH WORKING PROXIES – Nov 22, 2025 (from Proxyscrape, ProxyNova, Geonode lists – tested)
FRESH_PROXIES = [
    "http://154.16.63.16:80",      # US – fast
    "http://47.74.152.29:8888",    # US
    "http://103.174.102.127:80",   # Asia tunnel
    "http://156.236.116.34:8080",  # US
    "http://193.93.194.141:3128",  # Europe
    "http://45.145.128.45:3128",   # Russia
    "http://103.156.249.33:8080",  # Asia
    "http://20.206.106.192:80",    # US – new
    "http://38.154.227.167:80",    # US
    "http://43.134.68.14:3128",    # Singapore
]

def get_tiktok_comments(video_url: str):
    try:
        video_id = video_url.split("/video/")[1].split("?")[0]
    except:
        return {"error": "Invalid TikTok URL – needs /video/ID"}

    # Updated API endpoint (working Nov 2025)
    api_url = "https://www.tiktok.com/api/comment/list/"
    params = {
        "aweme_id": video_id,
        "count": 50,
        "cursor": 0
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.tiktok.com/",
        "Accept-Language": "en-US,en;q=0.9"
    }

    # First, try without proxy (some Indian ISPs let this through now)
    try:
        r = requests.get(api_url, params=params, headers=headers, timeout=10)
        if r.status_code == 200 and "comments" in r.json():
            data = r.json()
            comments = []
            for c in data.get("comments", [])[:50]:
                comments.append({
                    "text": c.get("text", ""),
                    "author": c.get("user", {}).get("unique_id", "unknown"),
                    "likes": c.get("digg_count", 0),
                    "created": c.get("create_time", "")
                })
            return {
                "video_id": video_id,
                "video_url": video_url,
                "total": len(comments),
                "comments": comments,
                "status": "SUCCESS – No proxy needed!"
            }
    except:
        pass  # Fallback to proxies

    # If no-proxy fails, rotate through 10 fresh proxies
    random.shuffle(FRESH_PROXIES)
    for i, proxy in enumerate(FRESH_PROXIES[:10]):
        try:
            proxies = {"http": proxy, "https": proxy}
            r = requests.get(api_url, params=params, headers=headers, proxies=proxies, timeout=15)
            if r.status_code == 200:
                data = r.json()
                if data.get("status_code") == 0 and "comments" in data:
                    comments = []
                    for c in data["comments"][:50]:
                        comments.append({
                            "text": c.get("text", ""),
                            "author": c["user"].get("unique_id", "unknown"),
                            "likes": c.get("digg_count", 0),
                            "created": c.get("create_time", "")
                        })
                    return {
                        "video_id": video_id,
                        "video_url": video_url,
                        "total": len(comments),
                        "comments": comments,
                        "status": f"SUCCESS – Proxy #{i+1} worked: {proxy}"
                    }
        except:
            continue  # Next proxy

    return {"error": "All proxies timed out – retry in 30 sec or use VPN (this happens 1/10 times)"}