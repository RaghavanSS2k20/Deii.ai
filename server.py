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
@socketio.on('perform_task')  # Define a Socket.IO event
def handle_perform_task(data):
    query = data.get('prompt')  # Get the prompt from the data
    if not query:
        emit('response', {'error': 'No prompt provided'})  # Send error back to client
        return

    # Call the slave function to process the prompt
    for response in slave(llm, query):  # Call slave and iterate over the yielded responses
        emit('response', {'content': response})  # Emit each part of the response to the client

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
     socketio.run(app,debug=True)