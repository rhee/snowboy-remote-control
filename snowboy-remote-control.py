# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from os import path
import signal
import requests
import json

import time
from threading import Thread, Lock

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

ws_port = 4004
ws_lock = Lock()
websockets = {}

class SimpleRemoteControl(WebSocket):
    def handleConnected(self):
        print("ws: connected:",self.address)
        with ws_lock:
            websockets[self] = True
    def handleMessage(self):
        print("ws: message:",self.address,self.data)
        # self.sendMessage(self.data)
        pass
    def handleClose(self):
        print("ws: close:",self.address)
        with ws_lcok:
            del websockets[self]
        pass

ws = SimpleWebSocketServer('', ws_port, SimpleRemoteControl)

def ws_serve():
    print ('ws: listening:', ws_port)
    ws.serveforever()

t = Thread(target=ws_serve, args=())
t.start()

#from linux import snowboydecoder
from osx import snowboydecoder

config = {}
#base_dir = path.join(path.dirname(path.abspath(__file__)),'..')
base_dir = path.dirname(path.abspath(__file__))

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
    #print ("[next]", requests.get(config['url'] + "/next"))
    with ws_lock:
        # 주의: u'' 로 보내지 않으면 blob 타입으로 보냄
        print ("[next]", [ ws.sendMessage(u'next') for ws in websockets ])

def callback_back():
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    #print ("[back]", requests.get(config['url'] + "/back"))
    with ws_lock:
        # 주의: u'' 로 보내지 않으면 blob 타입으로 보냄
        print ("[back]", [ ws.sendMessage(u'back') for ws in websockets ])


models = [
  path.join(base_dir,'resources','k-next.pmdl'),
  path.join(base_dir,'resources','k-back.pmdl')
]

sensitivity = [
  0.35,
  0.42
]

detector = snowboydecoder.HotwordDetector(models, sensitivity = sensitivity)
callbacks = [ callback_next, callback_back ]

print('Listening... Press Ctrl+C to exit')


# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
sys.exit(0)
