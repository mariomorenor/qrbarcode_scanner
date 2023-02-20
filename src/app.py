from tkinter import *
from camera import Camera


height = 600
width = 800

window = Tk()

window.title = "Registro Laboratorios"
window.geometry(f"{width}x{height}+0+0")

cam_widget = Label(window)
cam_widget.grid(row=0, column=0)

Camera(cam_widget).open()



window.mainloop()


