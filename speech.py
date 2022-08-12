from pydub import AudioSegment
import librosa
from librosa import feature
import matplotlib.pyplot as plt
import numpy as np 
import wave 
import matplotlib.pyplot as plt
import soundfile as sf
from scipy import signal
from scipy.io import wavfile
import os
import os.path
from os import path
from pathlib import Path


PATH =  "downloads_convert\\"
PATH_WAV = "downloads_convert_wav\\"
SILENCE_PATH = "downloads_convert_wav_silence"
MP3 = ".mp3"

def convert_wav(VIDEO_ROOT, VIDEO_NAME):
    all_path = VIDEO_ROOT + VIDEO_NAME
    mp3_to_wav = AudioSegment.from_mp3(all_path)

    if not os.path.exists(PATH_WAV):
       os.mkdir(PATH_WAV)
    
    split_video_path = all_path.split("\\")
    VIDEO_ID = (split_video_path[1])



    id_len = len(VIDEO_NAME)
    VIDEO_NAME  = VIDEO_NAME[:id_len-4]
    if not os.path.exists(PATH_WAV + "\\" + VIDEO_ID):
      os.mkdir(PATH_WAV + VIDEO_ID)
    
    if not os.path.exists(PATH_WAV + VIDEO_ID +"\\"+VIDEO_NAME +".wav"):
        mp3_to_wav.export(PATH_WAV + VIDEO_ID +"\\"+VIDEO_NAME +".wav", format = "wav")

    return PATH_WAV + VIDEO_ID +"\\"+VIDEO_NAME +".wav",VIDEO_NAME ##returns the root and name of the current audio mp3 file 


def crop_silence(audio_file, VIDEO_ID):
    time_series, sr = librosa.load(audio_file)
    mse = feature.rms(y=time_series, frame_length=2048, hop_length=512)[0]
    mse_db = librosa.power_to_db(mse, top_db=None)

    percentage_of_silence = 0.1     
    noise_db = -3       

    threshold =int(np.percentile(mse_db, percentage_of_silence) + noise_db)
    clip = librosa.effects.trim(time_series, top_db=abs(threshold))
    
    path_list = audio_file.split("\\")
    cropped_video = str(path_list[1])

    if not os.path.exists(SILENCE_PATH):
        os.mkdir(SILENCE_PATH)

    new_path = SILENCE_PATH + "\\" + cropped_video
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    
    new_path = SILENCE_PATH +"\\"+ cropped_video +"\\"+  VIDEO_ID+"_without_silence.wav"
    if not os.path.exists(new_path):
        sf.write( new_path, clip[0], sr)


for root,dirs,files in os.walk(PATH, topdown=False):
    for files_dir in files:
        if MP3 in files_dir:
            audio_with_silence,video_id = convert_wav(root + "\\", files_dir)
            crop_silence(audio_with_silence, video_id)
    break
            
            






