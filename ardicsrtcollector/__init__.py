# __init__.py
"""
it is used for the setup.py
"""

import sys
import argparse
from ardicsrtcollector.youtube_srt_mp3 import YoutubeSrtMp3
import ardicsrtcollector.helper as package_version

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
                        help="A file which contains youtube URLs")

    args = parser.parse_args()

    if args.save_path is None:
        print(' # -Path of converted files set to '
              'default is \'downloads_convert\'')
        YoutubeSrtMp3(urls_file_path=args.url_file_path).convert()
    else:
        YoutubeSrtMp3(urls_file_path=args.url_file_path,
                      save_dir=args.save_path).convert()


if __name__ == '__main__':
    sys.exit(main())
