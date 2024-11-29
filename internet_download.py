from requests import get as r_get
from requests.exceptions import ConnectionError
from tkinter import messagebox as mBox
from pathlib import Path

_AGREEMENT_URL = 'https://raw.githubusercontent.com/FiremanC4/nulp-s3-os-semproject/refs/heads/master/user_agreement.txt'

def _get_user_agreement():
    try:
        r = r_get(_AGREEMENT_URL)
    except ConnectionError:
        mBox.showerror('No internet connection', 'Unable to download user agreement')
        return None
    
    return r.text

def _save_file(content):
    path = Path.home() / 'Downloads'
    return path
    

if __name__ == "__main__":
    print(_get_user_agreement())
    print(_save_file('a'))