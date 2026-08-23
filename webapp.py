import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

CREDS_FILE = os.environ.get('CREDS_FILE', '/data/creds.json')
PASSWORD = os.environ.get('SKIMMER_PASSWORD', 'admin')


def load_creds(query_ip=None, query_host=None, query_source=None):
    try:
        with open(CREDS_FILE, 'r') as f:
            creds = json.load(f)
    except Exception:
        creds = []
    if query_ip:
        creds = [c for c in creds if c.get('ip') == query_ip]
    if query_host:
        creds = [c for c in creds if query_host.lower() in c.get('hostname', '').lower()]
    if query_source:
        creds = [c for c in creds if c.get('source', '').upper() == query_source.upper()]
    return creds


@app.route('/robots.txt')
def robots_txt():
    return app.send_static_file('robots.txt')


@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    query_ip = request.args.get('ip', '').strip()
    query_host = request.args.get('host', '').strip()
    query_source = request.args.get('source', '').strip()
    creds = load_creds(query_ip or None, query_host or None, query_source or None)
    return render_template('index.html', creds=creds, ip=query_ip, host=query_host, source=query_source)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/creds')
def api_creds():
    if 'logged_in' not in session:
        return jsonify([]), 401
    query_ip = request.args.get('ip', '').strip()
    query_host = request.args.get('host', '').strip()
    creds = load_creds(query_ip or None, query_host or None)
    return jsonify(creds)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
