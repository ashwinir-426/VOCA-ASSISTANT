import os
import eel 
import threading
from wakeword import htwrd

from engine.features import*
from engine.command import*

def start():
    eel.init("www")
    # playAssistantSound()
    
    t1 = threading.Thread(target=htwrd)
    t1.daemon = True
    t1.start()

    eel.start('index.html', mode='chrome', host='localhost', block=True)

start()