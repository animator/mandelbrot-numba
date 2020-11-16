from tkinter import *
from PIL import ImageTk, Image
import math
import numpy as np
import numba as nb
import time

WIDTH = 500 
MAX_ITER = 2000

@nb.njit(parallel = True)
def mandelbrot(bbox, width, max_iter):     
    pixels = np.zeros((width, width, 3), dtype=np.uint8)
    for y in nb.prange(width):
        for x in range(width):
            c0 = complex(bbox[0] + (bbox[2]-bbox[0])*x/width, 
                         bbox[1] + (bbox[3]-bbox[1])*y/width) 
            c = 0
            for i in range(1, max_iter): 
                if abs(c) > 2: 
                    log_iter = math.log(i) 
                    pixels[y, x, :] = np.array([int(255*(1+math.cos(3.32*log_iter))/2), 
                                                int(255*(1+math.cos(0.774*log_iter))/2), 
                                                int(255*(1+math.cos(0.412*log_iter))/2)], 
                                               dtype=np.uint8) 
                    break
                c = c * c + c0
    return pixels

class MandelbrotCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
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

        calcpixels = mandelbrot(self.plane, WIDTH, MAX_ITER)
        return calcpixels

    def show_img(self, pixels = None):
        """
        Paint the mandelbrot set on the canvas.
        If the pixel array is not provided then paint the original mandelbrot set.
        """

        pixels = self.default_mandelbrot if pixels is None else pixels
        root.myimg = myimg = ImageTk.PhotoImage(Image.fromarray(pixels, mode='RGB'))
        self.create_image(int(WIDTH/2), int(WIDTH/2), image=myimg)

    def set_plane_bounds(self):
        """
        Calculates the new complex coordinates denoting the boundaries of
        the rectangle selected by the user.
        """

        bbox = sorted([(self.start_x, self.start_y), (self.end_x, self.end_y)])
        r_width = self.plane[2] - self.plane[0]
        i_width = self.plane[3] - self.plane[1]
        self.plane = (self.plane[0] + r_width*bbox[0][0]/WIDTH,
                      self.plane[1] + i_width*bbox[0][1]/WIDTH, 
                      self.plane[0] + r_width*bbox[1][0]/WIDTH,
                      self.plane[1] + i_width*bbox[1][1]/WIDTH)

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
        root.title("{0:.3g} secs".format(time_exec))

    def reset(self, event):
        """
        Reset the plot on right click.
        """

        self.plane = (-2.0, -1.5, 1.0, 1.5)
        self.show_img() 

root = Tk()
root.geometry("%dx%d+0+0" % (WIDTH, WIDTH))
sketch = MandelbrotCanvas(root, 
                          height = WIDTH, 
                          width = WIDTH, 
                          bd=0, 
                          highlightthickness=0,
                          cursor="cross")
sketch.grid(column=0, row=0)

root.mainloop()


