# HypnoDL
A simple downloader for Hypnotube.com and video platforms that use Tube Script

## Feature
* Download up to 250 of the latest videos
* Download a specific video
* All features also work for other websites that use Tube Script

## Usage
```
usage: downloader.py [-h] [-p PATH] [-q {High,Low}] [-a AMOUNT] [-c  CATEGORY] [-o  {True,False}] [-f {True,False}] [-s SPECIFIC] [-t TUBE]

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  path to the download folder
  -q {High,Low}, --quality {High,Low} Choose quality (default: High)
  -a AMOUNT, --amount AMOUNT Amount of recent videos to download (default: 1)
  -o {True,False}, --organize {True,False} Organize downloaded videos to folder named like the category of the video
  -f {True,False}, --force {True,False} Download, even when already downloaded (default: False)
  -s SPECIFIC, --specific SPECIFIC Download a specific Video from URL of the Site
  -t TUBE, --tube TUBE  Use HypnoDL for another Website that's using TUBE SCRIPT. Enter Domain e.x: hypnotube.com
  ```
  
  ### Example
  * Download last 10 videos `downloader.py -p S:/HypnoTube Downloader/downloads -a 10`
  * Download a specific video: `downloader.py -p S:/HypnoTube Downloader/downloads -s https://hypnotube.com/video/example-video1.html`
  * Download a specific video of a different platform thats also using Tube Script: `downloader.py -t example.com -p S:/HypnoTube Downloader/downloads -s https://example.com/video/example-video1.html`
