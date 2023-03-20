import requests as req
import re

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
    video_urls = get_video_urls(video_website_urls)
    for i in range(len(website_content)):
        information[i].append(video_id[i])
        information[i].append(video_title[i])
        information[i].append(video_website_urls[i])
        information[i].append(video_thumbnail_urls[i])
        information[i].append(video_urls[i])
    return information

def get_specific_title(video_website_url):
    title = req.get(video_website_url).text.split("title", 3)
    return title[1][1:-23]
