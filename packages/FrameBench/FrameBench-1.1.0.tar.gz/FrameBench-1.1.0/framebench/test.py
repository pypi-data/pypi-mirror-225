import threading
import hashlib
import time
import logging
import sys

import cv2
from PIL import Image

class CamTest:
    def __init__(self, cam: str, resolution = "640x480", framerate = 30, stream_format = "MJPG", test_time = 30):
        self.cam = cam
        self.resolution = resolution
        self.framerate = framerate
        self.stream_format = stream_format
        self.test_time = test_time

        self.results = [self.cam]
        self.ready = False
        self.logger = logging.getLogger(__package__)
        self.vid = self._setup_capture_device()

    def run(self):
        start_time = time.time()

        last_frame = (None, start_time) #checksum, time
        while time.time() - start_time < self.test_time:
            ret, frame = self.vid.read()
            frame_time = time.time()

            if not ret:
                self.logger.warn("Can't receive frame (stream end?).")
                continue

            #OpenCV brings frames in using BGR, convert it to RGB to prevent PIL from getting confused
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame)
            pil_chksum = hashlib.md5(pil_img.tobytes())
            
            if pil_chksum != last_frame[0]:
                if last_frame[0] != None: # Skip first frame, since camera initialization gives a large initial frame time
                    self.results.append((frame_time - last_frame[1]) * 1e3)
                last_frame = (pil_chksum, frame_time)
            
        self.vid.release()

    def get_result(self):
        return self.results

    def _setup_capture_device(self):
        (width, _, height) = self.resolution.partition("x")
        
        vid = cv2.VideoCapture(self.cam)
        
        vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self.stream_format))
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, int(width))
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, int(height))

        if not vid.isOpened():
            raise RuntimeError(f"Could not open {self.cam}")

        cv_resolution = f"{vid.get(cv2.CAP_PROP_FRAME_WIDTH)}x{vid.get(cv2.CAP_PROP_FRAME_HEIGHT)}"
        cv_fps = vid.get(cv2.CAP_PROP_FPS)
        cv_format = int(vid.get(cv2.CAP_PROP_FOURCC)).to_bytes(4, sys.byteorder).decode()

        self.logger.info(f"Opened {self.cam} at {cv_resolution} {cv_fps}fps using {cv_format} encoding")
        self.ready = True

        return vid
