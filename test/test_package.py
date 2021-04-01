import os
import random
from ardicsrtcollector.youtube_srt_mp3 import YoutubeSrtMp3

NUM_SUBTITLES = 193  # total number of the subtitles
TEST_SRT_FILE_PATH = "test/test_srt_file/Ot0vYkRT1Mg.srt"
DOWNLOAD_PATH = "test/test_downloads_cropped"
PATH_CROPPED_FILE = DOWNLOAD_PATH + "/Ot0vYkRT1Mg"
URLS_FILE_PATH = "test/urls.txt"


def read_test_srt_file():
    """
    to compare random subtitles
    """
    all_lines_in_srt = open(TEST_SRT_FILE_PATH, 'r').readlines()

    # To test random subtitle
    def _test_compare_random_subs():
        # generate random number to check 
        num_rand = random.randint(0, NUM_SUBTITLES)
        # get subtitle from the cropped file
        sub_from_the_random_txt_file = open(PATH_CROPPED_FILE + "/Ot0vYkRT1Mg_crop_"
                                            + str(num_rand) + ".txt").readlines()[0]

        # calculate the index of the random generated sub
        
        real_index = num_rand * 4 - 2
        if num_rand==0:
            real_index = 2
        

        # get random sub text from the real srt file
        real_random_sub = all_lines_in_srt[real_index][:-1]
        assert sub_from_the_random_txt_file == real_random_sub

    return _test_compare_random_subs()


def _download_crop_files():
    """
    it's  downloading and cropping files
    """
    YoutubeSrtMp3(urls_file_path=URLS_FILE_PATH, save_dir=DOWNLOAD_PATH).convert()


def test_total_number_of_cropped_files():
    """
    to test number rof files
    """
    total_num_mp3 = 0
    total_num_srt = 0
    for file in os.listdir(DOWNLOAD_PATH + "/Ot0vYkRT1Mg"):
        if file.endswith('.mp3'):
            total_num_mp3 += 1
        elif file.endswith('.txt'):
            total_num_srt += 1

    assert total_num_srt + total_num_mp3 == NUM_SUBTITLES * 2 + 1


if __name__ == '__main__':
    # test download and cropped files
    _download_crop_files()
    test_total_number_of_cropped_files()
    # test the random subtitle between real sub and downloaded file
    read_test_srt_file()
