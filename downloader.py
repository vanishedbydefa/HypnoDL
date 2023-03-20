import re
from status import *
from video import *
from database import *
from flags import run_specific
import argparse
import pathlib
import time
import datetime

api_domain = "hypnotube.com"

argParser = argparse.ArgumentParser()
argParser.add_argument("-p", "--path", type=pathlib.Path, help="path to the download folder")
argParser.add_argument("-q", "--quality", default="High", choices=["High","Low"], help="Choose quality (default: High)")
argParser.add_argument("-a", "--amount", type=int, default=1, help="Amount of recent videos to download (default: 1)")
argParser.add_argument("-f", "--force", type=bool, default=False, help="Download, even when already downloaded (default: False)")
argParser.add_argument("-s", "--specific", type=str, default="", help="Download a specific Video from URL of the Site")
argParser.add_argument("-t", "--tube", type=str, default="", help="Use HypnoDL for another Website that's using TUBE SCRIPT. Enter Domain e.x: hypnotube.com")
args = argParser.parse_args()
path = args.path

if not check_path(path) or path == None:
    if get_path() != "#":
        path = get_path()
        if not check_path(path) or path == None:
            raise SystemExit("Error: You need to specify a path") 
    else:
        raise SystemExit("Error: You need to specify a path")
quality = args.quality
amount = args.amount
if amount > 250:
    raise SystemExit("Too much videos to download in one run, maximum is 250")
if amount > 30:
    print(str(amount) +  " Videos will take a very long time to download\n")
    time.sleep(3)
force = args.force
specific = args.specific
tube = args.tube
if tube != "":
    api_domain = str(tube)

api_resp = req.get("https://" + api_domain + "/api/?output=json&command=media.newest&type=videos&offset=0&amount=" + str(amount)).json()["data"]
print("Welcome to HypnoDL")
print("[*] Configuring")
set_date(str(datetime.datetime.now()))
set_path(str(path))
set_quality(quality)

if get_used() == "True":
    print("    -> Last time used HypnoDL: " + get_date())
else:
    print("    -> HypnoDL was never used until now")
    set_used("True")
con = connect_db()

if specific != "":
    run_specific(specific, path, quality, force)
    exit(1)

print("    Info: Will download <= " + str(amount) + " videos")
to_download = get_all_informations(api_resp)
print("[*] Downloading the following titles: ")
for i in range(amount):
    print("    -> " + to_download[i][1])
    if i == 5:
        print("       ...")
        break

if quality == "High":
    quality = 1
else:
    quality = 2

not_downloadable = False
for i in range(len(to_download)-1,-1,-1):
    if len(to_download[i][4]) >= 2:
        if quality == "High":
            quality = 0
        else:
            quality = len(to_download[i][4])-1
    elif len(to_download[i][4]) == 1:
        quality = 0
    else:
        not_downloadable = True

    if not_downloadable == False:
        to_download[i][1] = re.sub('[/<>:?|"*]', "", to_download[i][1]).replace("\\", "")
        if "avi" in to_download[i][4][quality]:
            tmp_path = str(path) + "\\" + str(to_download[i][1]) + ".avi"
        elif "mp4" in to_download[i][4][quality]:
            tmp_path = str(path) + "\\" + str(to_download[i][1]) + ".mp4"
        elif "webm" in to_download[i][4][quality]:
            tmp_path = str(path) + "\\" + str(to_download[i][1]) + ".webm"
        elif "m4v" in to_download[i][4][quality]:
            tmp_path = str(path) + "\\" + str(to_download[i][1]) + ".m4v"
        elif "mkv" in to_download[i][4][quality]:
            tmp_path = str(path) + "\\" + str(to_download[i][1]) + ".mkv"
        elif "mov" in to_download[i][4][quality]:
            tmp_path = str(path) + "\\" + str(to_download[i][1]) + ".mov"
        elif "MOV" in to_download[i][4][quality]:
            tmp_path = str(path) + "\\" + str(to_download[i][1]) + ".MOV"
        elif "mpg" in to_download[i][4][quality]:
            tmp_path = str(path) + "\\" + str(to_download[i][1]) + ".mpg"        
        entrys = request_db(con, str(to_download[i][0]))
        update_db = False
        if len(entrys) == 4:
            if force == False:
                print("\n")
                print("WARNING: ")
                print("There already is an entry for this ID in the database [" + str(entrys[0]) + "]")
                print("Last time you downloaded this video to: " + entrys[2] + " on " + entrys[3])
                print("HypnoDL will try to check if the Video still exist in the old location")
            if os.path.isfile(tmp_path):
                if force == False:
                    print("File seems to still exist here: " + entrys[2] + "\\" + to_download[i][1])
                    print("HypnoDL will NOT download this video again.")
                    continue
            else:
                if force == False:
                    print("File seems to not exist anymore: " + entrys[2])
                update_db = True
        
        print("Donloading: " + to_download[i][1])
        r = req.get(to_download[i][4][quality], stream = True)
        with open(tmp_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    f.write(chunk)
        f.close()
        insert_db(con, str(to_download[i][0]), to_download[i][2], str(path), str(datetime.datetime.now()), update_db)
        set_last_id(to_download[i][0])
        print("Done [" + str(len(to_download)-i) + "/" + str(len(to_download)) + "]")
    else:
        print("    Info: Video < " + to_download[i][1] + " > cloudn't be downloaded!")
        print("       -> If you want to check access manually: " + to_download[i][2])
    not_downloadable = False
