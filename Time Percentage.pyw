from tkinter import *
from datetime import datetime, timezone
from ctypes import windll
from winreg import *

# To-Do: save settings in file

ALWAYS_ON_TOP = False
ALPHA = 1.0


# Windows Accent Color code adapted (and fixed) from:
# https://www.rigaspapas.com/blog/mastering-windows-10-appearance-with-python/

def getAccentColor():
    registry = ConnectRegistry(None, HKEY_CURRENT_USER)
    key = OpenKey(
        registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Accent')
    key_value = QueryValueEx(key, 'AccentColorMenu')
    accent_hex = str(hex(key_value[0]))[4:]
    accent = accent_hex[4:6]+accent_hex[2:4]+accent_hex[0:2]
    return '#'+accent


accent = getAccentColor()

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

border = Frame(root, highlightbackground=accent,
               highlightcolor=accent, highlightthickness=2, bd=0)
border.pack(fill=BOTH, expand=True)

l = Label(border, textvariable=text, bg='#333333',
          fg='#eeeeee', font=('Segoe UI', 18), bd=0)
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

        if new_y < 0:
            new_y = 0
        elif new_y > root.winfo_screenheight() - HEIGHT:
            new_y = int(root.winfo_screenheight() - HEIGHT)
        if new_x < 0:
            new_x = 0
        elif new_x > root.winfo_screenwidth() - WIDTH:
            new_x = int(root.winfo_screenwidth() - WIDTH)

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

    if not locked:
        border.config(highlightbackground=accent, highlightcolor=accent)
    else:
        border.config(highlightbackground='#454545', highlightcolor='#454545')


root.bind("<B1-Motion>", mouse_motion)
root.bind("<Button-1>", left_click)
root.bind("<Double-Button-1>", double_click)
root.bind("<Button-3>", right_click)

# End of Movement Code


def update():
    now = datetime.now(timezone.utc)
    seconds = (now - now.replace(hour=0, minute=0,
                                 second=0, microsecond=0)).seconds

    text.set(str(format(round(seconds/864, 2), '.2f')) + '%')

    if ALWAYS_ON_TOP:
        root.lift()

    root.after(1000, update)


root.after(0, update)
root.mainloop()
