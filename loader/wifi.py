import gui
import os
import re
scanned = False
homedir = os.getenv("HOME")+"/.cider"
networks = []
password = "example"
mode = 0
select = 0
target = "invalid network"
tested = False
connected = 0
def scan():
    global networks
    global scanned
    if not scanned:
        try:
            os.remove(homedir+"/wifi.txt")
        except:
            pass
        os.system("nmcli d wifi &> "+homedir+"/wifi.txt")
        readnet = open(homedir+"/wifi.txt","r")
        rawnet = readnet.read()
        readnet.close()
        rawnet = rawnet.replace("\n","")
        rawnet = rawnet.split()
        networks = []
        net = -1
        for word in rawnet:
            if(word == "Infra"): # infrastructer mode
                name = ""
                wrd = net
                itr = 0
                while True:
                    if re.search("..:..:..:..:..:..",rawnet[wrd]): # mac address as regex
                                 break
                    name = rawnet[wrd]+" "+name if itr!=0 else rawnet[wrd]
                    wrd-=1
                    itr += 1
                networks.append(name)
            net += 1
        scanned = True
        print("found networks: "+str(networks))
def netpick(win):
    global select
    global mode
    global target
    off = 0
    select += win.Input
    select = select%len(networks)
    for net in networks:
        win.DrawText(net,(1,off),off==select)
        off+=1
    if win.Select:
        target = networks[select]
        mode+=1
def connect(win):
    global password
    global mode
    global tested
    win.DrawText("password for "+target+":",(1,0),False)
    win.DrawText("[enter to continue]",(1,2),False)
    password = win.DrawEntry(password,(1,1),True)
    if win.Select:
        os.system("nmcli d wifi connect "+target+" password "+password)
        tested = False
        mode+=1
def feedback(win):
    global tested
    global mode
    global connected
    if not tested:
        connected = os.system("ping -c 4 1.1.1.1")
        tested = True
    if connected == 0:
        win.DrawText("Connected",(1,0),False)
    else:
        win.DrawText("Failed to connect :(",(1,0),False)
    win.DrawText("[enter to continue] [escape to retry]",(1,1),True)
    if(win.Select):
        mode = -1
modes = [netpick,connect,feedback]
def tick(win):
    global scanned
    global networks
    global mode
    scan()
    modes[mode](win)
    if win.Back:
        mode-=1
    if mode < 0:
        scanned = False
        mode = 0
        return 0
    return 4
