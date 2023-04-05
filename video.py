import requests as req
import re
import os
from status import *
from database import *
import datetime

def get_video_id(website_content):
    video_id = []
    for tags in website_content:
        for key, value in tags.items():
            if key == "id":
                video_id.append(value)
    return video_id

def get_video_title(website_content):
    video_title = []
    for tags in website_content:
        for key, value in tags.items():
            if key == "title":
                video_title.append(value)
    return video_title

def get_video_website_urls(website_content):
    video_urls= []
    for tags in website_content:
        for key, value in tags.items():
            if key == "url":
                video_urls.append(value)
    return video_urls

def get_video_thumbnail_urls(website_content):
    video_thumbnail_urls = []
    for tags in website_content:
        for key, value in tags.items():
            if key == "main_thumb":
                video_thumbnail_urls.append(value)
    return video_thumbnail_urls

def get_video_category(website_content):
    video_categorys = []
    for tags in website_content:
        for key, value in tags.items():
            if key == "channels":
                video_categorys.append(value)
    return video_categorys

def get_video_urls(video_website_urls):
    video_urls = [ [] for i in range(len(video_website_urls))]
    for i in range(len(video_website_urls)):

        url = req.get(video_website_urls[i]).text.split("<source", 3)
        url.pop(0)
        for j in range(len(url)):
            url[j] = url[j][:130]
            if ".avi" in url[j]:
                url[j] = re.sub(r'\.avi.*',"",url[j])[6:] + ".avi"
            elif ".m4v" in url[j]:
                url[j] = re.sub(r'\.m4v.*',"",url[j])[6:] + ".m4v"
            elif ".webm" in url[j]:
                url[j] = re.sub(r'\.webm.*',"",url[j])[6:] + ".webm"
            elif ".mkv" in url[j]:
                url[j] = re.sub(r'\.mkv.*',"",url[j])[6:] + ".mkv"
            elif ".mov" in url[j]:
                url[j] = re.sub(r'\.mov.*',"",url[j])[6:] + ".mov"
            elif ".MOV" in url[j]:
                url[j] = re.sub(r'\.MOV.*',"",url[j])[6:] + ".MOV"
            elif ".mpg" in url[j]:
                url[j] = re.sub(r'\.mpg.*',"",url[j])[6:] + ".mpg"
            elif ".mp4" in url[j]:
                url[j] = re.sub(r'\.mp4.*',"",url[j])[6:] + ".mp4"
            else:
                print(url[j])
                raise SystemExit("Error: video format is not avi, m4v, webm, mkv, mov, MOV, mpg, mp4. Couldn't generate correct url")
            video_urls[i].append(url[j])
    return video_urls

def get_all_informations(website_content):

    information = [ [] for i in range(len(website_content))]

    video_id = get_video_id(website_content)
    video_title = get_video_title(website_content)
    video_website_urls = get_video_website_urls(website_content)
    video_thumbnail_urls = get_video_thumbnail_urls(website_content)
    video_categorys = get_video_category(website_content)
    video_urls = get_video_urls(video_website_urls)
    for i in range(len(website_content)):
        information[i].append(video_id[i])
        information[i].append(video_title[i])
        information[i].append(video_website_urls[i])
        information[i].append(video_thumbnail_urls[i])
        information[i].append(video_categorys[i])
        information[i].append(video_urls[i])
    return information

def get_specific_title(video_website_url):
    title = req.get(video_website_url).text.split("title", 3)
    return title[1][1:-23]


def downloader(to_download, organize, path, con, force, quality):
    not_downloadable = False
    for i in range(len(to_download)-1,-1,-1):
        if len(to_download[i][5]) >= 2:
            if quality == "High":
                quality = 0
            else:
                quality = len(to_download[i][5])-1
        elif len(to_download[i][5]) == 1:
            quality = 0
        else:
            not_downloadable = True

        if not_downloadable == False:
            folder = str(to_download[i][4]).split(",",1)[0]
            if organize:
                if os.path.isdir(str(path) + "\\" + str(folder)) == False:
                    os.mkdir(str(path) + "\\" + str(folder))
                tmp_path = str(path) + "\\" + str(folder) + "\\"
            else:
                tmp_path = str(path) + "\\"
            
            to_download[i][1] = re.sub('[/<>:?|"*]', "", to_download[i][1]).replace("\\", "")
            if "avi" in to_download[i][5][quality]:
                tmp_path += str(to_download[i][1]) + ".avi"
            elif "mp4" in to_download[i][5][quality]:
                tmp_path += str(to_download[i][1]) + ".mp4"
            elif "webm" in to_download[i][5][quality]:
                tmp_path += str(to_download[i][1]) + ".webm"
            elif "m4v" in to_download[i][5][quality]:
                tmp_path += str(to_download[i][1]) + ".m4v"
            elif "mkv" in to_download[i][5][quality]:
                tmp_path += str(to_download[i][1]) + ".mkv"
            elif "mov" in to_download[i][5][quality]:
                tmp_path += str(to_download[i][1]) + ".mov"
            elif "MOV" in to_download[i][5][quality]:
                tmp_path += str(to_download[i][1]) + ".MOV"
            elif "mpg" in to_download[i][5][quality]:
                tmp_path += str(to_download[i][1]) + ".mpg"        
            entrys = request_db(con, str(to_download[i][0]))
            update_db = False
            if len(entrys) == 5:
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
                        print("File seems to not exist anymore")
                    update_db = True
            
            print("Donloading: " + to_download[i][1] + " [" + str(folder) + "]")
            r = req.get(to_download[i][5][quality], stream = True)
            with open(tmp_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024*1024):
                    if chunk:
                        f.write(chunk)
            f.close()
            insert_db(con, str(to_download[i][0]), to_download[i][2], str(path), str(datetime.datetime.now()), str(folder), update_db)
            set_last_id(to_download[i][0])
            print("Done [" + str(len(to_download)-i) + "/" + str(len(to_download)) + "]")
        else:
            print("    Info: Video < " + to_download[i][1] + " > cloudn't be downloaded!")
            print("       -> If you want to check access manually: " + to_download[i][2])
        not_downloadable = False
