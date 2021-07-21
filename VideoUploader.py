import os

import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

from Secrets import get_youtube_credentials


def upload(filename, video_title):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    credentials = get_youtube_credentials()

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": "Description of uploaded video.",
                "title": video_title
            },
            "status": {
            "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(filename)
    )
    return request.execute()
