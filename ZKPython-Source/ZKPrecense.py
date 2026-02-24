from pypresence import Presence
import keyboard
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from rich import print
import json
import requests
import sys, os
from plyer import notification
from pathlib import Path

PORT = 9977
client_id = "1355259672013177043"
RPC = None
StartRun = None
GameImg = None
Ended = False

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes("ZKPresence Working :3", "utf8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        global Ended
        global GameImg
        global StartRun
        
        try:
            parsed_data = json.loads(post_data.decode('utf-8'))

            if parsed_data["Unloaded"] == True:
                Ended = True
                GameImg = None
                RPC.update(state = "On Main Studio",start=int(time.time()))
                #print("Unloaded")
                return
            else:
                if Ended == True:
                    Ended = False
                    StartRun = int(time.time())
                    #print("Reanuded")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            Activity = {}

            if parsed_data["Settings"]["ShowGameImg"] == True and GameImg == None:
                UniID = parsed_data["UniverseID"]
                Responce = requests.get(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={UniID}&returnPolicy=0&size=512x512&format=Png&isCircular=false")
                Responce.raise_for_status()
                GameImg = Responce.json()["data"][0]["imageUrl"]

            elif parsed_data["Settings"]["ShowGameImg"] == False and not GameImg == None:
                GameImg = None

            Activity["large_image"] = parsed_data["Images"]["LImage"]["Img"]
            Activity["large_text"] = parsed_data["Images"]["LImage"]["Desc"]
            Activity["small_text"] = parsed_data["Images"]["SImage"]["Desc"]
            Activity["small_image"] = parsed_data["Images"]["SImage"]["Img"]

            if not parsed_data["Buttons"][0]["url"] == "":
                Activity["buttons"] = parsed_data["Buttons"]

            if not GameImg == None:
                if parsed_data["DevType"] == "Workspace":
                    Activity["large_image"] = GameImg

            Activity["state"] = parsed_data["State"]
            Activity["details"] = parsed_data["Details"]
            Activity["start"] = StartRun

            if parsed_data["Collaborators"]["Enabled"] == True:
                Activity["party_size"] = [parsed_data["Collaborators"]["Actual"], parsed_data["Collaborators"]["Max"]]

            try:
                RPC.update(**Activity)
            except Exception as e:
                print(f"Error While Updating ZKP: {e}")

                notification.notify(
                    app_name = "ZKPrecense",
                    title = "ZKP Posible Critical ERROR!",
                    message = str(e),
                    app_icon = str(Path.cwd() / "Art\\ZKPLogoExport.ico"),
                    timeout = 5
                )

        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Error: Invalid JSON data")

    def log_message(self, format, *args):
        # Disable the fking console print
        pass

try:
    RPC = Presence(client_id)
    RPC.connect()
    StartRun = int(time.time())

    # pyfiglet doesnt work
    print("███████╗██╗░░██╗██████╗░██████╗░███████╗░█████╗░███████╗███╗░░██╗░█████╗░███████╗")
    print("╚════██║██║░██╔╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝████╗░██║██╔══██╗██╔════╝")
    print("░░███╔═╝█████═╝░██████╔╝██████╔╝█████╗░░██║░░╚═╝█████╗░░██╔██╗██║██║░░╚═╝█████╗░░")
    print("██╔══╝░░██╔═██╗░██╔═══╝░██╔══██╗██╔══╝░░██║░░██╗██╔══╝░░██║╚████║██║░░██╗██╔══╝░░")
    print("███████╗██║░╚██╗██║░░░░░██║░░██║███████╗╚█████╔╝███████╗██║░╚███║╚█████╔╝███████╗")
    print("╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░╚═╝╚══════╝░╚════╝░╚══════╝╚═╝░░╚══╝░╚════╝░╚══════╝")

    print("ZKPresence active and listening on port: '9977' \nMade By ZuKomaDEV \ninspired from StudioPresence v3.0.4 \nOriginated by: DRPC by RigidStudios")
    print("Source Code In: https://github.com/ZuKomaDEVYT/ZKPrecense")
    print("\nPress 'Ctrl + C' to Stop ZKPrecense!")

    RPC.update(state = "Waiting ZKP In Studio!",start=int(time.time()))

except Exception as e:
   notification.notify(
        app_name = "ZKPrecense",
        title = "CRITICAL ZKP ERROR!",
        message = "ZKP Experienced a Critical Error While Starting Up",
        app_icon = str(Path.cwd() / "Art\\ZKPLogoExport.ico"),
        timeout = 15
    )
   
   print(f"An Critical Error occurred: {e}")
   input("Press 'ENTER' to close")
   sys.exit(1)

try:
    with HTTPServer(('', PORT), handler) as server:
        server.serve_forever()
        server.shutdown()
except KeyboardInterrupt:
    print("Pressed 'ctrl + c'")

    for i in range(4):
        print(f"Closing ZKP in: {i}", end="\r", flush=True)
        time.sleep(1)

    sys.exit(0)