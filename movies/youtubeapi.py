from googleapiclient.discovery import build


def search_videos(movie_name):
    api_key = "AIzaSyA_QCq9X2KzzvYMIHkEWu5I4iCPQECpnGE"

    youtube = build('youtube', "v3", developerKey=api_key)
    request = youtube.search().list(part="snippet", q=movie_name+"trailer",
                                    type="videos", maxResults="1")
    response = request.execute()

    return response["items"][0]["id"]["videoId"]
