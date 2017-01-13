from __future__ import unicode_literals
import yaml
import youtube_dl
import requests
import argparse
import urllib

with open("config.yml", "r") as f:
    CONFIG = yaml.load(f)

HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
API_ROOT = 'http://ws.audioscrobbler.com/2.0/?api_key={0}&format=json&method='.format(CONFIG['api_key'])

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def download_video(ytID):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['http://www.youtube.com/watch?v=' + ytID])


def track_search(artist, title):

	# url = "%strack.search&track=%s&%s" % (API_ROOT, title, API_KEY)
	url = "%strack.getInfo&artist=%s&track=%s" % (API_ROOT, artist, title)
	r = requests.get(url, headers=HEADERS)
	result = r.text
	print result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--artist', help='Artist name')
    parser.add_argument('-t', '--title', help='Song title')
    parser.add_argument('-v', '--video', help='Youtube ID')
    args = parser.parse_args()

    download_video(args.video)
    # track_search(args.artist, args.title)


if __name__ == "__main__":
    main()
