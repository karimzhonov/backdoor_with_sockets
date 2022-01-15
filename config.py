import os
import pyautogui
import numpy as np
import socket
import cv2
import pickle
import sys
from threading import Thread

LOCAL_IP = '127.0.0.1'
GLOBAL_IP = '0.0.0.0'
MAIN_PORT = 55555
WEBCAM_PORT = 55556
DESKTOP_PORT = 55557
WEBCAM_MODE = 'webcam'
DESKTOP_MODE = 'desktop'
STOP_STREAM_STATUS = 'stop_stream'
QUIT_STREAM = 'q'
CONTROLLER_WEBCAM = '--stream-webcam'
CONTROLLER_DESKTOP = '--stream-desktop'
