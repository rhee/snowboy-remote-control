import snowboydecoder
import sys
import signal
import requests

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
    print "[next]", requests.get("https://gc-airi-demo.keyma.kr/simple-remote/next")

def callback_back():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    print "[back]", requests.get("https://gc-airi-demo.keyma.kr/simple-remote/back")



models = [ '../resources/k-next.pmdl', '../resources/k-back.pmdl' ]
detector = snowboydecoder.HotwordDetector(models, sensitivity = [0.44] * len(models))
callbacks = [ callback_next, callback_back ]

print('Listening... Press Ctrl+C to exit')


# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()