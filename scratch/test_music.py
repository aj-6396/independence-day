import ctypes
import os
import time

filepath = "data/bg_music.mp3"
abs_path = os.path.abspath(filepath)
print("Abs Path:", abs_path)

try:
    # Open the file
    open_cmd = f'open "{abs_path}" type mpegvideo alias bgmusic'
    r1 = ctypes.windll.winmm.mciSendStringW(open_cmd, None, 0, None)
    
    # Play the file looped from 0:50 (50000 ms)
    play_cmd = 'play bgmusic from 50000 repeat'
    r2 = ctypes.windll.winmm.mciSendStringW(play_cmd, None, 0, None)
    
    print(f"Open status: {r1}, Play status: {r2}")
    if r1 == 0 and r2 == 0:
        print("Music started successfully at 0:50! Playing for 5 seconds...")
        time.sleep(5)
    else:
        print(f"Failed to play. Open error code: {r1}, Play error code: {r2}")
        
    # Close it
    close_cmd = 'close bgmusic'
    ctypes.windll.winmm.mciSendStringW(close_cmd, None, 0, None)
    print("Music closed.")
except Exception as e:
    print("Error occurred:", e)
