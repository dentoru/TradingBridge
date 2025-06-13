import subprocess, os

basedir = os.path.dirname(__file__)
ngrok_path = os.path.join(basedir, 'ngrok', 'ngrok.exe')
flask_path = os.path.join(basedir, 'core', 'tv_server.py')

# Start Flask webhook server
subprocess.Popen(['python', flask_path])
# Start ngrok tunnel
subprocess.Popen([ngrok_path, 'http', '80'])

print("✅ Flask + ngrok launched.")
