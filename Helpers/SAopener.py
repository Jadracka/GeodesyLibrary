import os
import subprocess
import time
import psutil
import winreg
import wmi

def dongle_check():
#    VID = 0x04B9
#    PID = 0x0300
    wmi_inst = wmi.WMI()
    devices = wmi_inst.Win32_PnPDevice()
    device_ids = [dev.SystemElement.DeviceID for dev in devices]
    for devid in device_ids:
        if ("VID_" + "04B9" + "&PID_" + "0300") in devid:
            return True

def get_SApath_registry():
    try:
        # Open the registry key
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                             r"SOFTWARE\New River Kinematics\Spatial Analyzer\Log")

        # Read the registry value
        value, _ = winreg.QueryValueEx(key, r"EXE Path")

        # Close the registry key
        winreg.CloseKey(key)
        
        program_name = os.path.basename(value)
        return (value, program_name)
    except Exception as e:
        print("It seems the SA is not installed on this computer.")
        print(f"Error: {e}")
        del e, key, value, program_name
        return None


def start_program(program_path, timeout=6):
    try:
        subprocess.Popen(f'"{program_path}"', shell=True)

        time.sleep(timeout)  # Wait for the program to start (you might need to adjust the delay)

        program_name = os.path.basename(program_path)
        for proc in psutil.process_iter(attrs=['name']):
            if proc.info['name'] == program_name:
                return True  # Program started successfully

    except (subprocess.CalledProcessError, Exception):
        pass

    return False  # Program did not start or an error occurred

def is_program_running(program_name):
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] == program_name:
            return True
    return False

def start_SA():
    if not dongle_check():
        print("SA Hardware key has not been found, is it plugged in?")
    else:
        path, name = get_SApath_registry()
        if not is_program_running(name):
            start_program(path)
        if is_program_running(name):
            print("SA has been succesfully opened.")
    del path, name
    return True

start_SA()