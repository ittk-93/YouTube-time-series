from flask import Flask, render_template
from logic import get_dic

app = Flask(__name__)

# 前後1本ずつで固定ではなく可変にしたい
@app.route('/<string:video_id>')
def hello(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    dic = get_dic(url)
    return render_template('test.html', dic=dic)

if __name__ == 'main':
    app.run(debug=True)