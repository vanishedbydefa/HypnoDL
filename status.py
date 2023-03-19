from video import *
import json
import os

def get_config():
  with open('config.json', 'r') as stat:
    data = json.load(stat)
    stat.close()
  return data

def get_used():
  return get_config()["used"]

def get_date():
  return get_config()["date"]

def get_quality():
  return get_config()["quality"]

def get_path():
  return get_config()["path"]

def get_last_id():
  return get_config()["last_id"]

def set_used(content: bool):
    data = get_config()
    data["used"] = content
    with open('config.json', 'w') as config:
      json.dump(data, config)

def set_date(content: int):
    data = get_config()
    data["date"] = content
    with open('config.json', 'w') as config:
      json.dump(data, config)

def set_quality(content: str):
    data = get_config()
    data["quality"] = content
    with open('config.json', 'w') as config:
      json.dump(data, config)

def set_path(content: list):
    data = get_config()
    data["path"] = content
    with open('config.json', 'w') as config:
      json.dump(data, config)

def set_last_id(content: int):
    data = get_config()
    data["last_id"] = content
    with open('config.json', 'w') as config:
      json.dump(data, config)


def check_path(path):
    if path == None:
        return os.path.isdir(get_path())
    else:
        return os.path.isdir(path)
    
def get_amount_to_download(website_content,amount):
    ids = get_video_id(website_content, amount)
    amount_to_download = 0
    id = get_last_id()
    if id != "#":
        for i in range(len(ids)):
            if str(id) == ids[i]:
                amount_to_download = i
                break
            else:
               return amount
    else:
        amount_to_download = amount
    return amount_to_download 