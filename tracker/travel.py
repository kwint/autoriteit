import asyncio
import os
import time

from alive_progress import alive_bar
from PIL import Image
from playsound import playsound
from websockets.sync.client import ClientConnection, connect

ESPS =[
    "192.168.178.184",
    "192.168.178.185",
    "192.168.178.186",
    "192.168.178.187",
    "192.168.178.188",
    "192.168.178.190",
]

logo = """
                  _                _  _         _  _   
     /\          | |              (_)| |       (_)| |  
    /  \   _   _ | |_  ___   _ __  _ | |_  ___  _ | |_ 
   / /\ \ | | | || __|/ _ \ | '__|| || __|/ _ \| || __|
  / ____ \| |_| || |_| (_) || |   | || |_|  __/| || |_ 
 /_/    \_\\__,_| \__|\___/ |_|   |_| \__|\___||_| \__|
                                                       
"""
def clear_print_logo():
    os.system('clear')
    print(logo)

def stop():
    [ws.send("STOP") for ws in WSC]

def dance():
    [ws.send(f"CON&{1000}") for ws in WSC]
    time.sleep(.5)
    [ws.send(f"CON&{-1000}") for ws in WSC]
    time.sleep(1)
    [ws.send(f"CON&{1000}") for ws in WSC]
    time.sleep(1)
    [ws.send(f"CON&{-1000}") for ws in WSC]
    time.sleep(0.5)
    stop()


    
    
clear_print_logo()
img = Image.open("fomo.png")


WSC = []
for esp in ESPS:
    try:
        ws_connection = connect(f"ws://{esp}/ws", open_timeout=1)
        WSC.append(ws_connection)
    except Exception:
        print(f"{esp}")

stop()


playsound('teleporting.mp3', block=False)
dance()

x = 150
with alive_bar(x, title="Verbinden met Autoriteit machines") as bar:
    [ws.send("CON&1000") for ws in WSC]
    for i in range(x):
        time.sleep(0.01)
        bar()

[ws.send("STOP") for ws in WSC]
time.sleep(3)
clear_print_logo()


last_time = time.time()
for title, style, speed, itr in [("Klokken calibreren", "bubbles", -1000, 500)]:
    with alive_bar(itr, title=title, title_length=25, bar=style) as bar:
        [ws.send(f"CON&{speed}") for ws in WSC]
        for i in range(itr):
            time.sleep(0.01)
            bar()
            if time.time() - last_time > 0.5:
                last_time = time.time()
                speed = speed * -1
                [ws.send(f"CON&{speed}") for ws in WSC]

            
    [ws.send("STOP") for ws in WSC]

time.sleep(3)

for title, style, speed, itr in [("Localiseren Tijdkristal", "fish", 1400, 2000)]:
    with alive_bar(itr, title=title, title_length=25, bar=style) as bar:
        [ws.send(f"CON&{speed}") for ws in WSC]
        for i in range(itr):
            time.sleep(0.01)
            bar()
            speed_ramp = speed * (i/itr)
            if speed_ramp % 10 == 0:
                [ws.send(f"CON&{speed_ramp * -1}") for ws in WSC]


        time.sleep(2)

dance()

[ws.send(f"CON&{-250}") for ws in WSC]
os.system('CACA_DRIVER=ncurses mplayer -quiet -vo caca ./radar.mp4')
os.system('ffplay -fs -autoexit ./wereld.mp4')
[ws.send("STOP") for ws in WSC]

clear_print_logo()


clear_print_logo()

print("Tijdkristal gelokaliseerd")
time.sleep(3)

# Kristal teleporteren
for title, style, speed, itr in [("Klokken uitlijnen met kirstal", "fish", -1400, 2000)]:
    step = itr / (len(WSC) + 1)
    threshold = 0.0
    clock_nr = 0
    WSC[clock_nr].send(f"CON&{speed}") 

    with alive_bar(itr, title=title, title_length=50, bar=style) as bar:
        for i in range(itr):
            time.sleep(0.01)
            bar()
            if i > threshold and clock_nr < len(WSC):
                threshold += step
                WSC[clock_nr].send(f"CON&{speed}") 
                clock_nr += 1

for title, style, speed, itr in [("Kristal teleporteren", "fish", -1400, 2000)]:
    [ws.send(f"CON&{speed}") for ws in WSC]

    with alive_bar(itr, title=title, title_length=25, bar=style) as bar:
        for i in range(itr):
            time.sleep(0.01)
            bar()

time.sleep(1)

img.show()

[ws.send("STOP") for ws in WSC]

[ws.close() for ws in WSC]

time.sleep(100)