from tkinter import simpledialog, messagebox
from hashlib import sha256
import winreg as wrg 

_PROGRAM_NAME = 'MySupperProgram'
_LICENSE_KEY = '4eb007276d92ffcaa700cb422a5ea927e41ad0979cc91d5e0373baea04012e5a' # 'ilovecandy :)' in sha256.hex

def check_license():
    folder = _create_folder_if_not_exist()
    
    key = _read_reg_key(folder)
    if key is None or _check_key(key) == False:
        if key is not None:
            _del_reg_key(folder)
            
        new_key = _user_input_key()
        _write_reg_key(folder, new_key)
    
    if folder: wrg.CloseKey(folder) 

def _create_folder_if_not_exist():
    try:
        return wrg.OpenKeyEx(wrg.HKEY_CURRENT_USER,f"SOFTWARE\\{_PROGRAM_NAME}\\",0,wrg.KEY_SET_VALUE)
    except FileNotFoundError:
        folder = wrg.OpenKeyEx(wrg.HKEY_CURRENT_USER, r"SOFTWARE\\")
        folder = wrg.CreateKey(folder, _PROGRAM_NAME) 
        return folder
        
def _check_key(in_key):
    sha_key = sha256(in_key.encode('utf-8')).hexdigest()
    return sha_key == _LICENSE_KEY
        
def _read_reg_key(folder):
    folder = wrg.OpenKeyEx(wrg.HKEY_CURRENT_USER,f"SOFTWARE\\{_PROGRAM_NAME}\\")
    
    try:
        return wrg.QueryValueEx(folder, "license key")[0]
    except FileNotFoundError:
        return None
    finally:
        wrg.CloseKey(folder) 

def _user_input_key():
    while True:
        answer = simpledialog.askstring("license", "Enter your license key")
        if answer is None:
            quit()
        if _check_key(answer):
            messagebox.showinfo('Success', 'The program activated!')
            return answer
        messagebox.showerror("Error", "Wrong key!")
    
def _del_reg_key(folder):
    wrg.DeleteValue(folder, 'license key')

def _write_reg_key(folder, key):
    wrg.SetValueEx(folder, 'license key', 0, wrg.REG_SZ, key)

if __name__ == '__main__':
    check_license()
    print('Passed!')