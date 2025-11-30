# main.py
# Coded By iosmen (c) 2025

from flask import Flask, request, jsonify, render_template_string
import subprocess
import socket
import os
import shlex

app = Flask(__name__)

TERMINAL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>iPhone Terminal</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="apple-touch-icon" sizes="128x128" href="https://itweb-project-icons-site.netlify.app/apple/ios/assets/apple@x128.png">
    <link rel="icon" type="image/x-icon" href="https://itweb-project-icons-site.netlify.app/apple/ios/assets/terminal_web_icon.ico">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Courier New', monospace; 
            background: #0c0c0c; 
            color: #cccccc; 
            height: 100vh; 
            overflow: hidden;
        }
        .terminal { 
            height: 100vh; 
            padding: 20px; 
            display: flex; 
            flex-direction: column; 
        }
        .header { 
            background: #1a1a1a; 
            padding: 10px; 
            border-radius: 5px 5px 0 0; 
            margin-bottom: 10px;
        }
        .output { 
            flex: 1; 
            background: #000000; 
            padding: 15px; 
            border-radius: 0 0 5px 5px; 
            overflow-y: auto; 
            border: 1px solid #333333;
            margin-bottom: 10px;
        }
        .input-line { 
            display: flex; 
            background: #000000; 
            padding: 10px; 
            border-radius: 5px; 
            border: 1px solid #333333;
        }
        .prompt { 
            color: #cccccc; 
            margin-right: 10px; 
            white-space: nowrap;
        }
        #commandInput { 
            flex: 1; 
            background: transparent; 
            border: none; 
            color: #cccccc; 
            font-family: 'Courier New', monospace; 
            font-size: 14px; 
            outline: none;
        }
        .quick-commands { 
            display: flex; 
            flex-wrap: wrap; 
            gap: 5px; 
            margin-bottom: 10px; 
            padding: 10px; 
            background: #1a1a1a; 
            border-radius: 5px;
        }
        .quick-btn { 
            background: #2d2d2d; 
            color: #cccccc; 
            border: none; 
            padding: 5px 10px; 
            border-radius: 3px; 
            cursor: pointer; 
            font-family: 'Courier New', monospace;
        }
        .quick-btn:hover { background: #3d3d3d; }
        .connection-info { 
            color: #888888; 
            font-size: 12px; 
            margin-bottom: 10px; 
            text-align: center;
        }
        .line { margin: 5px 0; white-space: pre-wrap; word-break: break-all; }
        .error { color: #ff6b6b; }
        .success { color: #cccccc; }
        .info { color: #f1c27d; }
        .warning { color: #ffd966; }
        .command { color: #cccccc; }
    </style>
</head>
<body>
    <div class="terminal">
        <div class="header">
            <h2 style="color: #cccccc;">iPhone Terminal</h2>
            <div class="connection-info" id="connectionInfo">
                Checking connection...
            </div>
        </div>
        
        <div class="quick-commands">
            <button class="quick-btn" onclick="runCommand('ls -la')">List Files</button>
            <button class="quick-btn" onclick="runCommand('pwd')">Current Dir</button>
            <button class="quick-btn" onclick="runCommand('uptime')">Uptime</button>
            <button class="quick-btn" onclick="runCommand('whoami')">User</button>
            <button class="quick-btn" onclick="runCommand('uname -a')">System Info</button>
            <button class="quick-btn" onclick="runCommand('df -h')">Disk Usage</button>
            <button class="quick-btn" onclick="runCommand('free -h')">Memory</button>
            <button class="quick-btn" onclick="runCommand('ifconfig')">Network</button>
            <button class="quick-btn" onclick="runCommand('ps aux')">Processes</button>
            <button class="quick-btn" onclick="runCommand('python3 --version')">Python</button>
            <button class="quick-btn" onclick="runCommand('clear')">Clear</button>
        </div>

        <div class="output" id="output">
            <div class="line info">Welcome to iPhone Web Terminal!</div>
            <div class="line info">Coded By iosmen (c) 2025</div>
            <div class="line info">You can run all system commands</div>
            <div class="line info">Example commands: ls, cd, pwd, cat, grep, find, ps, top, etc.</div>
            <div class="line info">Warning: All commands are executable!</div>
            <div class="line"><br></div>
        </div>

        <div class="input-line">
            <span class="prompt" id="prompt">iphone:~ mobile$</span>
            <input type="text" id="commandInput" placeholder="Enter any command (e.g.: ls -la, cat /etc/hosts)" autofocus>
        </div>
    </div>

    <script>
        const output = document.getElementById('output');
        const commandInput = document.getElementById('commandInput');
        const connectionInfo = document.getElementById('connectionInfo');
        const prompt = document.getElementById('prompt');
        let currentDir = '~';

        window.addEventListener('load', function() {
            checkConnection();
            getCurrentDir();
        });

        function checkConnection() {
            fetch('/health')
                .then(response => response.json())
                .then(data => {
                    connectionInfo.innerHTML = `Connection active | Server: ${data.hostname} | User: ${data.user} | Directory: ${data.current_dir}`;
                    currentDir = data.current_dir;
                    updatePrompt();
                })
                .catch(error => {
                    connectionInfo.innerHTML = 'Connection error';
                    console.error('Connection error:', error);
                });
        }

        function getCurrentDir() {
            fetch('/pwd')
                .then(response => response.json())
                .then(data => {
                    if (!data.error) {
                        currentDir = data.output.trim();
                        updatePrompt();
                    }
                })
                .catch(error => {
                    console.error('PWD error:', error);
                });
        }

        function updatePrompt() {
            const dirName = currentDir.split('/').pop() || '~';
            prompt.textContent = `iphone:${dirName} ${getCurrentUser()}$`;
        }

        function getCurrentUser() {
            return 'mobile';
        }

        function addOutput(line, className = '') {
            const lineElement = document.createElement('div');
            lineElement.className = `line ${className}`;
            lineElement.textContent = line;
            output.appendChild(lineElement);
            output.scrollTop = output.scrollHeight;
        }

        function runCommand(cmd) {
            if (!cmd.trim()) return;

            commandInput.value = '';
            
            addOutput(`iphone:${currentDir.split('/').pop() || '~'} ${getCurrentUser()}$ ${cmd}`, 'command');
            
            fetch('/run', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({cmd: cmd})
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    addOutput(data.error, 'error');
                } else {
                    addOutput(data.output);
                    
                    if (cmd.trim().startsWith('cd ')) {
                        setTimeout(getCurrentDir, 100);
                    }
                }
            })
            .catch(error => {
                addOutput('Command execution error: ' + error, 'error');
            });
        }

        function clearTerminal() {
            output.innerHTML = '';
            addOutput('Terminal Cleared', 'info');
        }

        commandInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const cmd = this.value.trim();
                if (cmd) {
                    runCommand(cmd);
                }
            }
        });

        let commandHistory = [];
        let historyIndex = -1;

        commandInput.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (commandHistory.length > 0) {
                    if (historyIndex === -1) {
                        historyIndex = commandHistory.length - 1;
                    } else if (historyIndex > 0) {
                        historyIndex--;
                    }
                    this.value = commandHistory[historyIndex] || '';
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (historyIndex < commandHistory.length - 1) {
                    historyIndex++;
                    this.value = commandHistory[historyIndex] || '';
                } else {
                    historyIndex = -1;
                    this.value = '';
                }
            }
        });

        commandInput.focus();
    </script>
</body>
</html>
"""

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_hostname():
    try:
        return socket.gethostname()
    except:
        return "iphone"

def get_current_user():
    try:
        return subprocess.check_output(["whoami"]).decode().strip()
    except:
        return "mobile"

def get_current_directory():
    try:
        return subprocess.check_output(["pwd"]).decode().strip()
    except:
        return "~"

@app.route("/")
def home():
    local_ip = get_local_ip()
    return render_template_string(TERMINAL_HTML, local_ip=local_ip, port=5000)

@app.route("/run", methods=["POST"])
def run_command():
    data = request.get_json()
    cmd = data.get("cmd", "").strip()

    if not cmd:
        return jsonify({"error": "Command cannot be empty"}), 400

    DANGEROUS_COMMANDS = ['rm -rf /', ':(){ :|:& };:', 'mkfs', 'dd if=/dev/random']
    if any(dangerous in cmd for dangerous in DANGEROUS_COMMANDS):
        return jsonify({"error": "This command is blocked for security reasons"}), 403

    try:
        if cmd.startswith('cd '):
            directory = cmd[3:].strip()
            try:
                os.chdir(directory)
                new_dir = os.getcwd()
                return jsonify({"output": f"Directory changed to: {new_dir}"})
            except Exception as e:
                return jsonify({"error": f"cd: {str(e)}"}), 500
        else:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                return jsonify({"output": result.stdout})
            else:
                return jsonify({"error": result.stderr}), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Command timed out (30 seconds)"}), 500
    except Exception as e:
        return jsonify({"error": f"Command execution error: {str(e)}"}), 500

@app.route("/pwd")
def get_pwd():
    try:
        current_dir = os.getcwd()
        return jsonify({"output": current_dir})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health_check():
    try:
        hostname = get_hostname()
        user = get_current_user()
        current_dir = get_current_directory()
        
        return jsonify({
            "status": "healthy",
            "hostname": hostname,
            "user": user,
            "current_dir": current_dir
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def print_network_info():
    local_ip = get_local_ip()
    hostname = get_hostname()
    
    print("=" * 60)
    print("iPhone Terminal Server Started!")
    print("=" * 60)
    print(f"Local IP: http://{local_ip}:5000")
    print(f"Localhost: http://127.0.0.1:5000")
    print(f"Hostname: {hostname}")
    print(f"User: {get_current_user()}")
    print(f"Port: 5000")
    print("=" * 60)
    print("To connect from other devices on the network:")
    print(f"   http://{local_ip}:5000")
    print("=" * 60)
    print("FEATURES:")
    print("   All system commands executable")
    print("   cd command supported")
    print("   Real-time directory tracking")
    print("   Command history")
    print("=" * 60)
    print("WARNING: All commands are executable! Be careful!")
    print("=" * 60)
    print("To stop: Ctrl+C")
    print("=" * 60)

if __name__ == "__main__":
    print_network_info()
    app.run(host="0.0.0.0", port=5000, debug=False)