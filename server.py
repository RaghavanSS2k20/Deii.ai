from flask import Flask, send_file, request, jsonify
from flask_cors import CORS, cross_origin

from LLM import llm
from gtts import gTTS
from io import BytesIO
from io import BytesIO
from flask_socketio import SocketIO, emit
import base64
from app import slave
app = Flask(__name__)
CORS(app,supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*')
from scavange_bunker.scavange_bunker import get_data, send_attendance
@app.route('/', methods=['POST'])
@cross_origin()
def perform_task():
    query = request.get_json().get('prompt')
    for response in slave(llm, query):
        emit('response', {'content': response})  # Emit each part of the response to the client
    
    return jsonify({'status': 'Processing started'}), 202  # Return a


if __name__ == '__main__':
     socketio.run(app,debug=True)