from flask import Flask, render_template, Response
import time
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

isTouched = False

@app.route('/')
def index():
    
    return render_template('index.html',initData= '1' if isTouched else '0')
@app.route('/recieve')
def recieve():
    
    return render_template('recieve.html',initData= '1' if isTouched else '0')

@socketio.on('message')
def handle_message(data):
    message = data['message']
    global isTouched 
    isTouched = message
    # print('Received message:', message)
    emit('message', {'message': message}, broadcast=True)
@app.route('/listen')
def listen():
    def event_stream():
        with app.app_context():
            
            while True:
                
                yield f'data: {isTouched}\n\n'
                time.sleep(0.1) 
    return Response(event_stream(), mimetype='text/event-stream')

    