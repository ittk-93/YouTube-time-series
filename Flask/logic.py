from youtube_tools import MyYouTubeAPI

API_KEY = 'AIzaSyAzwO6lyH3vVTEEwDUQpzYKYJ7O13x3W84'
myt = MyYouTubeAPI(API_KEY)

def get_video_id(url):
    return url.split('=')[-1].split('&')[0]

def get_channel_id(myt, video_id):
    func = lambda response: [item['snippet']['channelId'] for item in response['items']]
    results = myt.deal_videos([video_id], func, True, 'snippet')
    return results[0]

def get_playlist_id_of_uploads(myt, channel_id):
    return 'UU' + channel_id[2:]

def get_video_ids(myt, playlist_id):
    func = lambda response: [item['snippet']['resourceId']['videoId'] for item in response['items']]
    results = myt.deal_playlist(playlist_id, func, True, 'snippet')
    return results

def get_iframe(video_id):
    return f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

def get_sides(index, video_ids):
    video_count = len(video_ids)
    sides = {}
    if index != 0: sides['next'] = get_iframe(video_ids[index-1])
    sides['selected'] = get_iframe(video_ids[index])
    if index != video_count: sides['pre'] = get_iframe(video_ids[index+1])
    return sides

def get_dic(url):
    video_id = get_video_id(url)
    channel_id = get_channel_id(myt, video_id)
    playlist_id = get_playlist_id_of_uploads(myt, channel_id)
    video_ids = get_video_ids(myt, playlist_id)
    index = video_ids.index(video_id)
    sides = get_sides(index, video_ids)
    return sides