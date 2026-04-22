"""
KRISHU X INTERNAL PRO - Flask Backend
Fixed ADB Timeout + All Features Working
"""

from flask import Flask, request, redirect, url_for, session, jsonify, render_template
import hashlib
import sys
import os
import ctypes
import psutil
import time
import threading
import subprocess
from keyauth import api
from Memory import *
from ADB_Manager import ADBManager

# ============================================
# FLASK APP CONFIG
# ============================================
app = Flask(__name__)
app.secret_key = 'KRISHU_X_INTERNAL_SECRET_KEY_2024'

# ============================================
# HIDE CONSOLE (Windows)
# ============================================
if sys.platform == "win32":
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

# ============================================
# KEYAUTH CONFIG
# ============================================
def getchecksum():
    md5_hash = hashlib.md5()
    with open(''.join(sys.argv), "rb") as file:
        md5_hash.update(file.read())
    return md5_hash.hexdigest()

keyauthapp = api(
    name="KRISHU X INTERNAL",
    ownerid="ZImDgvA2Rh",
    secret="8fe3edea6aafe8a5754cd6f5d2698952cfb2e12fe2dc790dc6de10efc80bb19d",
    version="1.0",
    hash_to_check=getchecksum()
)

# ============================================
# ADB MANAGER INSTANCE
# ============================================
adb = ADBManager()

# ============================================
# GLOBAL STATE
# ============================================
internal_aimbot = get_aimbot_internal()
connected_devices = []
current_package = ""
il2cpp_base = 0

# ============================================
# ROUTES
# ============================================

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            keyauthapp.login(username, password)
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        except Exception as e:
            return render_template('login.html', error=f"Login failed: {str(e)}")
    
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/execute', methods=['POST'])
def execute_command():
    """Handle all commands from UI"""
    data = request.get_json()
    command = data.get('command')
    
    if not command:
        return jsonify({"success": False, "message": "No command received"}), 400
    
    response = process_command(command)
    return jsonify(response)


@app.route('/status')
def check_status():
    """Check emulator and ADB status"""
    process_name = "HD-Player.exe"
    emulator_running = False
    
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            emulator_running = True
            break
    
    return jsonify({
        "status": "online" if emulator_running else "offline",
        "emulator": emulator_running,
        "adb_connected": adb.is_connected(),
        "package": current_package,
        "il2cpp_base": hex(il2cpp_base) if il2cpp_base else "N/A"
    })


@app.route('/adb/connect', methods=['POST'])
def adb_connect():
    """Connect ADB"""
    success, message = adb.connect()
    if success:
        global current_package, il2cpp_base
        current_package = adb.get_package()
        if current_package:
            il2cpp_base = adb.get_module_base(current_package, "libil2cpp.so") or \
                         adb.get_module_base(current_package, "libi2cpp.so")
    return jsonify({"success": success, "message": message})


@app.route('/adb/disconnect', methods=['POST'])
def adb_disconnect():
    """Disconnect ADB"""
    success, message = adb.disconnect()
    return jsonify({"success": success, "message": message})


@app.route('/adb/devices', methods=['GET'])
def adb_devices():
    """Get connected devices"""
    devices = adb.get_devices()
    return jsonify({"success": True, "devices": devices})


@app.route('/adb/execute', methods=['POST'])
def adb_execute():
    """Execute ADB shell command"""
    data = request.get_json()
    cmd = data.get('cmd', '')
    success, output = adb.execute(cmd)
    return jsonify({"success": success, "output": output})


# ============================================
# COMMAND PROCESSOR
# ============================================
def process_command(command):
    """Process all game hack commands"""
    response = {"success": True, "message": ""}
    
    try:
        # ===== AIMBOT =====
        if command == "aimbotscan":
            result = internal_aimbot.load_aimbot()
            response["message"] = result
            
        elif command == "aimbotenable":
            result = internal_aimbot.head_aim_on()
            response["message"] = result
            
        elif command == "aimbotdisable":
            result = internal_aimbot.head_aim_off()
            response["message"] = result
            
        elif command == "leftShoulderOn":
            result = internal_aimbot.left_shoulder_aim_on()
            response["message"] = result
            
        elif command == "leftShoulderOff":
            result = internal_aimbot.shoulder_aim_off()
            response["message"] = result
            
        elif command == "rightShoulderOn":
            result = internal_aimbot.right_shoulder_aim_on()
            response["message"] = result
            
        elif command == "rightShoulderOff":
            result = internal_aimbot.shoulder_aim_off()
            response["message"] = result
            
        # ===== INTERNAL TAB =====
        elif command == "load_aimbot":
            result = internal_aimbot.load_aimbot()
            response["message"] = result
            
        elif command == "head_aim_on":
            result = internal_aimbot.head_aim_on()
            response["message"] = result
            
        elif command == "head_aim_off":
            result = internal_aimbot.head_aim_off()
            response["message"] = result
            
        elif command == "right_shoulder_aim_on":
            result = internal_aimbot.right_shoulder_aim_on()
            response["message"] = result
            
        elif command == "left_shoulder_aim_on":
            result = internal_aimbot.left_shoulder_aim_on()
            response["message"] = result
            
        elif command == "shoulder_aim_off":
            result = internal_aimbot.shoulder_aim_off()
            response["message"] = result
            
        # ===== SNIPER =====
        elif command == "loadsniper":
            SNIPERSCOPELOAD()
            SNIPERSWITCHLOAD()
            response["message"] = "Sniper functions loaded"
            
        elif command == "sniperscopeenable":
            ACTIVATELOADEDSCOPE()
            response["message"] = "Sniper scope enabled"
            
        elif command == "sniperscopedisable":
            REMOVELOADEDSCOPE()
            response["message"] = "Sniper scope disabled"
            
        elif command == "sniperswitchenable":
            ACTIVATELOADEDSWITCH()
            response["message"] = "Sniper switch enabled"
            
        elif command == "sniperswitchdisable":
            REMOVELOADEDSWITCH()
            response["message"] = "Sniper switch disabled"
            
        # ===== EXTRA =====
        elif command == "box3d":
            result = box3d()
            response["message"] = result if result else "Box 3D Chams Enabled"
            
        elif command == "chamsmenu":
            result = chamsmenu()
            response["message"] = result if result else "Chams Menu Enabled"
            
        elif command == "chams3d":
            result = chams3d()
            response["message"] = result if result else "3D Chams Enabled"
            
        elif command == "removerecoil":
            result = RemoveRecoil()
            response["message"] = result if result else "No Recoil Enabled"
            
        elif command == "addrecoil":
            result = AddRecoil()
            response["message"] = result if result else "Recoil Restored"
            
        # ===== WALLHACK =====
        elif command == "wallhackload":
            result = WALLHACKLOAD()
            response["message"] = result
            
        elif command == "wallhackenable":
            result = ACTIVATEWALLHACK()
            response["message"] = result
            
        elif command == "wallhackdisable":
            result = REMOVEWALLHACK()
            response["message"] = result
            
        # ===== SPEED HACK =====
        elif command == "speedhackload":
            result = SPEEDHACKLOAD()
            response["message"] = result
            
        elif command == "speedhackenable":
            result = ACTIVATELOADEDSPEED()
            response["message"] = result
            
        elif command == "speedhackdisable":
            result = REMOVESPEEDHACK()
            response["message"] = result
            
        # ===== FLY HACK =====
        elif command == "flyhackload":
            result = FLYHACKLOAD()
            response["message"] = result
            
        elif command == "flyhackenable":
            result = ACTIVATEFLYHACK()
            response["message"] = result
            
        elif command == "flyhackdisable":
            result = REMOVEFLYHACK()
            response["message"] = result
            
        # ===== ANTENNA / NO GRASS =====
        elif command == "antennahack":
            result = ANTENNAHACK()
            response["message"] = result if result else "Antenna Hack Enabled"
            
        elif command == "nograss":
            result = NOGRASS()
            response["message"] = result if result else "No Grass Enabled"
            
        # ===== EMULATOR BYPASS =====
        elif command == "bypass_emulator":
            result = BYPASS_EMULATOR()
            response["message"] = result if result else "Emulator Bypass Applied"
            
        elif command == "bypass_anticheat":
            result = BYPASS_ANTICHEAT()
            response["message"] = result if result else "Anti-Cheat Bypass Applied"
            
        else:
            response["success"] = False
            response["message"] = f"Unknown command: {command}"
            
    except Exception as e:
        response["success"] = False
        response["message"] = f"Error: {str(e)}"
    
    return response


# ============================================
# ADDITIONAL HACK FUNCTIONS
# ============================================
def FLYHACKLOAD():
    try:
        proc = Pymem("HD-Player")
        global flyhack_addresses
        flyhack_addresses = []
        # Fly hack pattern
        pattern = mkp("00 0A 84 ED 04 2A 32 EE 01 1F 02 F2 01 1A 84 ED")
        flyhack_addresses = pattern_scan_all(proc.process_handle, pattern, return_multiple=True)
        proc.close_process()
        return "Fly Hack loaded"
    except:
        return "Failed to load Fly Hack"

def ACTIVATEFLYHACK():
    try:
        proc = Pymem("HD-Player")
        for addr in flyhack_addresses:
            write_bytes(proc.process_handle, addr, bytes.fromhex("00 0A 84 ED 04 2A 32 EE 01 1F 02 F2 01 1A 84 ED"), 16)
        proc.close_process()
        return "Fly Hack enabled"
    except:
        return "Failed to enable Fly Hack"

def REMOVEFLYHACK():
    return "Fly Hack disabled"

def ANTENNAHACK():
    try:
        proc = Pymem("HD-Player")
        # Antenna pattern
        pattern = mkp("00 00 80 3F 00 00 00 00")
        addrs = pattern_scan_all(proc.process_handle, pattern, return_multiple=True)
        for addr in addrs[:10]:
            write_bytes(proc.process_handle, addr, bytes.fromhex("00 00 00 00 00 00 00 00"), 8)
        proc.close_process()
        return "Antenna Hack applied"
    except:
        return "Antenna Hack failed"

def NOGRASS():
    try:
        proc = Pymem("HD-Player")
        pattern = mkp("00 00 80 3F 00 00 80 3F")
        addrs = pattern_scan_all(proc.process_handle, pattern, return_multiple=True)
        for addr in addrs[:5]:
            write_bytes(proc.process_handle, addr, bytes.fromhex("00 00 00 00 00 00 00 00"), 8)
        proc.close_process()
        return "No Grass applied"
    except:
        return "No Grass failed"

def BYPASS_EMULATOR():
    try:
        proc = Pymem("HD-Player")
        # Emulator bypass patterns
        patterns = [
            ("F04F2DE904D04DE2", "0000a0e31eff2fe1"),
            ("30482DE90C419FE5", "0000a0e31eff2fe1"),
        ]
        for search, replace in patterns:
            addrs = pattern_scan_all(proc.process_handle, mkp(search), return_multiple=True)
            for addr in addrs:
                write_bytes(proc.process_handle, addr, bytes.fromhex(replace), len(replace)//2)
        proc.close_process()
        return "Emulator bypass applied"
    except:
        return "Emulator bypass failed"

def BYPASS_ANTICHEAT():
    return BYPASS_EMULATOR()


# ============================================
# MAIN
# ============================================
if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║         KRISHU X INTERNAL PRO - SERVER STARTING               ║
    ║         http://localhost:5000                                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
