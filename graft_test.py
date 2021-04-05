# from tkinter import *
# from PIL import ImageTk, Image
# import os

# root = Tk()
# panel = Label(root, image = img)
# panel.pack(side = "bottom", fill = "both", expand = "yes")
# root.mainloop()
import numpy as np

from tkinter import *
from PIL import Image, ImageTk


class Main(object):

    def __init__(self):
        self.canvas = None

    def main(self):
        self.master = Tk()
        self.i = 1

        # Right side of the screen / image holder
        right_frame = Frame(self.master, width=500, height=500, cursor="dot")
        right_frame.pack(side=LEFT)

        # Retrieve image
        image = Image.open(f"grafts/graft{self.i}.jpg")
        image = image.resize((1000, 1000), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)

        # Create canvas
        self.canvas = Canvas(right_frame, width=1000, height=1000)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.paint)
        self.master.bind("<space>", self.switch)
        self.master.bind("x", self.end)
        self.master.bind("n", self.next)

        self.mode = "calibration"
        self.coords =[]
        self.cal = []
        self.calibration = 1
        self.area = 0
        self.grafts = []

        print("Calibration: Mark two points that are 1cm apart and press the space key.")
        mainloop()

    def end(self, event):
        self.grafts.append(self.area)
        print(f"Total Areas: {self.grafts}")
        self.master.destroy()

    def next(self, event):
        print(f"Total Area: {self.area}")
        self.grafts.append(self.area)
        self.canvas.delete("all")

        self.i += 1
        image = Image.open(f"grafts/graft{self.i}.jpg")
        image = image.resize((1000, 1000), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        self.mode = "calibration"
        self.coords =[]
        self.cal = []
        self.calibration = 1
        self.area = 0
        print("Calibration: Mark two points that are 1cm apart and press the space key.")

    def paint(self, event):
        blue = "#0000FF"
        red = "#FF0000"
        r = 5
        x1, y1 = (event.x - 5), (event.y - 5)
        x2, y2 = (event.x + 5), (event.y + 5)
        self.canvas.create_oval(x1, y1, x2, y2, fill="blue", outline="white", width=2)

        if(self.mode == "draw"):
            self.coords.append((event.x, event.y))
        if(self.mode == "calibration"):
            self.cal.append((event.x, event.y))

    def switch(self, event):
        if self.mode == "calibration":
            self.mode = "draw"
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            self.calibrate()

            print(f"Successfully Calibrated! 1cm = {self.calibration} pixels")
            print("Now mark the outline of the first region and press the space key to calculate the area.")
        
        elif self.mode == "draw":
            self.calculate()
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            
            self.coords =[]

            print(f"Current total area is: {self.area} cm^2")
            print("Options: \n\t 1. You can continue marking the outline of the next region and press the space key.\n\t 2. Press 'n' to go to the next image\n\t 3. Press 'x' to exit.")

    def calibrate(self):
        self.calibration = np.sqrt((self.cal[1][0]- self.cal[0][0])**2 + (self.cal[1][1]- self.cal[0][1])**2)
    
    def calculate(self):
        self.area += self.shoelace(self.coords)/(self.calibration ** 2)

    def shoelace(self, x_y):
        x_y = np.array(x_y)
        x_y = x_y.reshape(-1,2)

        x = x_y[:,0]
        y = x_y[:,1]

        S1 = np.sum(x*np.roll(y,-1))
        S2 = np.sum(y*np.roll(x,-1))

        area = .5*np.absolute(S1 - S2)

        return area
if __name__ == "__main__":
    Main().main()