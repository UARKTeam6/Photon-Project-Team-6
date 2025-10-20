from tkinter import *
from PIL import Image, ImageTk

def show_splash(on_done):
    """Displays the splash screen, then calls on_done() after 3 seconds."""
    splash = Tk()
    height = 500
    width = 780
    x = (splash.winfo_screenwidth() // 2) - (width // 2)
    y = (splash.winfo_screenheight() // 2) - (height // 2)
    splash.geometry(f"{width}x{height}+{x}+{y}")

    try:
        img_path = "images/photon_logo.png"
        img = Image.open(img_path)
        img.thumbnail((width, height), Image.LANCZOS)
        splash_image = ImageTk.PhotoImage(img)
        Label(splash, image=splash_image).pack(expand=True)
        splash.overrideredirect(True)
    except Exception as e:
        print(f"Error loading splash image: {e}")

    # after 3 seconds, destroy splash and call on_done()
    splash.after(3000, lambda: (splash.destroy(), on_done()))
    splash.mainloop()
