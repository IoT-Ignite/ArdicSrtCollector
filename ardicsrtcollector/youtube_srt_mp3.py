"""
This is a file which performs conversions
"""
import os
import datetime
import sys
from youtube_transcript_api import YouTubeTranscriptApi
import youtube_dl
from .crop_mp3_srt.crop_mp3_srt import CropMp3Srt
from .helper.helper import progress, create_folder, is_url_valid


class YoutubeSrtMp3:
    """
     This class takes a file path which contains all youtube URLs,
     and gets mp3, and creates srt files for each youtube URL.
    """

    def __init__(self, save_dir='downloads_convert', urls_file_path=""):
        self._save_dir = save_dir
        self._url_file_path = None if urls_file_path == "" else urls_file_path
        self._ydl_opts = None
        self._video_title = ""
        self._video_id = ""
        self.path = ""
        # create a folder with the given folder name
        create_folder(self._save_dir)

        # times to calculate
        self.hour_ms = 3600000
        self.min_ms = 60000
        self.sec_ms = 1000

    def convert(self):
        """
        it's a public function that performs main task
        -checking a file that contains URLs for empty
        -read all lines in the file
        -each line is a youtube URL to get mp3 and srt file
        """
        if self._url_file_path is None:
            print("Please give a url file path.")
        else:
            try:
                _filesize = os.path.getsize(self._url_file_path)
            except:
                print("!!! Invalid file path !!!")
                sys.exit(0)

            if _filesize == 0:
                print("The %s is empty." % self._url_file_path)
            else:
                # read line from the file and convert it
                file1 = open(self._url_file_path, 'r')
                lines = file1.readlines()
                # print("LINES DATA:\n{}".format(lines))
                for line in lines:
                    # print(line.strip()+"*")
                    youtube_url = line.strip()

                    # check youtubeurl is valid or not
                    # if it is valid, convert to mp3, srt file
                    # print info to screen and continue
                    res = False

                    if is_url_valid(youtube_url):
                        # self.__check_url_is_available(youtube_url)
                        print("The URL is okay.")

                        res = self.get_mp3_srt(line)
                    else:
                        print('!# %s is not valid url' % youtube_url)
                if res is True:
                    print(
                        "\033[0;32;49mDownloading and cropping are DONE!\033[0m")

    def __set_file_details(self, video_url):
        """
        get video information
        """
        ydl_opt = self.__set_video_download_options(True)
        with youtube_dl.YoutubeDL(ydl_opt) as ydl:
            info_dict = ydl.extract_info(video_url, False)
            self._video_id = info_dict.get("id", None)

            temp_name = info_dict.get('title', None)
            if ':' in temp_name:
                split_word = temp_name.split(':')
                self._video_title = split_word[0] + ' -' + split_word[1]
            else:
                self._video_title = temp_name

    def get_mp3_srt(self, youtube_url):
        """
           convert video url to mp3 and srt file.
           1-convert  to mp3 and save video details(or extract video details)
        """
        self.__set_file_details(youtube_url)
        # convert to mp3
        self.__url_to_mp3(youtube_url)

        # convert to srt file with the video title
        self.__url_to_srt_file()
        return True

    def __url_to_srt_file(self):
        srt = YouTubeTranscriptApi.get_transcript(
            self._video_id, languages=["tr", "en"])
        # Get the length of the all subtitles
        _len_of_all_srt = len(srt)

        try:
            get_transcripts = YouTubeTranscriptApi.list_transcripts(
                self._video_id)
            transcript = get_transcripts.find_manually_created_transcript([
                                                                          'tr', 'en'])
            print(transcript)
        except:
            print('\n\033[2;31;43m !!!! WARNING !!!! \033[0;0m')
            x = ""
            while not x == "q":
                print(
                    '\n\033[2;31;43mThis transcript is not manually created. Press "q" to continue cropping, "e" to exit. \033[0;0m \n')
                x = input()
                if x == "q":
                    print(
                        "\033[2;37;42mContinue to cropping auto-generated subtitle \033[0;0m\nvideo ID = %s " % self._video_id)
                elif x == "e":
                    print("Exiting the program...")
                    sys.exit(-1)
                else:
                    print("\033[2;31;43m !!! Invalid Entrance !!! \033[0;0m\n")

                    # BURASI DEGISTIRILDI
        # Create a path of the srt file to save it
        path = self._save_dir + '/' + self._video_id
        print("PATH {}".format(path))

        # Create a folder if the path doesnt exit
        create_folder(path)
        filepath = path + "/" + self._video_id + ".srt"

        # create an object to crop mp3 and srt files
        save_each_subtitle = CropMp3Srt(path)
        with open(filepath, 'w+') as new_srt_file_write:
            add_sec = 0
            # from 0 to 373 if the len of the subtitle is 375

            for cur_idx in range(0, _len_of_all_srt):
                progress(percent=cur_idx, delim=_len_of_all_srt, )
                # print(srt[cur_idx])
                # GET current SUBTITLE
                current_subtitle = srt[cur_idx].get('text')

                # START POINT
                s_time = srt[cur_idx].get("start") + add_sec
                start_time_str = str(self.milliseconds_to_time(s_time))

                # END POINT
                # the end point of the current subtitle will be
                # the start time of the second subtitle
                _dur_time_str = ""
                _line_after_subs = ""
                if cur_idx != _len_of_all_srt - 1:  # index if smaller than 374
                    dur_time = srt[cur_idx + 1].get("start")
                    # compare between the duration of the current time
                    # and the second subtitle start time
                    # get the current time duration
                    cur_sub_dur = srt[cur_idx].get("duration") + s_time
                    the_next_sub_start_time_of = srt[cur_idx + 1].get("start")
                    # diff_time = the_next_sub_start_time_of - cur_sub_dur
                    add_sec = 0
                    _dur_time_str = str(self.milliseconds_to_time(
                        the_next_sub_start_time_of))
                    _line_after_subs = "\n\n"
                else:
                    dur_time = srt[cur_idx].get("duration")
                    _dur_time_str = str(self.milliseconds_to_time(dur_time
                                                                  + s_time))
                    _line_after_subs = "\n"
                new_srt_file_write.write(str(cur_idx + 1) + "\n" +
                                         start_time_str + " --> " +
                                         _dur_time_str + "\n"
                                         + current_subtitle + _line_after_subs)

                save_each_subtitle.onetime_save_cropped_mp3_srt(self._video_id,
                                                                cur_idx + 1,
                                                                current_subtitle,
                                                                start_time_str,
                                                                _dur_time_str)
            new_srt_file_write.close()
            print("\n")
            return

    def __url_to_mp3(self, youtube_url):
        self._ydl_opts = self.__set_video_download_options(is_info=False)
        self.path = self._save_dir + self._video_id
        directories = os.listdir(self._save_dir)  # BURASI ##
        if self._video_id in directories:     # Prevent a video from downloading more than once
            print("This directory already exist")
        else:
            with youtube_dl.YoutubeDL(self._ydl_opts) as ydl:
                # download video and convert to mp3
                ydl.download([youtube_url])
            # extract video information's

    def __set_video_download_options(self, is_info):
        return {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': self._save_dir + '/%(id)s.%(ext)s' if is_info is True else self._save_dir +
            '/%(id)s/%(id)s.%(ext)s',

        }

    def milliseconds_to_time(self, millis_time):
        """
        it is a func. which convert ms to time as 00:15:15.25
        """
        millis_time = millis_time * 1000
        # print("millis_time:{}".format(millis_time))

        start_hh = int(millis_time / self.hour_ms)
        if start_hh > 0:
            current = millis_time - (start_hh * self.hour_ms)
        else:
            current = millis_time
        # print("current to min:{}".format(current))
        start_mm = int(current / self.min_ms)

        if start_mm > 0:
            current = current - (start_mm * self.min_ms)

        start_ss = int(current / self.sec_ms)

        if start_ss > 0:
            current = current - (start_ss * self.sec_ms)

        current = current % self.sec_ms

        milli_sec = current
        # print("Curr:{},{},{},{}".format(start_hh,
        # start_mm, start_ss, current))
        start_time = datetime.time(start_hh, start_mm, start_ss)
        if milli_sec >= 100:
            result_time = "{},{}".format(start_time, int(milli_sec))
        elif milli_sec < 100 and milli_sec >= 10:
            result_time = "{},{}{}".format(start_time, "0", int(milli_sec))
        else:
            result_time = "{},{}{}".format(start_time, "00", int(milli_sec))
        return result_time
