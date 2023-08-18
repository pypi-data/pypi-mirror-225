import threading
from PIL import Image
import numpy
import pyvirtualcam
import sounddevice
import argparse
import os
import logging

frames_path = os.path.dirname(__file__) + "/freddy_frames"

parser = argparse.ArgumentParser(
    description="Replaces your camera with Withered Freddy that talks while you're talking",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    prog="python -m freddy_camera",
)
    
parser.add_argument('-d', '--device', type=str, help="the camera device to use", default=None)
parser.add_argument('-b', '--backend', type=str, help="the camera backend to use", default=None)
parser.add_argument('-s', '--sensitivity', type=float, help="the sensitivity of the microphone", default=0.5)
parser.add_argument('-r', '--resolution-multiplier', type=float, help="restriction: cannot be greater than 1", default=1)
parser.add_argument('--debug', action="store_true", help="whether the debug logging is enabled or not")
parser.set_defaults(debug=False)

args = parser.parse_args()

if args.resolution_multiplier > 1:
    raise Exception("resolution multiplier cannot be greater than 1")

if args.debug:
    log_level = logging.DEBUG
else:
    log_level = logging.WARNING

logging.basicConfig(format="%(asctime)s;%(levelname)s;%(message)s", level=log_level)

def block():
    threading.Event().wait()

width, height = Image.open(f"{frames_path}/1.png").size
width, height = int(width * args.resolution_multiplier), int(height * args.resolution_multiplier)

frames = [
    numpy.array(
        Image.open(f"{frames_path}/{frame_num}.png").resize((width, height))
    )
    for frame_num in range(1, 7)
]

CHECK_INTERVAL = 0.1

with pyvirtualcam.Camera(width=width, height=height, fps=round(1 / CHECK_INTERVAL), device=args.device, backend=args.backend) as cam:
    logging.debug("Connected the camera using the device %s!", cam.device)
    last_index = 0
    cam.send(frames[last_index])

    def process_sound(indata, _frames, _time, _status):
        global last_index
        volume_norm = numpy.linalg.norm(indata)
        index = int(float(volume_norm) * args.sensitivity)
        if index > last_index:
            index = last_index + 1
            if index == len(frames):
                index -= 1
        elif index < last_index:
            index = last_index - 1
        if index != last_index:
            last_index = index
            logging.debug("Changing the frame to %s!", index)
            cam.send(frames[index])

    sounddevice.InputStream(callback=process_sound, latency=CHECK_INTERVAL).start()
    block()
