from flask import Flask, render_template, request, session, make_response, jsonify
import jwt
from datetime import datetime, timedelta
from functools import wraps
import config

app = Flask(__name__)
app.config['secret_key'] = config.secret_key

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message ': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['secret_key'])
        except:
            return jsonify({'message ': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/')

def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'logged in'

@app.route('/home')

def home():
        return render_template('home.html')

@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to the dashboard!'

@app.route('/about')

def about():
    return render_template('about.html')

@app.route('/contact')

def contact():
    return render_template('contact.html')

@app.route('/portfolio')

def portfolio():
    return render_template('portfolio.html')

@app.route('/resume')

def resume():
    return render_template('resume.html')

@app.route('/login', methods=['POST'])

def login():
    if request.form['username'] and request.form['password'] == 'admin':
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'exp': str(datetime.utcnow() + timedelta(seconds=240))
    }, 
    
        app.config['secret_key'])
        return jsonify({'token': token.decode('UTF-8')})
    else:
        return make_response('Could not verify', 403, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    

if __name__ == '__main__':
    app.run(debug=True)