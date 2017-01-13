# songcollection
A python script to create content for https://www.instagram.com/songcollection/

## Requirements:
* [homebrew](http://brew.sh)
* python, pip: ```brew install python```
* virtualenv: ```pip install virtualenv```
* ffmpeg: ```brew install ffmpeg```
* last.fm API key: http://www.last.fm/api

## Initial Setup:
To create a config file with your api key, create the virtual environment and install dependencies run:<br>`source setup.sh` <br/>

## Running the app:
1. Activate the virtual environment: ```source virtualenv/songcollection/bin/activate```<br>
2. Run the script: ```python app.py -y ErYAGQZs8e0```<br>

## Parameters:
|`parameter`|Required|Description|Example|
|-----------|--------|-----------|-------|
|-y <br>-youtube|**yes**|The youtube ID of the video.  |-y ErYAGQZs8e0|
|-t <br>-title|-|Manually specify the songtitle. <br>Default: Youtube Video Title |-t "SBTRKT - Pharaohs"|
|-i <br>-image|-|Manually specify the cover image url<br>Default: App will try to find one based on title.|-i https://goo.gl/2aoOEz|
|-s <br>-start|-|Starting point (in seconds).<br>Default: 0 seconds.|-s 30|
