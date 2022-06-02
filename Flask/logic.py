from yt_dlp import YoutubeDL
import requests
import re
from bs4 import BeautifulSoup as bs

def get_video_id(url):
    return url.split('=')[-1].split('&')[0]

def get_channel_id(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        try:
            meta = ydl.extract_info(url, download=False)
        except:
            print("\nerror")
            exit(1)
    return meta['channel_id']

def get_playlist_id_of_uploads(channel_id):
    return 'UU' + channel_id[2:]

def get_iframe(video_id):
    return f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

def get_playlist_info(video_id, playlist_id):
    #ua = 'ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    #headers = {'User-Agent': ua}
    url = f'https://www.youtube.com/watch?v={video_id}&list={playlist_id}'
    res = requests.get(url)
    soup = bs(res.content,'html.parser')
    index = int(re.search(r'currentIndex":(\d*)',str(soup)).group(1))
    video_count = int(re.search(r'totalVideosText":{"runs":\[{"text":"(\d*)', str(soup)).group(1))
    print(index, video_count)
    return index, video_count

# あとは指定した動画のインデックスさえ特定できれば...
def get_sides(playlist_id, index):
    url = f'https://www.youtube.com/playlist?list={playlist_id}'
    # 範囲は0及びアイテム数を超えた場合無視
    ydl_opts = {'playlist_items': f'{index}-{index+2}'}
    with YoutubeDL(ydl_opts) as ydl:
        try:
            meta = ydl.extract_info(url, download=False)
        except:
            print("\nerror")
            exit(1)
    video_ids_sides = [items['id'] for items in meta['entries']]
    return video_ids_sides

def get_dic(url):
    video_id = get_video_id(url)
    channel_id = get_channel_id(video_id)
    playlist_id = get_playlist_id_of_uploads(channel_id)
    index, video_count = get_playlist_info(video_id, playlist_id)
    sides = get_sides(playlist_id, index)
    dic = {}

    if index == 0:
        dic['selected'] = get_iframe(sides[0])
        dic['next'] = get_iframe(sides[1])
    elif 0 < index < video_count:
        dic['next'] = get_iframe(sides[0])
        dic['selected'] = get_iframe(sides[1])
        dic['pre'] = get_iframe(sides[2])
    elif index == video_count:
        dic['selected'] = get_iframe(sides[0])
        dic['pre'] = get_iframe(sides[1])

    return dic