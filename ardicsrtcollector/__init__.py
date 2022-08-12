# __init__.py
"""
it is used for the setup.py
"""

import sys
import argparse
from ardicsrtcollector.youtube_srt_mp3 import YoutubeSrtMp3
import ardicsrtcollector.helper as package_version
from ardicsrtcollector.helper.helper import is_url_valid, check_double_URL
import os 

# Version of the ardicsrtcollector package

__version__ = package_version.helper.VERSION


def main():
    """
    It is a helper function which checks arguments when its package is running
    """
    parser = argparse.ArgumentParser(description='To convert the Youtube URL'
                                                 'to mp3 and srt file.')
    parser.add_argument("-sv", '--save_path', type=str,
                        help="Path to save converted files"
                             "(default: downloads_convert)")
    parser.add_argument('-ufp', '--url_file_path', type=str,
                        required=True,
                        help="A file which contains youtube URLs or one valid youtube link only")

    args = parser.parse_args()

    if is_url_valid(args.url_file_path):
        """
        This if statement checks the url_file_path argument
        Checks the user's input of entering the valid url 
        instead of the file path.

        """
        print("The URL is okay.")
        if check_double_URL("videos.txt", args.url_file_path):
            print("URL saved into the videos.txt by default")
        else:   
            print(args.url_file_path +" this URL already exist in the given folder path")
        YoutubeSrtMp3(urls_file_path = "videos.txt").convert()
    else:
        if args.save_path is None:
            print(' # -Path of converted files set to '
                'default is \'downloads_convert\'')
            YoutubeSrtMp3(urls_file_path=args.url_file_path).convert()
        else:
            YoutubeSrtMp3(urls_file_path=args.url_file_path,
                        save_dir=args.save_path).convert()


if __name__ == '__main__':
    sys.exit(main())
