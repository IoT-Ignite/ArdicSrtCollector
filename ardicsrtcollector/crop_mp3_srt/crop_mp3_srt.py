"""
It is a file that crops the mp3 and srt file by the durations
which is getting from the srt file.
"""
import os
from ..helper.helper import run_bash, parse_time


class CropMp3Srt:
    """
    Gets the mp3 and srt files to crop
    """

    def __init__(self, filepath):
        self._path = filepath

    def crop(self):
        """
        It is a public function which is used from the other packages or files
        to perform main purpose
        """
        dirs = os.listdir(self._path)
        for file in dirs:
            if not file.startswith("crop_"):
                if file.endswith(".srt"):
                    self._crop_mp3_srt(file)

    def _crop_mp3_srt(self, filename):
        # extract video_id from the filename
        _video_id = filename[:-4]
        # read from the given file.
        with open(self._path + "/" + filename, 'r') as _filehandle:
            _filecontent_list = _filehandle.readlines()

            # it starts at index one and increases at adding 4
            for line in range(1, len(_filecontent_list), 4):
                _current_sub_num = _filecontent_list[line - 1][:-1]

                # to split the times (start and end times)
                _split__current_times = _filecontent_list[line].split(' ')

                # crop mp3 by the current times
                # PARSE TIMES
                # before given time, the duration time will get
                # as _split__current_times[:-1],
                # because it has "\n"
                _current_start = parse_time(_split__current_times[0])
                _current_end = parse_time(_split__current_times[2])
                # CALL THE CROPPING MP3 func
                self._crop_mp3(_video_id, _current_sub_num,
                               _current_start, _current_end)

                # CALL the function which WILL SAVE THE CURRENT
                # SUBTITLE to the TXT FILE
                self._save_sub_txt(_video_id, _current_sub_num,
                                   _filecontent_list[line + 1])

    def onetime_save_cropped_mp3_srt(self, video_id, sub_id,
                                     current_sub, start_time, end_time):
        """
        Saves each cropped file and performing cropping of the mp3 file
        :param video_id: is the current video id
        which is using to save cropped files
        :param sub_id: is using for naming to save cropped files
        :param current_sub: it saves to the new cropped text file
        :param start_time: is used to crop the mp3 file
        :param end_time: is used to crop the mp3 file
        """
        _current_start = parse_time(start_time)
        _current_end = parse_time(end_time)
        self._crop_mp3(video_id, str(sub_id), _current_start, _current_end)
        self._save_sub_txt(video_id, str(sub_id), current_sub)

    def _save_sub_txt(self, video_id, sub_id, current_subtitle):
        _new_srt_name = self._path + "/" + video_id\
                        + "_crop_" + sub_id + ".txt"
        with open(_new_srt_name, 'w+') as new_cropped_file:
            new_cropped_file.write(current_subtitle)
        new_cropped_file.close()

    def _crop_mp3(self, video_id, sub_id, start_time, end_time):
        """
        video_id is the video id from the youtube
        sub_id is the index from the subtitle list
        start time the starting point to crop
        """
        input_filename = self._path + "/" + video_id + ".mp3"
        new_file_name = self._path + "/" + video_id+"_crop_" + sub_id + ".mp3"

        # -n means never override
        command = "ffmpeg -n -i " + input_filename + " -ss  " + \
                  start_time + " -to " + end_time + " -c copy " \
                  + new_file_name + " 2> /dev/null"

        run_bash(command)
