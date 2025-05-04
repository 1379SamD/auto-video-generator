import whisper
from moviepy.editor import *
import os
import subprocess
import time
from pathlib import Path
from moviepy.config import change_settings

def generate_subtitled_video(audio_path, output_video_path="output_video.mp4"):
    # Whisperモデル読み込み
    try:
        # os.environ["FFMPEG_BINARY"] = r"C:\ffmpeg\bin\ffmpeg.exe"  # 自分のFFmpegのパスを指定
        os.environ["PATH"] = r"C:\ffmpeg\bin;" + os.environ["PATH"]
        model = whisper.load_model("large")
        print("!!!!!!!!!!!!!!", audio_path)
        # audio_path = Path(audio_path)
        print("存在する？", audio_path)
        subprocess.run(["C:/ffmpeg/bin/ffmpeg.exe", "-version"])
        print("📥 音声から字幕を抽出中...")
        audio_path = audio_path.replace("\\", "/")
        print("???????????", audio_path)
        print(os.path.exists(audio_path))

        timeout = 10  # 待機時間を10秒に設定
        start_time = time.time()

        while not os.path.exists(audio_path):
            if time.time() - start_time > timeout:
                print(f"タイムアウトしました。{audio_path}が見つかりません。")
                break
            time.sleep(0.1)  # 少し待つ

    except Exception as e:
        print(f"エラー発生: {e}")

    result = model.transcribe(str(audio_path))
    print(result)
    segments = result['segments']

    print("🎬 動画を生成中...")

    # ImageMagick のパス（magick.exe のフルパス）
    change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

    # 音声ファイル
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # 背景（黒背景 1280x720）
    video = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=duration)
    video = video.set_audio(audio)

    # 字幕を作成
    subtitles = []
    for seg in segments:
        txt = TextClip(seg["text"], fontsize=40, color="white", bg_color="black", size=(1200, None), font="C:/Windows/Fonts/msgothic.ttc", method="caption")
        txt = txt.set_start(seg["start"]).set_end(seg["end"])
        txt = txt.set_position(("center", "center"))
        subtitles.append(txt)

    # 字幕と背景を合成
    final_video = CompositeVideoClip([video] + subtitles)

    # 書き出し
    final_video.write_videofile(output_video_path, fps=24)
    print(f"✅ 完了！動画を生成しました: {output_video_path}")
