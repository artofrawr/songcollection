from __future__ import unicode_literals
import yaml
import youtube_dl
import requests
import argparse
import os
import urllib
import shutil
from PIL import Image
from StringIO import StringIO
from ffmpy import FFmpeg
from collections import OrderedDict

with open("config.yml", "r") as f:
    CONFIG = yaml.load(f)

HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
API_ROOT = 'http://ws.audioscrobbler.com/2.0/?api_key={0}&format=json&method='.format(CONFIG['api_key'])
COVER_SIZE = (816, 816)
COVER_POSITION = (132,134)


class SongCollector(object):

    def __init__(self, args):
        self.args = args
        self.ytID = args.youtube
        self.ytURL = 'http://www.youtube.com/watch?v=' + self.ytID
        self.title = args.title
        self.imageURL = args.image
        self.timestamp = args.start
        self.start()

    def start(self):
        self.download_song(self.ytID)
        self.download_cover()
        self.stitch_video()
        print("Done!")

    def stitch_video(self):
        '''Stitches together audio, cover art and background template.'''
        print '[video] stitching video'
        output_path = 'files/{0}.mp4'.format(self.title)

        input_mp3 = 'files/{0}.mp3'.format(self.title)
        input_jpg = 'files/{0}.jpg'.format(self.title)
        timestamp = 0 if self.timestamp is None else self.timestamp

        if os.path.isfile(output_path):
            os.remove(output_path)

        inputs = OrderedDict([('template/background.mp4', None), (input_jpg, None), (input_mp3, '-ss {0}'.format(timestamp))])

        ff = FFmpeg(
            inputs=inputs,
            outputs={output_path: [
                '-filter_complex', '[0:v][1:v] overlay={0}:{1}:enable=\'between(t,0,60)\''.format(COVER_POSITION[0],COVER_POSITION[1]),
                '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '256k',
                '-shortest'
            ]}
        )
        ff.run()

    def download_cover(self):
        '''Downloads cover art.'''

        # if we have not manually provided an image url, try to find one
        if self.imageURL is None:
            print '[cover art] trying to find cover art for: ' + self.title
            self.imageURL = self.search_cover()

            if self.imageURL is None:
                print '[cover art] couldn\'t find cover art'
                exit()


        # download the image
        print '[cover art] downloading: ' + self.imageURL
        r = requests.get(self.imageURL)
        i = Image.open(StringIO(r.content))
        i = i.resize(COVER_SIZE)
        i.save('files/{0}.jpg'.format(self.title), format='JPEG')

    def search_cover(self):
        '''Tries to find cover art via last.fm api based on song title.'''

        # first try to find the track using the track.search endpoint
        url = "{0}track.search&track={1}".format(API_ROOT, self.title)
        trackdata = requests.get(url, headers=HEADERS).json()
        tracks = trackdata['results']['trackmatches']['track']
        if len(tracks) == 0:
            return None

        # get more detailled data using track.getInfo endpoint
        for i in range(min(5, len(tracks))):
            artist = tracks[i].get('artist', '')
            trackname = tracks[i].get('name', '')
            url = "{0}track.getInfo&artist={1}&track={2}".format(API_ROOT, artist, trackname)
            r = requests.get(url, headers=HEADERS)
            result = r.json()
            if ('album' in result['track']):
                for image in result['track']['album']['image']:
                    if image['size'] == "extralarge":
                        return image['#text'].replace('300x300', '1200x1200')

        # if we couldn't find any album art using track.getInfo, fallback to artist imagery
        for i in range(min(5, len(tracks))):
            artist_images = tracks[i].get('image', [])
            for image in artist_images:
                if image['size'] == "extralarge":
                    return image['#text'].replace('300x300', '1200x1200')

        return None

    def download_song(self, ytID):
        '''Youtube Video -> MP3'''

        # store the YT title if we haven't manually provided a title
        if self.title is None:
            ydl = youtube_dl.YoutubeDL()
            result = ydl.extract_info(self.ytURL, download=False)
            self.title = result['title']

        # download YT video as mp3
        ydl = youtube_dl.YoutubeDL({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': "files/{0}.%(ext)s".format(self.title)
        })
        ydl.download([self.ytURL])



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--youtube', required=True, help='Youtube ID (e.g. "cthwJXKFEoU").')
    parser.add_argument('-t', '--title', help='Song title (e.g. "Muscles - Sweaty").')
    parser.add_argument('-i', '--image', help='Cover art image URL (e.g. "https://goo.gl/npDZ4o").')
    parser.add_argument('-s', '--start', help='Timestamp in seconds to start at (e.g. 72).')
    args = parser.parse_args()

    sc = SongCollector(args)

if __name__ == "__main__":
    main()
