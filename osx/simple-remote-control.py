import snowboydecoder
import sys
from os import path
import signal
import requests
import json

config = {}
base_dir = path.join(path.dirname(__file__),'..')

with open(path.join(base_dir,'config.json')) as config_json:
    config = json.load(config_json)

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

signal.signal(signal.SIGINT, signal_handler)



def callback_next():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
    print "[next]", requests.get(config['url'] + "/next")

def callback_back():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    print "[back]", requests.get(config['url'] + "/back")



models = [
  path.join(base_dir,'resources','k-next.pmdl'),
  path.join(base_dir,'resources','k-back.pmdl')
]

detector = snowboydecoder.HotwordDetector(models, sensitivity = [0.44] * len(models))
callbacks = [ callback_next, callback_back ]

print('Listening... Press Ctrl+C to exit')


# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
