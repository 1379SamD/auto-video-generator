import requests

url = "http://127.0.0.1:5000/synthesize"
payload = {
    "text":         "えっ！？チョコレートって、昔は飲み物だったの！？"
        "時は紀元前！メキシコのオルメカ文明では…カカオをすり潰して、水と混ぜてゴクッ！"
        "さらにアステカでは“ショコラトル”、つまり“苦い水”と呼ばれてて…なんと唐辛子まで入ってたんだよ！"
        "その後スペインに伝わると、砂糖やシナモンが加わって…甘〜いホットチョコとして大人気に！"
        "でもね、今の“固形チョコレート”が生まれたのは…実は19世紀！意外と最近なんだよ！"
        "つまりチョコレートは、もともと“飲み物”だったってこと！…知ってた？知らなかった？コメントで教えて！",
    "speaker": 2
}

response = requests.post(url, json=payload)

# 成功時に音声ファイル保存
if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("✔ 音声ファイル 'output.wav' を保存しました。")
else:
    print("❌ リクエストに失敗しました:", response.text)
