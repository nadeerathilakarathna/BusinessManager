import sqlite3
import sys
import pygetwindow as gw
from ClassRunning import CurrentProcess
from ClassSQL import BusinessSQL
import ClassGUI
conn = sqlite3.connect('data/bm.db')

db = BusinessSQL()
gui = ClassGUI.Home()


import customtkinter


if not (CurrentProcess().isRunning()):
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()

    width = 1000 # Width
    height = 750 # Height

    screen_width = root.winfo_screenwidth()  # Width of the screen
    screen_height = root.winfo_screenheight() # Height of the screen

    # Calculate Starting X and Y coordinates for Window
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)

    root.geometry('%dx%d+%d+%d' % (width, height, x+50, y-40))


    ltitle = customtkinter.CTkLabel(master=root, text="Business Manager", font=("Arial", 25), pady=20)
    ltitle.pack()



    gui.HomeScreen(root=root)

    root.mainloop()
else:
    try:
        window = gw.getWindowsWithTitle("Business Manager")
        if window:
            window[0].activate()
            if window[0].isMinimized:
                window[0].restore()
        sys.exit(0)
    except:
        pass