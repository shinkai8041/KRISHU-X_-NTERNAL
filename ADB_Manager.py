"""
KRISHU X INTERNAL - ADB MANAGER
Fixed Timeout Issues + Multiple Port Support
"""

import subprocess
import os
import time
import psutil
from typing import Tuple, List, Optional

class ADBManager:
    def __init__(self):
        self.adb_path = None
        self.connected = False
        self.current_port = None
        self.device_serial = None
        
    def find_adb(self) -> bool:
        """Find ADB executable - Multiple locations"""
        adb_paths = [
            r"C:\Program Files\BlueStacks_nxt\HD-Adb.exe",
            r"C:\Program Files\BlueStacks_msi5\HD-Adb.exe",
            r"C:\Program Files\LDPlayer\adb.exe",
            r"C:\LDPlayer\LDPlayer9\adb.exe",
            r"C:\Program Files\Nox\bin\adb.exe",
            r"C:\Program Files\Microvirt\MEmu\adb.exe",
            r"C:\Program Files\MuMu\emulator\nemu\EmulatorShell\adb.exe",
        ]
        
        for path in adb_paths:
            if os.path.exists(path):
                self.adb_path = path
                return True
        
        # Try to find from PATH
        try:
            result = subprocess.run(["where", "adb.exe"], capture_output=True, text=True, shell=True, timeout=5)
            if result.stdout.strip():
                self.adb_path = result.stdout.strip().split('\n')[0]
                return True
        except:
            pass
        
        return False
    
    def is_emulator_running(self) -> bool:
        """Check if any emulator is running"""
        emulators = ["HD-Player.exe", "BlueStacks.exe", "Ld9BoxHeadless.exe", "dnplayer.exe"]
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] in emulators:
                    return True
        except:
            pass
        return False
    
    def kill_adb_server(self):
        """Kill existing ADB server"""
        if self.adb_path:
            try:
                subprocess.run([self.adb_path, "kill-server"], capture_output=True, timeout=5)
            except:
                pass
        time.sleep(1)
    
    def start_adb_server(self):
        """Start ADB server"""
        if self.adb_path:
            try:
                subprocess.run([self.adb_path, "start-server"], capture_output=True, timeout=5)
            except:
                pass
        time.sleep(2)
    
    def connect(self) -> Tuple[bool, str]:
        """Connect to emulator via ADB"""
        if not self.is_emulator_running():
            return False, "No emulator running! Start BlueStacks/LDPlayer first."
        
        if not self.find_adb():
            return False, "ADB not found! Please install BlueStacks or LDPlayer."
        
        self.kill_adb_server()
        self.start_adb_server()
        
        # Try multiple ports
        ports = [5555, 5554, 5556, 5557, 21503, 21513, 21523, 62001, 62025, 7555]
        
        for port in ports:
            try:
                result = subprocess.run(
                    [self.adb_path, "connect", f"127.0.0.1:{port}"],
                    capture_output=True, text=True, timeout=5
                )
                output = result.stdout.lower()
                if "connected" in output or "already connected" in output:
                    self.connected = True
                    self.current_port = port
                    self.device_serial = f"127.0.0.1:{port}"
                    return True, f"ADB Connected on port {port}!"
            except subprocess.TimeoutExpired:
                continue
            except:
                continue
        
        # Try auto-connect
        try:
            result = subprocess.run([self.adb_path, "connect", "127.0.0.1"], capture_output=True, text=True, timeout=5)
            if "connected" in result.stdout.lower():
                self.connected = True
                return True, "ADB Connected (auto)!"
        except:
            pass
        
        return False, "Could not connect to ADB. Try restarting emulator."
    
    def disconnect(self) -> Tuple[bool, str]:
        """Disconnect ADB"""
        if self.adb_path and self.device_serial:
            try:
                subprocess.run([self.adb_path, "disconnect", self.device_serial], capture_output=True, timeout=5)
            except:
                pass
        self.connected = False
        self.device_serial = None
        return True, "ADB Disconnected"
    
    def is_connected(self) -> bool:
        """Check if ADB is connected"""
        return self.connected
    
    def get_devices(self) -> List[str]:
        """Get list of connected devices"""
        if not self.adb_path:
            return []
        try:
            result = subprocess.run([self.adb_path, "devices"], capture_output=True, text=True, timeout=5)
            devices = []
            for line in result.stdout.split('\n')[1:]:
                if '\tdevice' in line:
                    devices.append(line.split('\t')[0])
            return devices
        except:
            return []
    
    def get_package(self) -> str:
        """Get running Free Fire package"""
        packages = ["com.dts.freefireth", "com.dts.freefiremax"]
        for pkg in packages:
            try:
                result = subprocess.run(
                    [self.adb_path, "shell", "pidof", pkg],
                    capture_output=True, text=True, timeout=5
                )
                if result.stdout.strip():
                    return pkg
            except:
                pass
        return ""
    
    def get_module_base(self, package: str, module: str) -> int:
        """Get module base address"""
        try:
            # Get PID
            result = subprocess.run(
                [self.adb_path, "shell", "pidof", package],
                capture_output=True, text=True, timeout=5
            )
            pid = result.stdout.strip()
            if not pid:
                return 0
            
            # Get module base
            result = subprocess.run(
                [self.adb_path, "shell", f"cat /proc/{pid}/maps | grep {module}"],
                capture_output=True, text=True, timeout=5
            )
            if result.stdout:
                base = result.stdout.split('-')[0]
                return int(base, 16)
        except:
            pass
        return 0
    
    def execute(self, cmd: str) -> Tuple[bool, str]:
        """Execute ADB shell command"""
        if not self.connected or not self.adb_path:
            return False, "ADB not connected"
        try:
            result = subprocess.run(
                [self.adb_path, "shell", cmd],
                capture_output=True, text=True, timeout=10
            )
            return True, result.stdout
        except subprocess.TimeoutExpired:
            return False, "Command timeout"
        except Exception as e:
            return False, str(e)
