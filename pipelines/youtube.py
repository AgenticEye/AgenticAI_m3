from youtube_comment_downloader import YoutubeCommentDownloader

def get_youtube_comments(video_url: str, limit: int = 500):
    downloader = YoutubeCommentDownloader()
    comments = []
    for comment in downloader.get_comments_from_url(video_url, sort_by=0):
        comments.append({
            "text": comment['text'],
            "author": comment['author'],
            "likes": comment['votes'],
            "time": comment['time']
        })
        if len(comments) >= limit:
            break
    return comments