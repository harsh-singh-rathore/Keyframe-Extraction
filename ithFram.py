import os
import cv2 as cv
from datetime import datetime

def iFrame(i : int, path):
    if os.path.isfile(path):
        if not os.path.isdir('keyframes'):
            os.mkdir('keyframes')


        iframe = 0

        cap = cv.VideoCapture(path)
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        filename = str(datetime.now().strftime('%b%d%y%H%M%S'))+str('.avi')
        frameDim = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
        out = cv.VideoWriter(os.path.join('keyframes',filename), fourcc, 24.0, frameDim)

        if not cap.isOpened():
            print("Can't open video")
            exit()


        while cap.isOpened():
            iframe += 1
            ret, frame = cap.read()

            if iframe%i == 0:
                out.write(frame)
    else:
        raise Exception("Can't find the file")


if __name__ == '__main__':
    iFrame(15, os.path.join("Footage", "Keyframe video.mp4"))
    print("Done!")
