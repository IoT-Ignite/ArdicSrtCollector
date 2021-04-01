"""
Helper functions
"""
import os

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


def is_url_valid(youtube_url):
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
