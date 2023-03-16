import cv2
import pandas as pd
from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip
import mutagen
import os

#import get_video_points
path_video = 'C:/Users/123/Desktop/НЕЙРОСЕТЬ/Парез/videos/Патология/'
path_points = 'C:/Users/123/Desktop/НЕЙРОСЕТЬ/Парез/points/Патология/'
k = 0
while k < len(os.listdir(path_video)):

    name = os.listdir(path_video)[k]

    video_full_file_name = path_video + name

    cap = cv2.VideoCapture(video_full_file_name)
    reader = pd.read_csv(path_points + os.listdir(path_points)[k])

    video = mutagen.File(video_full_file_name)
    clip = VideoFileClip(video_full_file_name)
    clip.audio.write_audiofile('output_audio.mp3')
    audio = AudioFileClip('output_audio.mp3')

    audio.write_audiofile('output_audio1.mp3', fps=44100, bitrate=str(video.info.bitrate))
    audio = AudioFileClip('output_audio1.mp3')

    success, img0 = cap.read()
    height = img0.shape[0]
    width = img0.shape[1]
    FPS = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter("output.mp4", -1, FPS, (width, height))
    i = -1

    while True:
        success, img = cap.read()

        if success == True:
            i = i + 1

            if reader['frame_validity'][i] == 'valid':

                for j in range(3, len(reader.loc[0, :]), 2):
                    cv2.circle(img, (int(reader.loc[i][j]), int(reader.loc[i][j + 1])), 3, (0, 0, 255), thickness=cv2.FILLED)

            out.write(img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif i == len(reader.loc[:]) - 1:
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    video = VideoFileClip("output.mp4")
    clip = video.set_audio(audio)
    clip.write_videofile('C:/Users/123/Desktop/НЕЙРОСЕТЬ/' + 'new_' + str(name), fps=FPS, codec="libx264")
    k += 1
os.remove("output.mp4")
os.remove("output_audio.mp3")
os.remove("output_audio1.mp3")