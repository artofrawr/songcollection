# songcollection
A python script to create content for https://www.instagram.com/songcollection/

## Requirements:
* [homebrew](http://brew.sh)
* python, pip: ```brew install python```
* virtualenv: ```pip install virtualenv```
* ffmpeg: ```brew install ffmpeg```

## Initial Setup:
To create the virtual environment and install dependencies: `source setup.sh` 

## Running the app:
Activate the virtual environment: <br>```source virtualenv/songcollection/bin/activate```<br>
<br>
Basic use: <br>```python app.py -y cthwJXKFEoU```<br>

## Parameters:
|`parameter`|Required|Description|Example|
|-----------|--------|-----------|-------|
|-y <br>-youtube|**yes**|The youtube ID of the video.  |-y cthwJXKFEoU|
|-t <br>-title|-|Manually specify the songtitle. <br>Default: Youtube Video Title |-t "Muscles - Sweaty"|
|-i <br>-image|-|Manually specify the cover image<br>Default: App will try to find one based on title.|-i files/cover.jpg|
|-s <br>-start|-|Starting point (in seconds).<br>Default: 0 seconds.|-s 72|
