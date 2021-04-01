# ArdicSrtCollector

[![MIT license](http://img.shields.io/badge/license-Apache-brightgreen.svg?style=flat)](https://opensource.org/licenses/Apache-2.0) 
[![Python](https://img.shields.io/pypi/pyversions/ardicsrtcollector.svg?style=plastic)](https://badge.fury.io/py/ardicsrtcollector)
[![PyPI](https://badge.fury.io/py/ardicsrtcollector.svg)](https://badge.fury.io/py/ardicsrtcollector)

ArdicSrtCollector has been developed to generate the Turkish speech recognition dataset. As parameters, it takes a txt file consisting of the links of these Youtube videos and a folder name to store the files to be created. For each youtube video URL, it downloads the audio file,  extracts subtitles as the [SRT format](https://en.wikipedia.org/wiki/SubRip), and saves as two new files to the disk. Then it cropped (using [FFMPEG](https://www.ffmpeg.org)) the audio file according to the start and end time of each subtitle and creates a new audio file, and at the same time saves the current subtitle as a new txt file. 


### Installation

1. Install [ffmpeg](https://www.ffmpeg.org/).(it is re)
2. Run `$ pip install ardicsrtcollector`.

### Usage 

#### 1- From the terminal
```$ ardicsrtcollector -h
ardicsrtcollector [-h] [-sv SAVE_PATH] -ufp URL_FILE_PATH

To convert the Youtube URL to mp3 and srt file.

optional arguments:
  -h, --help            show this help message and exit
  -sv SAVE_PATH, --save_path SAVE_PATH
                        Path to save converted files (default: downloads_convert)
  -ufp URL_FILE_PATH, --url_file_path URL_FILE_PATH
                        A file which contains youtube URLs
```

##### Example
 Run on terminal :```ardicsrtcollector -ufp urls.txt```

#### 2- Using it by importing as a package like the one below. 

``` 
from ardicsrtcollector.youtube_srt_mp3 import YoutubeSrtMp3

YoutubeSrtMp3(urls_file_path="urls.txt", save_dir="save_path").convert()
```

### The content of the file containing the URLs should be as follows.

```
https://www.youtube.com/watch?v=ENwtC8LgPcw
https://www.youtube.com/watch?v=ENwtC8LgPcw
...
````

## License

[Apache License 2.0](LICENSE)
