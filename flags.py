from status import *
from video import *
import requests
import time

def run_specific(specific, path, quality, force):
    print("Downloading a specific video started")
    if quality == "High":
        quality = 0
    else:
        quality = len(to_download[1]-1)

    to_download = get_video_urls([specific])
    to_download.insert(0,get_specific_title(specific))
    if "avi" in to_download[1][quality]:
        tmp_path = str(path) + "\\" + str(to_download[0]) + ".avi"
    elif "mp4" in to_download[1][quality]:
        tmp_path = str(path) + "\\" + str(to_download[0]) + ".mp4"
    elif "m4v" in to_download[1][quality]:
        tmp_path = str(path) + "\\" + str(to_download[0]) + ".m4v"
    elif "mkv" in to_download[1][quality]:
        tmp_path = str(path) + "\\" + str(to_download[0]) + ".mkv"
    elif "mov" in to_download[1][quality]:
        tmp_path = str(path) + "\\" + str(to_download[0]) + ".mov"
    elif "MOV" in to_download[1][quality]:
        tmp_path = str(path) + "\\" + str(to_download[0]) + ".MOV"   
    
    if force == False:
        if os.path.isfile(tmp_path):
            print("Video already downloaded")
            exit(1)
    
    print("Donloading: " + to_download[0])
    r = requests.get(to_download[1][quality], stream = True)
    with open(tmp_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024*1024):
            if chunk:
                f.write(chunk)
    print("Done")  
    f.close()
    return
