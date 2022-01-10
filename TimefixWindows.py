# -*- coding: UTF-8 -*-
from subprocess import PIPE, STDOUT
import subprocess
from ping3 import ping
import ctypes
import time
import psutil

is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
if is_admin == False:
    print("You need to launch this app in administrator")
    time.sleep(3)
    
else:
    #time.server.url.com = exemple link

    serverurl = ["time.windows.com","time.nist.gov","ntp.midway.ovh","ntp.unice.fr","ntp.accelance.net","ntp.cirad.fr","ntp.lothaire.net","chronos.espci.fr","chronos.univ-brest.fr","delphi.phys.univ-tours.fr","ntp.deuza.net"]
                    
    def search(number):
        try:
                    service = psutil.win_service_get("w32time")
                    service = service.as_dict()
                    if service and service['status'] != 'running':
                        subprocess.Popen("net start w32time")
        finally:
                    if number >= len(serverurl):
                        print("Cant connect to any server")
                        time.sleep(3)
                        return()
                    value = number
                    host = ping(serverurl[number])
                    if host == False:
                        search(value + 1)
                        return()
                    else:
                        subprocess.Popen(f"w32tm /config /update /manualpeerlist:{serverurl[number]} /syncfromflags:manual /reliable:yes")
                        subprocess.Popen(f"w32tm /resync", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, encoding="latin-1")
                        print(serverurl)
                    
    search(0)
