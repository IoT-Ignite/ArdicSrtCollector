"""
Helper functions
"""
from hashlib import new
import sys
import os
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IRWXO, S_IRWXU
from xmlrpc.client import Boolean

VERSION = "1.0.14"


def get_seconds(time_str):
    """Get Seconds from time."""
    hour, minutes, seconds = time_str.split(':')
    return int(hour) * 3600 + int(minutes) * 60 + int(seconds)


def run_bash(command):
    """
    It is a helper function to run a given command
    :param command: to run by the OS
    """
    os.system(command)


def parse_time(time):
    """
    PARSING a given TIME to FFMPEG format
    """
    _temp_time_split = time.split(',')
    _new_time = _temp_time_split[0] + "."
    if "\n" in _temp_time_split[1]:
        _new_time += _temp_time_split[1][:-1]
    else:
        _new_time += _temp_time_split[1]
    return _new_time


def create_folder(folder_name):
    """
    if the folder doesnt create. it is creating
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def is_url_valid(youtube_url) -> bool:
    """
    Checks a given url is valid or not
    :param youtube_url: is URL
    :return: True if the URL is valid, otherwise False
    """
    if "https://www.youtube.com/watch?v=" not in youtube_url:
        return False
    return True


def progress(percent=0, delim=100, width=30):
    """
    To show progress in the screen
    """
    left = width * percent // delim + 20
    right = width - left + 18
    print('\rCropping files: [', '#' * left, ' ' * right, ']',
          f' {percent:.0f} ', sep='', end='', flush=True)


def is_file_Empty(filepath) -> bool:
    with open(filepath, "r") as file:
        if os.stat(filepath).st_size == 0:
            return True
        else:
            return False


def check_double_URL(url_file_path, youtube_url) -> bool:
    """
    Write youtube urls with given argument into the default videos.txt file
    Read-only mode is set in the end of this function so users do not change directly 
    """
    try:
        if not os.path.exists(url_file_path):
            with open(url_file_path, "w") as file:
                file.write(youtube_url + "\n")
        else:
            os.chmod(url_file_path, S_IRWXU | S_IRGRP |
                     S_IROTH)  # read-write-execute
            with open(url_file_path, "w") as file:
                file.write(youtube_url + "\n")

        file.close()
        os.chmod(url_file_path, S_IREAD | S_IRGRP | S_IROTH)  # read-only
    except:
        print("!!! Permission Error !!!")
        sys.exit(0)

    return True
