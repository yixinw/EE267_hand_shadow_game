## setup logging
import logging
logging.basicConfig(level = logging.INFO)

## import the package
import pyrealsense as pyrs
from PIL import Image
import matplotlib.pyplot as plt
import IPython
import numpy as np
import cv2
import time
import image_preprocessing
import socket
import pickle
from data_collection import collect_images

# Start the camera.
pyrs.start()
dev = pyrs.Device()

cnt = 0
last = time.time()
smoothing = 0.9;
fps_smooth = 30

# Fetch the images. hand_shadow_list is a list of 480x640 images
# (numpy array). edges_list is a list of 60x80 images (numpy array).
dir_path = '.'
hand_shadow_list, edges_list = collect_images(dir_path, ['scissors', 'spock', 'crab', 'dog', 'stag'])
total_num_shadows = len(hand_shadow_list)

# Player level.
level = 0
is_shadow_complete = False
# score threshold to pass
threshold = [0.9, 0.85, 0.8, 0.8, 0.8]

# If the user would like to render camera and processed images.
render = False

# Prepare the socket.
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()
# s.setblocking(0)

while True:

    cnt += 1
    if (cnt % 10) == 0:
        now = time.time()
        dt = now - last
        fps = 10/dt
        fps_smooth = (fps_smooth * smoothing) + (fps * (1.0-smoothing))
        last = now

    dev.wait_for_frame()
    colour = dev.colour
    c = cv2.cvtColor(colour, cv2.COLOR_RGB2BGR)
    depth = dev.dac * dev.depth_scale * 1000
    d = cv2.applyColorMap(depth.astype(np.uint8), cv2.COLORMAP_HSV)
    hand_image_raw = image_preprocessing.detect_hand(colour, depth)
    # hand_image_raw = image_preprocessing.detect_hand_sample(colour, depth)
    hand_image = cv2.cvtColor(hand_image_raw.astype(np.uint8), cv2.COLOR_RGB2BGR)
    hand_image_small = cv2.resize(hand_image, (80,60))

    # Load ground truth hand shadow and contour.
    # Add hand shadow contour to hand image. Prepare for request.
    edges = edges_list[level]  # 60x80
    hand_shadow = hand_shadow_list[level]  # 480x640
    b = 0
    g = 0
    r = 255
    hand_image_small[:,:,0] += edges / 255 * b
    hand_image_small[:,:,1] += edges / 255 * g
    hand_image_small[:,:,2] += edges / 255 * r
    hand_image_small = np.minimum(hand_image_small, 255)

    # Compare user hand with ground truth.
    is_shadow_complete, score  = image_preprocessing.compare_hand_shadow(hand_image,
            hand_shadow, threshold[level])

    # Send out the frame.
    try:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            # Client has closed connection.
            print "connection closed."
            conn.close()
            conn, addr = s.accept()
        elif data.strip("\n\r").startswith('Hello, World!'):
            # level information called from client side
            level = int(data.strip("\n\r")[-1])
            if is_shadow_complete:
                # User has completed this level. Load next level.
                print "Request received at server side. \
                        Succeed."
                conn.send("Succeed")
            else:
                print "Request received at server side. \
                        Sending hand image."
                _, hand_image_png = cv2.imencode('.png',
                        hand_image_small)
                hand_image_string = hand_image_png.tostring()
                # convert int scores to string of size 2
                # fix the size of buffer (=2)
                if score >= 100:
                    score = 99
                elif score >= 10:
                    score_string = str(score)
                elif score < 0:
                    score_string = '00'
                else:
                    score_string = '0' + str(score)
                assert len(score_string) == 2
                conn.send(score_string + hand_image_string)
        else:
            print "Received garbage:", data
    except socket.error:
        print "socket error"
        pass

    if render:
        cd = np.concatenate((c,d), axis=1)
        cv2.putText(cd, str(fps_smooth)[:4], (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0))

        cv2.imshow('', cd)
        cv2.imshow('hand', hand_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

pyrs.stop()

