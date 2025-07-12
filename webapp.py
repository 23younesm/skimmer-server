from flask import Flask, render_template, request
import json

app = Flask(__name__)
CREDS_FILE = 'creds.json'

@app.route('/')
def index():
    query_ip = request.args.get('ip', '').strip()
    try:
        with open(CREDS_FILE, 'r') as f:
            creds = json.load(f)
    except:
        creds = []

    if query_ip:
        creds = [c for c in creds if c['ip'] == query_ip]

    return render_template('index.html', creds=creds, ip=query_ip)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
