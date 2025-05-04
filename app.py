from flask import Flask, request, send_file, jsonify
import requests, tempfile, os, subprocess, psutil, threading
from audio_generator import generate_audio
from video_generator import generate_subtitled_video

# FLaskサーバを起動
app = Flask(__name__)

# VOICEBOXのURLを定義
VOICEVOX_ENGINE_URL = "http://localhost:50021"

# VOICEVOXエンジンが起動しているかどうか確認し、起動していなければ起動
def is_voicvox_running():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'run.exe' in proc.info['name']:  # VOICEVOX エンジンが実行中かチェック
            return True
    return False

# VOICEVOXのエンジンを自動的に起動(起動していない場合)
if not is_voicvox_running():
    subprocess.Popen(["C:/Users/isamu/AppData/Local/Programs/VOICEVOX/vv-engine/run.exe"])

# http://localhost:5000/synthesizeにPOSTで送信した時に実行
@app.route("/synthesize", methods=["POST"])
def synthesize():
    request.charset = 'utf-8'
    try:
        text = request.json.get("text", "こんにちは、これはテスト音声です。")
        speaker_id = request.json.get("speaker", 2)

        audio_response = generate_audio(text, speaker_id)
        video_path = generate_subtitled_video(audio_response)

        return jsonify({"video_path": video_path})

    except Exception as e:
        print("エラー:", e)
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True)