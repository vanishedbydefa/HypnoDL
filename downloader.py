from video import *
from flags import run_specific, run_category
import argparse
import pathlib
import time

api_domain = "hypnotube.com"

argParser = argparse.ArgumentParser()
argParser.add_argument("-p", "--path", type=pathlib.Path, help="path to the download folder")
argParser.add_argument("-q", "--quality", default="High", choices=["High","Low"], help="Choose quality (default: High)")
argParser.add_argument("-a", "--amount", type=int, default=1, help="Amount of recent videos to download (default: 1)")
argParser.add_argument("-c ", "--category", type=str, default="", help="Specify category to download Videos from")
argParser.add_argument("-o ", "--organize", type=bool, default=True, choices=[True, False], help="Organize downloaded videos to folder named like the category of the video")
argParser.add_argument("-f", "--force", type=bool, default=False, choices=[True, False], help="Download, even when already downloaded (default: False)")
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
category = args.category
organize = args.organize
force = args.force
specific = args.specific
tube = args.tube
if tube != "":
    api_domain = str(tube)

api_resp = req.get("https://" + api_domain + "/api/?output=json&command=media.newest&type=videos&offset=0&amount=" + str(amount)).json()["data"]
print("Welcome to HypnoDL")
print("[*] Configuring")
set_path(str(path))
set_quality(quality)

if get_used() == "True":
    print("    -> Last time used HypnoDL: " + get_date())
else:
    print("    -> HypnoDL was never used until now")
    set_used("True")
set_date(str(datetime.datetime.now()))
con = connect_db()

if specific != "":
    run_specific(specific, path, quality, force)
    exit(1)

if category != "":
    run_category(category, path, quality, force, api_domain, organize, con)
    exit(1)
    

print("    Info: Will download <= " + str(amount) + " videos")
print("[*] Fetching necessary information (this can take some time)")
to_download = get_all_informations(api_resp)
print("[*] Downloading the following titles: ")
for i in range(amount):
    print("    -> " + to_download[i][1])
    if i == 5:
        print("       ...")
        break
downloader(to_download, organize, path, con, force, quality)
