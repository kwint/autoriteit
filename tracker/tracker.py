import asyncio
import os
import time

from alive_progress import alive_bar
from PIL import Image
from websockets.sync.client import ClientConnection, connect

ESPS =[
    "192.168.178.184",
    "192.168.178.185",
    "192.168.178.186",

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

clear_print_logo()
img = Image.open("fomo.png")

WSC = []
for esp in ESPS:
    try:
        ws_connection = connect(f"ws://{esp}/ws", open_timeout=1)
    except Exception:
        print(f"{esp}")

    WSC.append(ws_connection)

x = 150
with alive_bar(x, title="Verbinden met tijd machines") as bar:
    [ws.send("CON&1000") for ws in WSC]
    for i in range(x):
        time.sleep(0.01)
        bar()
        
time.sleep(3)
clear_print_logo()


for title, style, speed, itr in [("Klokken calibreren", "bubbles", 1000, 500), ("Meten van tijd", "fish", -1000, 500), ("Tijdreiziger tracken", "ruler2", 1200, 1000)]:
    with alive_bar(itr, title=title, title_length=25, bar=style) as bar:
        [ws.send(f"CON&{speed}") for ws in WSC]
        for i in range(itr):
            time.sleep(0.01)
            bar()
            
        [ws.send("STOP") for ws in WSC]

time.sleep(3)
clear_print_logo()

print("Tijdreiziger gevonden")
time.sleep(3)

x = 450
with alive_bar(x, title="Informatie downloaden", title_length=25, bar="scuba") as bar:
    [ws.send("CON&-1000") for ws in WSC]
    for i in range(x):
        time.sleep(0.01)
        bar()

time.sleep(1)

img.show()

[ws.send("STOP") for ws in WSC]

[ws.close() for ws in WSC]

time.sleep(100)