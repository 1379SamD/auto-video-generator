from flask import send_file
import requests, tempfile, os, threading

def generate_audio(text, speaker_id):
    
    # VOICEBOXのURLを定義
    VOICEVOX_ENGINE_URL = "http://localhost:50021"
      # 1. audio_queryを取得
    query_resp = requests.post(
        f"{VOICEVOX_ENGINE_URL}/audio_query",
        params={"text": text, "speaker": speaker_id}
    )
    if query_resp.status_code != 200:
        return f"audio_query failed: {query_resp.text}", 500  # エラーメッセージを返す

    query = query_resp.json()

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

    # 一時ファイルに音声データを保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(synthesis_resp.content)  # 音声データを書き込む
        tmp_file_path = tmp_file.name  # 一時ファイルのパスを取得
        
        # # ファイル削除用のスレッド
        # def delete_file_later():
        #     try:
        #         # しばらく待機してファイルを削除
        #         import time
        #         time.sleep(5)  # 5秒程度待機（ダウンロード完了を待つ）
        #         os.remove(tmp_file_path)  # ファイル削除
        #         print(f"Deleted file: {tmp_file_path}")
        #     except Exception as e:
        #         print(f"ファイル削除エラー: {e}")

        # # ファイルを返す
        # response = send_file(
        #     tmp_file_path,
        #     mimetype="audio/wav",
        #     as_attachment=True,
        #     download_name="output.wav"
        # )

        # # ファイル削除スレッドを起動
        # threading.Thread(target=delete_file_later).start()

        return tmp_file_path
