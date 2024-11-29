from check_license import check_license
from graffic import opengl_3d_cube
from music import run_background_music

import threading

def main():
    check_license()
    
    threads = [
        threading.Thread(target=opengl_3d_cube),
        threading.Thread(target=run_background_music),
    ]
    
    for thread in threads:
        thread.start()
        
    for thread in threads:
        thread.join()
    
if __name__ == '__main__':
    main()