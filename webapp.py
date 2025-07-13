from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production!

CREDS_FILE = 'creds.json'
LOG_FILE = 'log.txt'
USERNAME = 'admin'
PASSWORD = 'BallsInYourFace69!'

def load_creds(query_ip=None):
    try:
        with open(CREDS_FILE, 'r') as f:
            creds = json.load(f)
    except:
        creds = []

    if query_ip:
        creds = [c for c in creds if c['ip'] == query_ip]
    return creds

@app.route('/robots.txt')
def robots_txt():
    return app.send_static_file('robots.txt')

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    query_ip = request.args.get('ip', '').strip()
    creds = load_creds(query_ip)
    return render_template('index.html', creds=creds, ip=query_ip)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/creds')
def api_creds():
    if 'logged_in' not in session:
        return jsonify([])

    query_ip = request.args.get('ip', '').strip()
    creds = load_creds(query_ip)
    return jsonify(creds)

@app.route('/api/logs')
def api_logs():
    if 'logged_in' not in session:
        return jsonify({"log": ""})

    if not os.path.exists(LOG_FILE):
        return jsonify({"log": ""})
    with open(LOG_FILE, 'r') as f:
        content = f.read()
    return jsonify({"log": content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
