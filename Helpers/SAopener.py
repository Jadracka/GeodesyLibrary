import os
import subprocess
import time
import winreg

import psutil
import wmi

# License Key Dongle USB Vendor & Product IDs
DONGLE_VID = 0x04B9
DONGLE_PID = 0x0300


class SAException(Exception):
    """Errors related to our Spatial Analyzer integration"""


def _is_dongle_present():
    wmi_inst = wmi.WMI()
    devices = wmi_inst.Win32_PnPDevice()
    device_ids = [dev.SystemElement.DeviceID for dev in devices]

    for devid in device_ids:
        if f"VID_{DONGLE_VID:04X}&PID_{DONGLE_PID:04X}" in devid:
            return True


def _get_SApath_registry():
    try:
        # Open the registry key
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\New River Kinematics\Spatial Analyzer\Log",
        )

        # Read the registry value
        value, _ = winreg.QueryValueEx(key, r"EXE Path")

        # Close the registry key
        winreg.CloseKey(key)

        return value

    except Exception:
        return None


def _start_program(program_path, timeout=6):
    try:
        subprocess.Popen(
            [program_path],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return False

    # Wait for the program to start (you might need to adjust the delay)
    time.sleep(timeout)

    program_name = os.path.basename(program_path)
    return _is_program_running(program_name)


def _is_program_running(program_name):
    for proc in psutil.process_iter(attrs=["name"]):
        if proc.name == program_name:
            return True

    return False


def start_SA():
    if not _is_dongle_present():
        raise SAException("SA Hardware key has not been found, is it plugged in?")

    path = _get_SApath_registry()

    if path is None:
        raise SAException("It seems the SA is not installed on this computer.")

    program_name = os.path.basename(path)

    if not _is_program_running(program_name):
        if not _start_program(path):
            raise SAException("SA did not start or an error occurred")


if __name__ == "__main__":
    start_SA()
