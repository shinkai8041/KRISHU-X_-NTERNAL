"""
KRISHU X INTERNAL - MEMORY FUNCTIONS
Enhanced with all patterns + Internal Aimbot Class
"""

from flask import *
import threading
import keyboard
from datetime import datetime
import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime
import ctypes
import binascii

from pymem import *
from pymem.memory import read_bytes, write_bytes
from pymem.pattern import pattern_scan_all
import pymem.exception
import pymem.process
import os

# ============================================
# UTILITY FUNCTIONS
# ============================================
def mkp(aob: str):
    """Make pattern from AOB string"""
    if '??' in aob:
        if aob.startswith("??"):
            aob = f" {aob}"
            n = aob.replace(" ??", ".").replace(" ", "\\x")
            b = bytes(n.encode())
        else:
            n = aob.replace(" ??", ".").replace(" ", "\\x")
            b = bytes(f"\\x{n}".encode())
        del n
        return b
    else:
        m = aob.replace(" ", "\\x")
        c = bytes(f"\\x{m}".encode())
        del m
        return c

def _hex_normalize(s: str) -> str:
    """Remove newlines/spaces and return continuous hex string"""
    return ''.join(s.split())

def clear():
    if platform.system() == 'Windows':
        os.system('cls & title KRISHU X INTERNAL')
    elif platform.system() == 'Linux':
        os.system('clear')

def getchecksum():
    md5_hash = hashlib.md5()
    file = open(''.join(sys.argv), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest

# ============================================
# GLOBAL VARIABLES
# ============================================
aimbot_addresses = []
original_value = []

sniperScopeAddress = []
original_Scope_value = []

sniperSwitchAddress = []
original_Switch_value = []

wallhack_addresses = []
original_wall_bytes = []

speedHackAddress = []
original_Speed_value = []

flyhack_addresses = []
original_fly_value = []

# ============================================
# AIMBOT FUNCTIONS
# ============================================
def HEADLOAD():
    try:
        proc = Pymem("HD-Player")
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"

    try:
        if proc:
            print("\033[31m[>]\033[0m Searching Entity...")
            global aimbot_addresses
            entity_pattern = mkp("FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF FF FF FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 00 00 00 00 00 00 00 00 00 00 00 00 A5 43")
            aimbot_addresses = pattern_scan_all(proc.process_handle, entity_pattern, return_multiple=True)

            if aimbot_addresses:
                print(f"Found {len(aimbot_addresses)} addresses")
            else:
                print("Failed to find addresses")
    except:
        pass
    finally:
        if proc:
            proc.close_process()
    return "Aimbot loaded successfully"


def HEADON():
    try:
        proc = Pymem("HD-Player")
        if proc:
            global original_value
            original_value = []
            for current_entity in aimbot_addresses:
                original_value.append((current_entity, read_bytes(proc.process_handle, current_entity + 0xA6, 4)))
                value_bytes = read_bytes(proc.process_handle, current_entity + 0xAA, 4)
                write_bytes(proc.process_handle, current_entity + 0xA6, value_bytes, len(value_bytes))
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"
    finally:
        if proc:
            proc.close_process()
    return "AIMBOT HEAD ON"


def HEADOFF():
    try:
        proc = Pymem("HD-Player")
        if original_value:
            for i in original_value:
                write_bytes(proc.process_handle, i[0] + 0xA6, i[1], len(i[1]))
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"
    finally:
        if proc:
            proc.close_process()
    return "AIMBOT HEAD OFF"


def RIGHTSHOULDERON():
    try:
        proc = Pymem("HD-Player")
        if proc:
            global original_value
            original_value = []
            for current_entity in aimbot_addresses:
                original_value.append((current_entity, read_bytes(proc.process_handle, current_entity + 0xA6, 4)))
                value_bytes = read_bytes(proc.process_handle, current_entity + 0xDA, 4)
                write_bytes(proc.process_handle, current_entity + 0xA6, value_bytes, len(value_bytes))
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"
    finally:
        if proc:
            proc.close_process()
    return "RIGHT SHOULDER AIM ON"


def RIGHTSHOULDEROFF():
    try:
        proc = Pymem("HD-Player")
        if original_value:
            for i in original_value:
                write_bytes(proc.process_handle, i[0] + 0xA6, i[1], len(i[1]))
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"
    finally:
        if proc:
            proc.close_process()
    return "RIGHT SHOULDER AIM OFF"


def LEFTSHOULDERON():
    try:
        proc = Pymem("HD-Player")
        if proc:
            global original_value
            original_value = []
            for current_entity in aimbot_addresses:
                original_value.append((current_entity, read_bytes(proc.process_handle, current_entity + 0xA6, 4)))
                value_bytes = read_bytes(proc.process_handle, current_entity + 0xD6, 4)
                write_bytes(proc.process_handle, current_entity + 0xA6, value_bytes, len(value_bytes))
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"
    finally:
        if proc:
            proc.close_process()
    return "LEFT SHOULDER AIM ON"


def LEFTSHOULDEROFF():
    try:
        proc = Pymem("HD-Player")
        if original_value:
            for i in original_value:
                write_bytes(proc.process_handle, i[0] + 0xA6, i[1], len(i[1]))
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"
    finally:
        if proc:
            proc.close_process()
    return "LEFT SHOULDER AIM OFF"

# ============================================
# RECOIL FUNCTIONS
# ============================================
def RemoveRecoil():
    try:
        proc = Pymem("HD-Player")
        if proc:
            value = pattern_scan_all(proc.process_handle, mkp("7a 44 f0 48 2d e9 10 b0 8d e2 02 8b 2d ed 08 d0 4d e2 00 50 a0 e1 10 1a 08 ee 08 40 95 e5 00 00 54 e3"), return_multiple=True)
            if value:
                for addr in value:
                    write_bytes(proc.process_handle, addr, bytes.fromhex("00 00"), 2)
        proc.close_process()
        return "No Recoil Enabled"
    except:
        return "Failed to remove recoil"


def AddRecoil():
    try:
        proc = Pymem("HD-Player")
        if proc:
            value = pattern_scan_all(proc.process_handle, mkp("00 00 f0 48 2d e9 10 b0 8d e2 02 8b 2d ed 08 d0 4d e2 00 50 a0 e1 10 1a 08 ee 08 40 95 e5 00 00 54 e3"), return_multiple=True)
            if value:
                for addr in value:
                    write_bytes(proc.process_handle, addr, bytes.fromhex("7a 44"), 2)
        proc.close_process()
        return "Recoil Restored"
    except:
        return "Failed to restore recoil"

# ============================================
# CHAMS FUNCTIONS (DLL Injection)
# ============================================
def box3d():
    process_name = "HD-Player.exe"
    try:
        temp_dll_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'BOX.dll')
        if os.path.exists(temp_dll_path):
            dll_path_bytes = bytes(temp_dll_path.encode('UTF-8'))
            open_process = Pymem(process_name)
            pymem.process.inject_dll(open_process.process_handle, dll_path_bytes)
            open_process.close_process()
            return "Box 3D Chams Enabled"
        else:
            return "BOX.dll not found"
    except Exception as e:
        return f"Error: {str(e)}"


def chamsmenu():
    process_name = "HD-Player.exe"
    try:
        temp_dll_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'charms_menu.dll')
        if os.path.exists(temp_dll_path):
            dll_path_bytes = bytes(temp_dll_path.encode('UTF-8'))
            open_process = Pymem(process_name)
            pymem.process.inject_dll(open_process.process_handle, dll_path_bytes)
            open_process.close_process()
            return "Chams Menu Enabled"
        else:
            return "charms_menu.dll not found"
    except Exception as e:
        return f"Error: {str(e)}"


def chams3d():
    process_name = "HD-Player.exe"
    try:
        temp_dll_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'wallfixedchams.dll')
        if os.path.exists(temp_dll_path):
            dll_path_bytes = bytes(temp_dll_path.encode('UTF-8'))
            open_process = Pymem(process_name)
            pymem.process.inject_dll(open_process.process_handle, dll_path_bytes)
            open_process.close_process()
            return "3D Chams Enabled"
        else:
            return "wallfixedchams.dll not found"
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================
# SNIPER FUNCTIONS
# ============================================
def SNIPERSCOPELOAD():
    try:
        proc = Pymem("HD-Player")
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"

    try:
        if proc:
            global sniperScopeAddress
            sniperScopePattern = mkp("CC 3D 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 3F 33 33 13 40 00 00 B0 3F 00 00 80 3F 01")
            sniperScopeAddress = pattern_scan_all(proc.process_handle, sniperScopePattern, return_multiple=True)
    except:
        pass
    finally:
        if proc:
            proc.close_process()
    return "Sniper Scope loaded"


def ACTIVATELOADEDSCOPE():
    try:
        proc = Pymem("HD-Player")
        if proc:
            global original_Scope_value
            original_Scope_value = []
            for addr in sniperScopeAddress:
                current_value = read_bytes(proc.process_handle, addr, 39)
                original_Scope_value.append(current_value)
                write_bytes(proc.process_handle, addr, bytes.fromhex("CC 3D 06 00 00 00 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 33 33 13 40 00 00 B0 3F 00 00 80 3F 01"), 39)
    except:
        pass
    finally:
        if proc:
            proc.close_process()
    return "Sniper Scope enabled"


def REMOVELOADEDSCOPE():
    try:
        proc = Pymem("HD-Player")
        if original_Scope_value:
            for i, original_val in enumerate(original_Scope_value):
                write_bytes(proc.process_handle, sniperScopeAddress[i], original_val, len(original_val))
    except:
        pass
    finally:
        if proc:
            proc.close_process()
    return "Sniper Scope disabled"


def SNIPERSWITCHLOAD():
    try:
        proc = Pymem("HD-Player")
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"

    try:
        if proc:
            global sniperSwitchAddress
            sniperSwitchPattern = mkp("B4 C8 D6 3F 00 00 80 3F 00 00 80 3F 0A D7 A3 3D 00 00 00 00 00 00 5C 43 00 00 90 42 00 00 B4 42 96 00 00 00 00 00 00 00 00 00 00 3F 00 00 80 3E 00 00 00 00 04 00 00 00 00 00 80 3F 00 00 20 41 00 00 34 42 01 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 80 3F 8F C2 35 3F 9A 99 99 3F 00 00 80 3F 00 00 00 00 00 00 80 3F 00 00 80 3F 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 00 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 80 3F")
            sniperSwitchAddress = pattern_scan_all(proc.process_handle, sniperSwitchPattern, return_multiple=True)
    except:
        pass
    finally:
        if proc:
            proc.close_process()
    return "Sniper Switch loaded"


def ACTIVATELOADEDSWITCH():
    try:
        proc = Pymem("HD-Player")
        if proc:
            global original_Switch_value
            original_Switch_value = []
            for addr in sniperSwitchAddress:
                current_value = read_bytes(proc.process_handle, addr, 148)
                original_Switch_value.append(current_value)
                write_bytes(proc.process_handle, addr, bytes.fromhex("B4 C8 D6 3F 00 00 80 3F 00 00 80 3F 0A D7 A3 3D 00 00 00 00 00 00 5C 43 00 00 90 42 00 00 B4 42 96 00 00 00 00 00 00 00 00 00 00 3C 00 00 80 3C 00 00 00 00 04 00 00 00 00 00 80 3F 00 00 20 41 00 00 34 42 01 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 80 3F 8F C2 35 3F 9A 99 99 3F 00 00 80 3F 00 00 00 00 00 00 80 3F 00 00 80 3F 00 00 80 3F 00 00 00 00 00 00 00 00 00 00 00 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 3F 00 00 80 3F"), 148)
    except:
        pass
    finally:
        if proc:
            proc.close_process()
    return "Sniper Switch enabled"


def REMOVELOADEDSWITCH():
    try:
        proc = Pymem("HD-Player")
        if original_Switch_value:
            for i, original_val in enumerate(original_Switch_value):
                write_bytes(proc.process_handle, sniperSwitchAddress[i], original_val, len(original_val))
    except:
        pass
    finally:
        if proc:
            proc.close_process()
    return "Sniper Switch disabled"

# ============================================
# WALLHACK FUNCTIONS
# ============================================
def WALLHACKLOAD():
    try:
        proc = Pymem("HD-Player")
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"

    pattern_hex = """AE 47 81 3F AE 47 81 3F AE 47 81 3F AE 47 81 3F 00 1A B7 EE DC 3A 9F ED 30"""
    try:
        global wallhack_addresses
        wall_pattern = mkp(pattern_hex)
        wallhack_addresses = pattern_scan_all(proc.process_handle, wall_pattern, return_multiple=True)
        if wallhack_addresses:
            return f"Wallhack loaded ({len(wallhack_addresses)} addresses)"
        else:
            return "No wallhack addresses found"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if proc:
            proc.close_process()


def ACTIVATEWALLHACK():
    try:
        proc = Pymem("HD-Player")
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"
    
    patch_hex = """00 00 EF C1 AE 47 81 3F AE 47 81 3F AE 47 81 3F 00 1A B7 EE DC 3A 9F ED 30"""
    try:
        global original_wall_bytes
        global wallhack_addresses
        original_wall_bytes = []
        if not wallhack_addresses:
            return "No wallhack addresses loaded"
        patch_hex_norm = _hex_normalize(patch_hex)
        patch_bytes = bytes.fromhex(patch_hex_norm)
        patch_len = len(patch_bytes)
        for addr in wallhack_addresses:
            orig = read_bytes(proc.process_handle, addr, patch_len)
            original_wall_bytes.append(orig)
            write_bytes(proc.process_handle, addr, patch_bytes, patch_len)
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if proc:
            proc.close_process()
    return "Wallhack enabled"


def REMOVEWALLHACK():
    try:
        proc = Pymem("HD-Player")
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"
    try:
        global original_wall_bytes
        global wallhack_addresses
        if not original_wall_bytes or not wallhack_addresses:
            return "No original bytes saved"
        for i, orig in enumerate(original_wall_bytes):
            write_bytes(proc.process_handle, wallhack_addresses[i], orig, len(orig))
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if proc:
            proc.close_process()
    return "Wallhack disabled"

# ============================================
# SPEED HACK FUNCTIONS
# ============================================
def SPEEDHACKLOAD():
    try:
        proc = Pymem("HD-Player")
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"

    try:
        global speedHackAddress
        speedPattern = mkp("00 01 00 00 00 02 2B 07 3D")
        speedHackAddress = pattern_scan_all(proc.process_handle, speedPattern, return_multiple=True)
        if speedHackAddress:
            return f"Speed Hack loaded ({len(speedHackAddress)} addresses)"
        return "No speed hack addresses found"
    finally:
        proc.close_process()


def ACTIVATELOADEDSPEED():
    try:
        proc = Pymem("HD-Player")
        global original_Speed_value
        original_Speed_value = []
        for addr in speedHackAddress:
            current_value = read_bytes(proc.process_handle, addr, 9)
            original_Speed_value.append(current_value)
            write_bytes(proc.process_handle, addr, bytes.fromhex("00 01 00 00 00 92 E4 50 3D"), 9)
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"
    finally:
        proc.close_process()
    return "Speed hack enabled"


def REMOVESPEEDHACK():
    try:
        proc = Pymem("HD-Player")
        if original_Speed_value:
            for i, original_val in enumerate(original_Speed_value):
                write_bytes(proc.process_handle, speedHackAddress[i], original_val, 9)
    except pymem.exception.ProcessNotFound:
        return "HD-Player not running"
    finally:
        proc.close_process()
    return "Speed hack disabled"

# ============================================
# FLY HACK FUNCTIONS
# ============================================
def FLYHACKLOAD():
    try:
        proc = Pymem("HD-Player")
        global flyhack_addresses
        flyhack_addresses = []
        pattern = mkp("00 0A 84 ED 04 2A 32 EE 01 1F 02 F2 01 1A 84 ED")
        flyhack_addresses = pattern_scan_all(proc.process_handle, pattern, return_multiple=True)
        proc.close_process()
        return f"Fly Hack loaded ({len(flyhack_addresses)} addresses)"
    except:
        return "Failed to load Fly Hack"


def ACTIVATEFLYHACK():
    try:
        proc = Pymem("HD-Player")
        global original_fly_value
        original_fly_value = []
        for addr in flyhack_addresses:
            current = read_bytes(proc.process_handle, addr, 16)
            original_fly_value.append((addr, current))
            write_bytes(proc.process_handle, addr, bytes.fromhex("00 0A 84 ED 04 2A 32 EE 01 1F 02 F2 01 1A 84 ED"), 16)
        proc.close_process()
        return "Fly Hack enabled"
    except:
        return "Failed to enable Fly Hack"


def REMOVEFLYHACK():
    try:
        proc = Pymem("HD-Player")
        for addr, orig in original_fly_value:
            write_bytes(proc.process_handle, addr, orig, len(orig))
        proc.close_process()
        return "Fly Hack disabled"
    except:
        return "Failed to disable Fly Hack"

# ============================================
# ANTENNA / NO GRASS
# ============================================
def ANTENNAHACK():
    try:
        proc = Pymem("HD-Player")
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

# ============================================
// ... existing code ...
# ============================================
# INTERNAL AIMBOT CLASS (OOP)
# ============================================
_aimbot_internal_singleton = None

def get_aimbot_internal():
    global _aimbot_internal_singleton
    if _aimbot_internal_singleton is None:
        _aimbot_internal_singleton = AimbotInternalPro()
    return _aimbot_internal_singleton


class AimbotInternalPro:
    def __init__(self):
        self.proc = None
        self.aimbot_addresses = []
        self.original_values = []
    
    def connect(self):
        try:
            self.proc = Pymem("HD-Player")
            return True
        except pymem.exception.ProcessNotFound:
            return False
    
    def disconnect(self):
        if self.proc:
            self.proc.close_process()
            self.proc = None
    
    def pattern_scan(self, pattern, return_multiple=True):
        if not self.proc:
            return None
        return pymem.pattern.pattern_scan_all(self.proc.process_handle, pattern, return_multiple=return_multiple)
    
    def read_memory(self, address, size):
        if not self.proc:
            return None
        return pymem.memory.read_bytes(self.proc.process_handle, address, size)
    
    def write_memory(self, address, value):
        if not self.proc:
            return False
        pymem.memory.write_bytes(self.proc.process_handle, address, value, len(value))
        return True
    
    def mkp(self, aob: str):
        if '??' in aob:
            if aob.startswith("??"):
                aob = f" {aob}"
                n = aob.replace(" ??", ".").replace(" ", "\\x")
                b = bytes(n.encode())
            else:
                n = aob.replace(" ??", ".").replace(" ", "\\x")
                b = bytes(f"\\x{n}".encode())
            return b
        else:
            m = aob.replace(" ", "\\x")
            return bytes(f"\\x{m}".encode())
    
    def load_aimbot(self):
        if not self.connect():
            return "HD-Player not running"
        try:
            entity_pattern = self.mkp("FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF FF FF FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 00 00 00 00 00 00 00 00 00 00 00 00 A5 43")
            self.aimbot_addresses = self.pattern_scan(entity_pattern)
            if self.aimbot_addresses:
                return f"Aimbot loaded ({len(self.aimbot_addresses)} addresses)"
            return "No aimbot addresses found"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            self.disconnect()
    
    def head_aim_on(self):
        if not self.connect():
            return "HD-Player not running"
        try:
            self.original_values = []
            for current_entity in self.aimbot_addresses:
                self.original_values.append((current_entity, self.read_memory(current_entity + 0xA6, 4)))
                value_bytes = self.read_memory(current_entity + 0xAA, 4)
                self.write_memory(current_entity + 0xA6, value_bytes)
            return "HEAD AIM ON"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            self.disconnect()
    
    def head_aim_off(self):
        if not self.connect():
            return "HD-Player not running"
        try:
            if self.original_values:
                for addr, original_val in self.original_values:
                    self.write_memory(addr + 0xA6, original_val)
            return "HEAD AIM OFF"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            self.disconnect()
    
    def right_shoulder_aim_on(self):
        if not self.connect():
            return "HD-Player not running"
        try:
            self.original_values = []
            for current_entity in self.aimbot_addresses:
                self.original_values.append((current_entity, self.read_memory(current_entity + 0xA6, 4)))
                value_bytes = self.read_memory(current_entity + 0xDA, 4)
                self.write_memory(current_entity + 0xA6, value_bytes)
            return "RIGHT SHOULDER AIM ON"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            self.disconnect()
    
    def left_shoulder_aim_on(self):
        if not self.connect():
            return "HD-Player not running"
        try:
            self.original_values = []
            for current_entity in self.aimbot_addresses:
                self.original_values.append((current_entity, self.read_memory(current_entity + 0xA6, 4)))
                value_bytes = self.read_memory(current_entity + 0xD6, 4)
                self.write_memory(current_entity + 0xA6, value_bytes)
            return "LEFT SHOULDER AIM ON"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            self.disconnect()
    
    def shoulder_aim_off(self):
        return self.head_aim_off()
