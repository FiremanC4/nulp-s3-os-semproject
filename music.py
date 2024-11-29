from playsound import playsound
import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def run_background_music():
    file = 'soundtrack.mp3'
    playsound(resource_path(file))
    
if __name__ == '__main__':
    run_background_music()