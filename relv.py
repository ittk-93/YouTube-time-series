from apiclient.discovery import build
import webbrowser

def getYT():
    API_KEY = 'AIzaSyAzwO6lyH3vVTEEwDUQpzYKYJ7O13x3W84'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=API_KEY
        )

    return youtube

def getChannelId(url):
    """From a url of channel, get channel Id.
    Args:
        url (str): str of url.

    Retruns:
        str: channelId
    """
    return url.split('/')[-1]

def getChannelItems(channelId):
    youtube = getYT()
    response = youtube.channels().list(
        part = 'snippet, statistics',
        id = channelId,
        maxResults = 1
        ).execute()
    print(response)
    return response['items'][0]

def getVideoId(url):
    videoId = url.split('watch?v=')[-1]
    if '&' in videoId:
        videoId = videoId.split('&')[0]
    return videoId

def getVideoItems(videoId):
    youtube = getYT()
    response = youtube.videos().list(
        part = "snippet, contentDetails, statistics, player, liveStreamingDetails",
        id = videoId,
        maxResults = 50
    ).execute()
    return response['items']

def getPlaylistIdOfUploadedVideos(channelId):
    """From a channelId, get playlistId of uploaded videos.
    Args:
        channelId (str): str of channelId.
        youtube (googleapiclient.discovery.Resource): resource of googleapiclient.discovery.

    Returns:
        str: playlistId of uploaded videos.
    """

    youtube = getYT()
    response = youtube.channels().list(
        part = 'contentDetails',
        id = channelId,
        maxResults = 1
        ).execute()

    contentDetails = response["items"][0]["contentDetails"]
    playlistIdOfUploadedVideos = contentDetails["relatedPlaylists"]["uploads"]

    return playlistIdOfUploadedVideos

def getVideoIdsFromPlaylist(plId, li, pagetoken=None):
    """From playlistId, get all videoIds in the playlist
    Args:
        plId (str): str of playlistId.
        li (list): list of videoIds. videoId will be appended in this.
            !!!ATTENTION!!! SET EMPTY LIST TO li, OR VIDEOS ID WILL BE APPENDED ORIGINAL LIST.
        pagetoken (str): pagetoken which shows which page to search.
        youtube (googleapiclient.discovery.Resource): resource of googleapiclient.discovery.

    Returns:
        list: list of videoIds.
    """

    youtube = getYT()
    response = youtube.playlistItems().list(
        part = 'snippet',
        playlistId = plId,
        maxResults = 50,
        pageToken = pagetoken
        ).execute()

    for i in range(len(response['items'])):
        snippet = response['items'][i]['snippet']
        v_id = snippet['resourceId']['videoId']
        li.append(v_id)

    try:
        nextPagetoken = response['nextPageToken']
        getVideoIdsFromPlaylist(plId, li, nextPagetoken)
    except:
        return li

    return li

def process():
    url = input('urlを入力してください')
    videoId = getVideoId(url)
    channelId = getVideoItems(videoId)[0]['snippet']['channelId']
    playlistId = getPlaylistIdOfUploadedVideos(channelId)
    videoIds = getVideoIdsFromPlaylist(playlistId, li=[])

    n = videoIds.index(getVideoId(url))
    attr = ','.join(videoIds[n-1:n+1+1])
    dict = getVideoItems(attr)
    for item in dict:
        str = item['player']['embedHtml']
        item['player']['embedHtml'] = str.replace('src="//www.', 'src="https://www.')

    iframes = []
    for item in dict:
        iframes.append(item['player']['embedHtml'])

    html = f'''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8" />
        <title>前後の動画が気になるあなたへ</title>
        <link rel="stylesheet" href="style.css" />
    </head>
    <body>
        <div class="whole">
        <div class="embed">
            {iframes[0]}
            <p>次の動画</p>
        </div>
        <div class="embed">
            {iframes[1]}
            <p>入力した動画</p>
        </div>
        <div class="embed">
            {iframes[2]}
            <p>前の動画</p>
        </div>
        </div>
    </body>
    </html>
    '''

    with open('test.html', 'w', encoding='utf-8') as f:
        f.writelines(html)

    webbrowser.open('C:/Users/YASUSHI/git-sample/cmd/relv/test.html')
