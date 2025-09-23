from tkinter import *
import os
from PIL import Image, ImageTk

splash = Tk()
# Splash window target size (pixels)
height = 500
width = 780
x = (splash.winfo_screenwidth() // 2) - (width // 2)
y = (splash.winfo_screenheight() // 2) - (height // 2)
splash.geometry(f"{width}x{height}+{x}+{y}")

# load and display splash image
# try catch in case image not found
try:
    img_path = "images/photon_logo.png"
    img = Image.open(img_path)
    img = img.copy()
    img.thumbnail((width, height), Image.LANCZOS)
    splash_image = ImageTk.PhotoImage(img)
    sp_image = Label(
        splash,
        image=splash_image,
    )
    sp_image.pack(expand=True)
    splash.overrideredirect(True)  # Remove title bar
except Exception as e:
    print(f"Error loading splash image: {e}")

def main_window():
    splash.withdraw()
    
    window = Tk()
    window.configure(bg="white")
    height = 650
    width = 1240
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    
    def exit_window():
        window.quit()

    window.protocol("WM_DELETE_WINDOW", exit_window)


# splash screen timer
splash.after(3000, main_window)
# main window is what leads to main application

splash.mainloop()