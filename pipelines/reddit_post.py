import httpx
from utils.headers import get_headers

def extract_comments(comment_list, out):
    for c in comment_list:
        if c["kind"] == "t1":
            data = c["data"]
            out.append({
                "author": data.get("author"),
                "text": data.get("body"),
                "score": data.get("score"),
            })
                        # Recursive parse replies
            if data.get("replies") and isinstance(data["replies"], dict):
                replies = data["replies"]["data"]["children"]
                extract_comments(replies, out)


def get_reddit_post(url: str):
    try:
        if not url.endswith(".json"):
            url = url.split("?")[0].rstrip("/") + "/.json"

        response = httpx.get(url, headers=get_headers(), timeout=30)
        data = response.json()

        post = data[0]["data"]["children"][0]["data"]

        # Get main comment tree
        comment_tree = data[1]["data"]["children"]

        all_comments = []
        extract_comments(comment_tree, all_comments)

        return {
            "url": url,
            "title": post.get("title"),
            "author": post.get("author"),
            "content": post.get("selftext"),
            "comments_count": len(all_comments),
            "comments": all_comments
        }

    except Exception as e:
        return {"error": str(e)}
