import booter
import gui
import wifi
import update
import installer
import menu
import os
homedir = os.getenv("HOME")+"/.cider"
try:
    os.makedirs(homedir+"/systems")
except:
    print("homedir ("+homedir+") skiped")
gui.init()
win = gui.Gui()
def shutdown(win):
    print("shutting down")
    os.system("systemctl poweroff")
tabs = [menu.tick,booter.tick,installer.tick,update.tick,wifi.tick,shutdown]
tab = 0
while win.Open:
    win.Clear()
    tab = tabs[tab](win)
    win.Update()
gui.Quit()
