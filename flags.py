from status import *
from video import *
import requests
from bs4 import BeautifulSoup
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
    elif "mpg" in to_download[1][quality]:
        tmp_path = str(path) + "\\" + str(to_download[0]) + ".mpg"   
    
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

def get_categorys(domain):
    home = req.get("https://" + domain + "/channels/").text
    soup = BeautifulSoup(home, 'html.parser')
    soup = soup.find_all("a", class_="has-counter")
    
    categorys = []
    for i in range(len(soup)):
        categorys.append([soup[i]["title"], soup[i]["href"]])   
    return categorys

def run_category(category, path, quality, force, domain, organize, con):
    categorys = get_categorys(domain)
    for i in categorys:
        if str(category) == str(i[0]):
            cat_url = i[1]
            break
        elif category != i[0] and i == categorys[len(categorys)-1]:
            print("\nYour entered category do not match any valid category")
            print("Enter a category like: " + categorys[0][0])
            exit(1)
    for p in range(1,10000):
        print("[*] Fetching necessary information (this can take some time)")
        website_urls = []
        cat_home_stat = req.get(cat_url+ "/page" + str(p) + ".html")
        if str(cat_home_stat) == "<Response [200]>":
            print("    Info: downloading page: " + str(p))
        else:
            print("Url wasn't recheable - page: " + str(p) + " wasn't downloaded")
            exit(1)
        cat_home = cat_home_stat.text.split('class="inner-box-container"',1)[1].split('<nav class="pagination-col col pagination"',1)[0]
        soup = BeautifulSoup(cat_home, 'html.parser')
        soup = soup.find_all(class_="item-inner-col inner-col")
        
        print("    Info: Processing fetched informations")
        to_download = []
        for i in range(len(soup)):
            website_urls.append(str(soup[i]).split('href="')[1].split('" title="')[0])
            video_id = re.findall(r'\d+',str(website_urls[i]))
            video_id = video_id[len(video_id)-2]
            to_download.append([video_id])
            to_download[i].append(get_specific_title(website_urls[i]))
            to_download[i].append(website_urls[i])
            to_download[i].append("thumbnail not downloadable")
            to_download[i].append(category)
            to_download[i].append(get_video_urls([website_urls[i]])[0])
            
        print("[*] Downloading videos")  
        downloader(to_download, organize, path, con, force, quality)
        if len(to_download) < 20:
            exit(1)
