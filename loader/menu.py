import gui
options = ["boot os","install os","update cider","configure wifi","shutdown"]
selected = 0
def tick(win):
    global options
    global selected
    selected += win.Input
    ind = 0
    for opt in options:
        win.DrawText(opt,(1,ind+1),selected==ind)
        ind+=1
    if(win.Select):
        return selected + 1
    selected=selected%len(options)
    return 0
