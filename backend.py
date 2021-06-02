
import soundfile as sf
import pyworld as pw
from pydub import AudioSegment

import os
import io
import numpy as np

from base64 import b64encode
from flask import Flask, jsonify, request,  make_response
from google.cloud import speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./My First Project-bbba15774894.json"

app = Flask(__name__, static_url_path="")


@app.route("/stt", methods=["POST"])
def returnWavAndTimestamp():
    print("hello, stt")

    buffer = io.BytesIO()
    audioSegment = AudioSegment.from_file(request.files["audio"])
    audioSegment = audioSegment.set_channels(1)
    audioSegment.export(buffer, format="wav")
    duraion = audioSegment.duration_seconds

    buffer.seek(0)
    x, fs = sf.read(buffer)
    f0, t = pw.harvest(x, fs)

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=buffer.getvalue())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=fs,
        language_code="zh-TW",
        enable_word_time_offsets=True,
    )

    response = client.recognize(config=config, audio=audio)
    wordInfo = []
    wordInfoFromStt = []
    startPosition = []

    for result in response.results :
        alternative = result.alternatives[0]
        print("Transcript: {}".format(alternative.transcript))

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            start_index = int( start_time.total_seconds() / duraion * len(f0) )
            end_index = int( end_time.total_seconds() / duraion * len(f0) )

            wordInfoFromStt.append({
                'word': word, 'start_index': start_index, 'end_index': end_index,
            })
            '''print(
                f"Word: {word}, start: {start_time.total_seconds()}, end: {end_time.total_seconds()}, f0: {wordF0}, s: {start_buffer}, e: {end_buffer}"
            )'''

    f0_ave = np.average( f0[0: len(f0)] )
    f0_vel = np.gradient(f0)
    for base in range(0, len(f0_vel) - 10) :
        if f0_vel[base] <= 1 or ( np.average( f0[base:base+10] ) < f0_ave and abs(np.average( f0[base:base+10] ) - f0_ave) > 30) :
            f0_vel[base] = 0

    if len(wordInfoFromStt) > 0  :  
        for i in wordInfoFromStt :
            head = i["start_index"] - 30
            tail = i["start_index"] + 30
            if head > 0 and tail < len(f0_vel) :
                indice = head + np.argmax(f0_vel[head: tail])
                if f0_vel[indice] > 0 and not indice in startPosition :
                    startPosition.append(indice)
    if len(startPosition) < len(wordInfoFromStt) :
        head = wordInfoFromStt[len(wordInfoFromStt) - 1]["end_index"]
        if head - 30 > 0 :
            indice = head - 30 + np.argmax(f0_vel[head - 30: len(f0_vel)])
            if not indice in startPosition :
                startPosition.append(indice)
        elif not head in startPosition :
            startPosition.append(head)
    if len(startPosition) < len(wordInfoFromStt) :
        for i in range(0, len(f0_vel)) :
            if f0_vel[i] > 1 :
                if i + 50 < len(f0_vel) :
                    indice = i + np.argmax(f0_vel[i: i + 50])
                    if not indice in startPosition :
                        startPosition.append(indice)
                elif not i in startPosition :
                    startPosition.append(i)
                break  

    if len(startPosition) > 0 :
        word = ''
        startPosition.sort()
        f0_len = len(f0_vel)
        for i in range(0, len(startPosition)) :
            if i < len(wordInfoFromStt) :
                word = wordInfoFromStt[i]['word']
            else :
                word = " "
            if i == len(startPosition) - 1 :
                wordInfo.append({
                    "word": word,
                    "start": int( startPosition[i] / f0_len * len(x) ),
                    "end": int(len(x) - 1),
                    "f0": f0_ave,
                    "f0Start": int(startPosition[i]),
                    "f0End": int(len(f0_vel) - 1)
                })
            else :
                wordInfo.append({
                    "word": word,
                    "start": int( startPosition[i] / f0_len * len(x) - 1),
                    "end": int( startPosition[i + 1] / f0_len * len(x) - 1),
                    "f0": f0_ave,
                    "f0Start": int(startPosition[i]),
                    "f0End": int(startPosition[i + 1])
                })

    '''if(len(wordInfo) > 0) :
        prev_end = 0
        for index in range(0, len(wordInfo) - 1) :
            next_start = wordInfo[index + 1]['f0Start']
            wordInfo[index]['f0Start'] = int((wordInfo[index]['f0Start'] + prev_end) / 2)
            prev_end = wordInfo[index]['f0End']
            wordInfo[index]['f0End'] = int((wordInfo[index]['f0End'] + next_start) / 2)
        wordInfo[0]['f0Start'] = 0
        wordInfo[len(wordInfo) - 1]['f0Start'] = int((wordInfo[len(wordInfo) - 1]['f0Start'] + prev_end) / 2)
        wordInfo[len(wordInfo) - 1]['f0End'] = len(f0)'''

    buffer.seek(0)
    base64 = b64encode(buffer.getvalue())
    audioString = base64.decode('utf-8')

    print(wordInfo)
    print('server end')
    return jsonify({"wordInfo": wordInfo, "audio": audioString})


@app.route("/tune", methods=["POST"])
def returnWav():
    print("hello, tune")

    import base64

    buffer = io.BytesIO()
    audioSegment = AudioSegment.from_file(request.files["audio"])
    audioSegment = audioSegment.set_channels(1)
    audioSegment.export(buffer, format="wav")
    
    '''buffer = io.BytesIO(base64.b64decode(request.form["audio"]))
    audioSegment = AudioSegment(buffer)
    audioSegment = audioSegment.set_channels(1)
    #audioSegment.export('4_4.wav', format="wav")
    audioSegment.export(buffer, format="wav")'''

    buffer.seek(0)
    x, fs = sf.read(buffer)
    f0, t = pw.harvest(x, fs)
    sp_h = pw.cheaptrick(x, f0, t, fs)
    ap_h = pw.d4c(x, f0, t, fs)

    f0FromClient = request.form['f0']
    f0FromClient = f0FromClient[1:-1].split(',')

    arrayFromClient = []
    for element in f0FromClient :
        arrayFromClient.append(float(element))
    for index in range(0, len(arrayFromClient)) :
        f0[index] = arrayFromClient[index]
    
    y_h = pw.synthesize(f0, sp_h, ap_h, fs, pw.default_frame_period)
    buffer.seek(0)
    sf.write(buffer, y_h, fs, format='wav')
    base64 = b64encode(buffer.getvalue())
    
    print('server end')
    return make_response(base64)


@app.route("/getURL", methods=["GET"])
def returnURL():
    print("hello, URL")
    print('server end')
    return make_response("https://youtu.be/9UoWtWaM1FA")


if __name__ == "__main__":

    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
