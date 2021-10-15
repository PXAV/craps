from tkinter import *


class Window:

    def __init__(self, height=400, width=800):
        self.root = Tk()
        self.height = height
        self.width = width

    def open(self):
        self.root.mainloop()

