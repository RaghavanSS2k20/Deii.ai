from flask import Flask, send_file, request, jsonify
from flask_cors import CORS, cross_origin

from gtts import gTTS
from io import BytesIO
from io import BytesIO
import base64
app = Flask(__name__)
CORS(app,supports_credentials=True)
from scavange_bunker.scavange_bunker import get_data, send_attendance
@app.route('/')
@cross_origin()

def generate_audio():
    text = "punda deii"
    
    # Generate audio using gTTS
    tts = gTTS(text=text, lang='en')
    
    # Create an in-memory file-like object
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    
    # Reset the file pointer to the beginning
    audio_file.seek(0)
    
    # Convert the audio data to base64 for easier transmission
    audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
    
    # Return the audio data as a JSON response
    return jsonify({'audio_data': audio_data})

@app.route('/getdata', methods=['GET'])
def get_data_route():
    return  get_data()
if __name__ == '__main__':
    app.run(debug=True)