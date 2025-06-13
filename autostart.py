import subprocess
import os

# Get the full path to the project base directory
basedir = os.path.dirname(os.path.abspath(__file__))

# Define script and executable paths
flask_script = os.path.join(basedir, 'core', 'tv_server.py')
ngrok_exe = os.path.join(basedir, 'ngrok', 'ngrok.exe')

# Launch Flask webhook server
print("🚀 Launching Flask webhook...")
subprocess.Popen(['python', flask_script])

# Launch ngrok to expose port 80
print("🌐 Launching ngrok tunnel on port 80...")
subprocess.Popen([ngrok_exe, 'http', '80'])

print("✅ System started: Flask + Ngrok")
