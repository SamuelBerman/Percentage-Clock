from tkinter import *
from threading import Timer
from datetime import datetime

x, y = 1700, 15

WIDTH, HEIGHT = 100, 40

root = Tk()
root.overrideredirect(True)
root.resizable(False, False)
root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

# movement code adapted from:
# https://stackoverflow.com/questions/4055267/tkinter-mouse-drag-a-window-without-borders-eg-overridedirect1

locked = False

def mouse_motion(event):
    if not locked:
        global x, y
        offset_x, offset_y = event.x - x, event.y - y  
        new_x = root.winfo_x() + offset_x
        new_y = root.winfo_y() + offset_y
        root.geometry(f"+{new_x}+{new_y}")

def left_click(event):
    if not locked:
        global x, y
        x, y = event.x, event.y

def middle_click(event):
    if not locked:
        root.destroy()

def right_click(event):
    global locked
    locked = not locked

root.bind("<B1-Motion>", mouse_motion)
root.bind("<Button-1>", left_click)
root.bind("<Button-2>", middle_click)
root.bind("<Button-3>", right_click)

# End of Movement Code

text = StringVar()

l = Label(root, textvariable=text, bg="#333333", fg='#cccccc', font=('Verdana', 16))
l.pack(fill=BOTH, expand=True)

def update():
    now = datetime.now()
    seconds = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).seconds

    text.set(str(format(round(seconds/864, 2), '.2f')) + '%')

    t = Timer(1, update)
    t.setDaemon(True)
    t.start()

update()
root.mainloop()
