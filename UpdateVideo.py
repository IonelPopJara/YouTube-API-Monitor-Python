#pip install python-dateutil
#pip install google-auth
#pip install google-auth-oauthlib
#python -m pip install google-api-python-client
#pip install Pillow

import os
import re
import time
import pickle
import urllib.request
import json

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from CountDownTimer import GetCountdownTime
from dateutil import parser, tz

TIME_ZONE = "America/Los_Angeles"
END_OF_2020 = parser.parse("January 1, 2021 0:00 AM").replace(tzinfo=tz.gettz(TIME_ZONE))
TEST_DATE = parser.parse("October 19, 2020 5:16 PM").replace(tzinfo=tz.gettz(TIME_ZONE))
TITLE = "Until 2020 Ends"

API_KEY = os.environ.get("YT_API_KEY")
VIDEO_ID = "2aDkYXOte4w"

credentials = None
update_count = 0

def get_video_stats(video_id, api_key):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}'
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    res = json.loads(respData.decode('utf-8'))
    stats = res["items"][0]["statistics"]

    views = stats["viewCount"]
    comments = stats["commentCount"]
    likes = stats["likeCount"]
    dislikes = stats["dislikeCount"]

    data = [views,comments,likes,dislikes]

    return data


def update_thumbnail_and_title(youtube, video_id, file, title):
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(file)
    ).execute()

    stats = get_video_stats(video_id, API_KEY)

    youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "categoryId": 24,
                "title": f'{title} {TITLE} (Yes, this thumbnail updates itself)',
                "description": f'Bip Bup this was written by a python script.\n2020 ends in {title}.\nThis video has: {stats[0]} views, {stats[1]} comments, {stats[2]} likes, {stats[3]} dislikes.\nTimes this description has been updated: {update_count}.'
            }
        }
    ).execute()

def create_thumbnail(timeleft, youtubebuild):
    fillColor = (255,255,255) #White
    strokeColor =(147,26,37) #Some shade of Red

    img = Image.open("thumbnail_template.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font="Rowdies-Bold.ttf", size=78)

    draw.text((50,450), timeleft, fill=fillColor, font=font, stroke_width=3, stroke_fill=strokeColor)

    img.save("Thumbnail.png")

    print(os.path.exists("Thumbnail.png"))
    
    update_thumbnail_and_title(youtubebuild, VIDEO_ID, "Thumbnail.png", timeleft)

#Gets credentials if they exists, if not, creats new credentials

if os.path.exists("token.pickle"):
    print("Loading Credentials From File...")
    with open("token.pickle", "rb") as token:
        credentials = pickle.load(token)

if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refresing Acces Token...")
        credentials.refresh(Request())
    else:
        print("Fetching New Tokens...")
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secrets.json",
            scopes=["https://www.googleapis.com/auth/youtube"]
        )

        flow.run_local_server(
            port=8080, prompt="consent", authorization_prompt_message=""
        )

        credentials = flow.credentials

        #Save the credentials for the next run
        with open("token.pickle", "wb") as f:
            print("Saving Credentials for Future Use...")
            pickle.dump(credentials, f)

youtube = build('youtube', 'v3', credentials=credentials)

while True:
    time_obtained = GetCountdownTime(END_OF_2020, TIME_ZONE)

    if(time_obtained == None):
        break

    update_count += 1

    create_thumbnail(time_obtained, youtube)

    time.sleep(900)

# while True:
#     time_obtained = GetCountdownTime(END_OF_2020, TIME_ZONE)

#     print(time_obtained)

#     if(time_obtained == None):
#         break
#     time.sleep(1)