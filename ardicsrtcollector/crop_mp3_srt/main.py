"""
It is main.py which is using to check the crop_mp3_srt.py file
"""

import argparse
from crop_mp3_srt import CropMp3Srt
import os
from ardicsrtcollector.helper.helper import is_url_valid

def main():
    
    """
    Usage: python3 main.py -path PATH_OF_MP3_AND_SRTFILE
                -start "00:00:02" -end "00:02:00"
    """
    parser = argparse.ArgumentParser(description='MP3 and text file cutting '
                                                 'according to the given '
                                                 'time period.')
    parser.add_argument("-path", '--path', type=str, required=True,
                        help="Path of mp3 and srt files which are "
                             "going to cut ")

    args = parser.parse_args()
    print(args)
    if args.path is None:
        print(" # -Please give a path of the mp3 and srt files.'")
    else:
        print(args.path)
        CropMp3Srt(filepath=args.path).crop()


if __name__ == '__main__':
    main()
