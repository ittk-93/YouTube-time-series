from flask import Flask, redirect, render_template, request
from yt_dlp import YoutubeDL
import requests

def get_valid_url(url):
    res = requests.get(url)
    return res.url

def get_video_id(valid_url):
    return valid_url.split('=')[1].split('&')[0]

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

def get_playlist_url(video_id):
    channel_id = get_channel_id(video_id)
    playlist_id = get_playlist_id_of_uploads(channel_id)
    url = f'https://www.youtube.com/watch?v={video_id}&list={playlist_id}'
    return url

app = Flask(__name__)

# 前後1本ずつで固定ではなく可変にしたい
#@app.route('https://www.youtube.com/watch?v=55larYBfmRU')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/redirect_to_yt', methods=['POST'])
def redirect_to_youtube():
    url = request.form.get('url')
    if url == '':
        return redirect('/error')
    valid_url = get_valid_url(url)
    if not valid_url.startswith('https://www.youtube.com/watch?v='):
        return redirect('/error')
    video_id = get_video_id(valid_url)
    return redirect(get_playlist_url(video_id))

if __name__ == 'main':
    app.run(debug=True)