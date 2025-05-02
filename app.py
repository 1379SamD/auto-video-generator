from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "自動生成動画ツールへようこそ！"

if __name__ == '__main__':
    app.run(debug=True)
