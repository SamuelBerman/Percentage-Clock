from tkinter import *
from datetime import datetime, timezone
from ctypes import windll

# To-Do: multi-device, save settings in file

ALWAYS_ON_TOP = False
ALPHA = 1.0


windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
scale_factor = root.winfo_fpixels('1i') / 96.0

WIDTH, HEIGHT = 100 * scale_factor, 40 * scale_factor

x = (root.winfo_screenwidth() / 2) - (WIDTH / 2)
y = (root.winfo_screenheight() / 2) - (HEIGHT / 2)

root.overrideredirect(True)
root.resizable(False, False)
root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))
root.wm_attributes("-topmost", ALWAYS_ON_TOP)
root.wm_attributes("-alpha", ALPHA)

text = StringVar()

l = Label(root, textvariable=text, bg="#333333", fg='#cccccc', font=('Verdana', 16), bd=0, relief='solid')
l.pack(fill=BOTH, expand=True)

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


def double_click(event):
    if not locked:
        root.destroy()


def right_click(event):
    global locked
    locked = not locked
    l.config(bd=locked * scale_factor)


root.bind("<B1-Motion>", mouse_motion)
root.bind("<Button-1>", left_click)
root.bind("<Double-Button-1>", double_click)
root.bind("<Button-3>", right_click)

# End of Movement Code


def update():
    now = datetime.now(timezone.utc)
    seconds = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).seconds

    text.set(str(format(round(seconds/864, 2), '.2f')) + '%')

    if ALWAYS_ON_TOP:
        root.lift()

    root.after(1000, update)


root.after(0, update)
root.mainloop()
