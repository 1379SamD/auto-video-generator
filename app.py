from flask import Flask, request, send_file
import requests
import tempfile
import os
import subprocess

app = Flask(__name__)

# VOICEVOXのエンジンを自動的に起動
subprocess.Popen(["C:/Users/isamu/AppData/Local/Programs/VOICEVOX/vv-engine/run.exe"])

VOICEVOX_ENGINE_URL = "http://localhost:50021"

@app.route("/synthesize", methods=["POST"])
def synthesize():
    request.charset = 'utf-8'
    data = request.get_json()  # リクエストデータをそのまま確認
    print(f"Received data: {data}")
    text = request.json.get("text", "こんにちは、これはテスト音声です。")
    speaker_id = request.json.get("speaker", 2)
    print(f"Received text: {text}")
    
    # 1. audio_queryを取得
    query_resp = requests.post(
        f"{VOICEVOX_ENGINE_URL}/audio_query",
        params={"text": text, "speaker": speaker_id}
    )
    if query_resp.status_code != 200:
        return f"audio_query failed: {query_resp.text}", 500  # エラーメッセージを返す

    query = query_resp.json()
    print("audio_query response:", query)  # レスポンス内容をログに出力

    # 2. synthesisで音声合成
    synthesis_resp = requests.post(
        f"{VOICEVOX_ENGINE_URL}/synthesis",
        params={"speaker": speaker_id},
        json=query
    )
    if synthesis_resp.status_code != 200:
        return f"synthesis failed: {synthesis_resp.text}", 500  # エラーメッセージを返す

    # 音声データが存在するか確認
    if not synthesis_resp.content:
        return "No audio data returned", 500  # 音声データが空ならエラーを返す

    print("synthesis response:", synthesis_resp.content[:100])  # 最初の100バイトを表示して確認

    # 3. 一時ファイルに保存して返す
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(synthesis_resp.content)
        tmp_path = tmp.name
        print(f"!!!!!!!!!!!! {tmp_path}")

    print(f"Audio query response: {query}")
    print(f"Synthesis response content length: {len(synthesis_resp.content)}")
    return send_file(tmp_path, mimetype="audio/wav", as_attachment=True, download_name="output.wav")

if __name__ == "__main__":
    app.run(debug=True)
