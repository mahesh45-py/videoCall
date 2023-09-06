from flask import Flask, render_template, Response, request, jsonify
import time
from flask_socketio import SocketIO, emit
import requests
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
CORS(app)

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

@app.route('/api/news')
def getNews():
    if request.method == 'GET':
        page = request.args.get('page')
        if not page:
            page = '1'
        url = 'https://www.ntnews.com/wp-json/ntnews/v1/latest-news-api?page='+page

        response = requests.get(url)
        if response.status_code == 200:
            # Parse and work with the response data (in JSON format)
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({
                'message':'An unexpected error occured',
                'code':response.status_code
            })
@app.route('/api/category')
def getAndhraNews():
    if request.method == 'GET':
        page = request.args.get('catname')
        if not page:
            page = 'andhrapradesh-news'
        url = 'https://www.ntnews.com/wp-json/ntnews/v1/category-api?cat_name='+page

        response = requests.get(url)
        if response.status_code == 200:
            # Parse and work with the response data (in JSON format)
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({
                'message':'An unexpected error occured',
                'code':response.status_code
            })
@app.route('/api/odisha')
def getOdishaNews():
    if request.method == 'GET':
        page = request.args.get('per_page')
        if not page:
            page = '20'
        url = 'https://odishabytes.com/wp-json/wp/v2/posts?per_page='+page

        response = requests.get(url)
        if response.status_code == 200:
            # Parse and work with the response data (in JSON format)
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({
                'message':'An unexpected error occured',
                'code':response.status_code
            })

    