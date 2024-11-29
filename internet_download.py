from requests import get as r_get
from requests.exceptions import ConnectionError
from tkinter import messagebox as mBox
from pathlib import Path

_AGREEMENT_URL = 'https://raw.githubusercontent.com/FiremanC4/nulp-s3-os-semproject/refs/heads/master/user_agreement.txt'
agr_text = ''

def _get_user_agreement():
    try:
        r = r_get(_AGREEMENT_URL)
    except ConnectionError:
        return None
    
    return r.text

def _save_file(content):
    global agr_text
    agr_text = content
    path = Path.home() / 'Downloads' / 'My Super Puper Program User Agreement.txt'
    with open(path, "w") as f:
        f.write(content)

def _check_file_validaty():
    path = Path.home() / 'Downloads' / 'My Super Puper Program User Agreement.txt'
    try:
        with open(path, "r") as f:
            content = f.read()
        return content == agr_text
    except FileNotFoundError:
        return False
    

def _download_user_agreement():
    agreement = _get_user_agreement()
    if agreement:
        _save_file(agreement)
        return True
    else:
        mBox.showerror('No internet connection', 'Unable to download user agreement')
        return False

def _ask_user_for_agreement():
    if not _download_user_agreement():
        return False
    
    res = mBox.askyesno('User agreement', 'Please accept the user agreement\nUser agreement located at download folder')\
    
    if res:  
        if _check_file_validaty():
            return True
        else:
            mBox.showerror('User agreement corrupted', 'The downloaded user agreement is not valid')
            return False
    return False

def force_user_to_accept_user_agreement():
    agrement = _ask_user_for_agreement()
    if agrement is False:
        quit()

if __name__ == "__main__":
    print(force_user_to_accept_user_agreement())