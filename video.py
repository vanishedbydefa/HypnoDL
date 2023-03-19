import requests as req
import re

def get_video_id(website_content, amount):
    video_id = website_content.split('"id":"', amount+1)
    video_id.pop(0)
    for i in range(len(video_id)):
        video_id[i] = re.sub(r'title.*', "", video_id[i])[:-3]
    return video_id

def get_video_title(website_content, amount):
    video_title = website_content.split('"title":"', amount+1)
    video_title.pop(0)
    for i in range(len(video_title)):
        video_title[i] = re.sub(r'length.*', "", video_title[i])[:-3]
    return video_title

def get_video_website_urls(website_content, amount):
    video_website_urls = website_content.split('"url":"', amount+1)
    video_website_urls.pop(0)
    for i in range(len(video_website_urls)):
        video_website_urls[i] = re.sub(r'\.html.*',"",video_website_urls[i]).replace("\\", "") + ".html"
    return video_website_urls

def get_video_thumbnail_urls(website_content, amount):
    video_thumbnail_urls = website_content.split('"main_thumb":"', amount+1)
    video_thumbnail_urls.pop(0)
    for i in range(len(video_thumbnail_urls)):
        video_thumbnail_urls[i] = re.sub(r'\.jpg.*',"",video_thumbnail_urls[i]).replace("\\","") + ".jpg"
    return video_thumbnail_urls

def get_video_urls(video_website_urls):
    video_urls = [ [] for i in range(len(video_website_urls))]
    for i in range(len(video_website_urls)):

        url = req.get(video_website_urls[i]).text.split("source", 3)
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
            elif ".mp4" in url[j]:
                url[j] = re.sub(r'\.mp4.*',"",url[j])[6:] + ".mp4"
            else:
                print(url[j])
                raise SystemExit("Error: video format is not avi, m4v, webm, mkv, mov, MOV, mp4. Couldn't generate correct url")
            video_urls[i].append(url[j])
    return video_urls

def get_all_informations(website_content, amount):

    information = [ [] for i in range(amount)]

    video_id = get_video_id(website_content, amount)
    video_title = get_video_title(website_content, amount)
    video_website_urls = get_video_website_urls(website_content, amount)
    video_thumbnail_urls = get_video_thumbnail_urls(website_content, amount)
    video_urls = get_video_urls(video_website_urls)
    for i in range(amount):
        information[i].append(video_id[i])
        information[i].append(video_title[i])
        information[i].append(video_website_urls[i])
        information[i].append(video_thumbnail_urls[i])
        information[i].append(video_urls[i])
    return information

def get_specific_title(video_website_url):
    title = req.get(video_website_url).text.split("title", 3)
    return title[1][1:-23]
