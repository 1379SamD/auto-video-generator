from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # 入力フォームがあるHTML

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text')  # 入力されたテキストを取得
    # テキストに基づいた処理（TTS、動画生成など）を呼び出し
    return '動画生成完了！'  # 仮の返り値

if __name__ == '__main__':
    app.run(debug=True)