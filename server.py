from flask import Flask, send_file, request
from flask_cors import CORS
from gtts import gTTS
from io import BytesIO

app = Flask(__name__)
# cors = CORS(app)

@app.route('/')
def ping_service():
    text = "Deii Punda"
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False)
    audio_stream = BytesIO()
    myobj.save(audio_stream)
    audio_stream.seek(0)  # Move to the beginning of the stream
    return send_file(audio_stream, mimetype='audio/mpeg', as_attachment=False, download_name='output.mp3')

if __name__ == '__main__':
    app.run(debug=True)