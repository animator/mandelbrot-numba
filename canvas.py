from tkinter import *
from PIL import ImageTk, Image
import numpy as np
import time
import math

class MandelbrotCanvas(Canvas):
    def __init__(self, parent, mandelbrot_func, size, max_iter, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.size = size
        self.max_iter = max_iter
        self.mandelbrot_func = mandelbrot_func

        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind("<ButtonPress-2>", self.reset)

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        # Setting the bounds of real and imaginary axes
        # given by a tuple r1, i1, r2, i2
        self.plane = (-2.0, -1.5, 1.0, 1.5) 

        # The first computation
        t = time.time()
        self.default_mandelbrot = self.calculate()
        time_exec = time.time()-t
        self.show_img()      

        # Update the title to reflect the run time
        self.show_time(time_exec)

    def calculate(self):
        """
        Calculate the mandelbrot set.
        """

        calcpixels = self.mandelbrot_func(self.plane, self.size, self.max_iter)
        return calcpixels

    def show_img(self, pixels = None):
        """
        Paint the mandelbrot set on the canvas.
        If the pixel array is not provided then paint the original mandelbrot set.
        """

        pixels = self.default_mandelbrot if pixels is None else pixels
        if isinstance(pixels, list): 
            pixels = np.asarray(pixels).astype(np.uint8)
        if pixels.dtype != "uint8":
            pixels = pixels.astype(np.uint8)
        self.parent.myimg = myimg = ImageTk.PhotoImage(Image.fromarray(pixels, mode='RGB'))
        self.create_image(int(self.size/2), int(self.size/2), image=myimg)

    def set_plane_bounds(self):
        """
        Calculates the new complex coordinates denoting the boundaries of
        the rectangle selected by the user.
        """

        bbox = sorted([(self.start_x, self.start_y), (self.end_x, self.end_y)])
        r_width = self.plane[2] - self.plane[0]
        i_width = self.plane[3] - self.plane[1]
        self.plane = (self.plane[0] + r_width*bbox[0][0]/self.size,
                      self.plane[1] + i_width*bbox[0][1]/self.size, 
                      self.plane[0] + r_width*bbox[1][0]/self.size,
                      self.plane[1] + i_width*bbox[1][1]/self.size)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        self.rect = self.create_rectangle(self.start_x, self.start_y, 
                                            self.start_x+1, self.start_y+1, 
                                            fill="", outline="yellow", width=2)

    def on_move_press(self, event):
        self.end_x, self.end_y = (event.x, event.y)
        dY = self.end_y - self.start_y
        dX = self.end_x - self.start_x
        if abs(dY) < abs(dX):
            self.end_x = self.start_x + math.copysign(dY, dX)
        else:
            self.end_y = self.start_y + math.copysign(dX, dY)

        # expand rectangle as you drag the mouse
        self.coords(self.rect, self.start_x, self.start_y, 
                               self.end_x, self.end_y)  

    def on_button_release(self, event):
        """
        Calculates the mandelbrot set in the rectangle selected
        by the user.
        """

        self.set_plane_bounds()
        t = time.time()
        pixels = self.calculate()
        time_exec = time.time()-t
        self.show_img(pixels)
        self.show_time(time_exec)
        
    def show_time(self, time_exec):
        self.parent.title("{0:.2e}X Zoom - Time: {1:.3g} secs".format(3.0/(self.plane[2]-self.plane[0]), time_exec))

    def reset(self, event):
        """
        Reset the plot on right click.
        """

        self.plane = (-2.0, -1.5, 1.0, 1.5)
        self.show_img()

def view_mandelbrot(width, max_iter, mandelbrot_func):
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (width/2))
    y_cordinate = int((screen_height/2) - (width/2))

    root.geometry("%dx%d+%d+%d" % (width, width, x_cordinate, y_cordinate))
    sketch = MandelbrotCanvas(root, 
                              mandelbrot_func,
                              width,
                              max_iter,
                              height = width, 
                              width = width, 
                              bd=0, 
                              highlightthickness=0,
                              cursor="cross")
    sketch.grid(column=0, row=0)
    root.mainloop()    
