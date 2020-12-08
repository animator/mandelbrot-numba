import math
from canvas import view_mandelbrot
import numpy as np
import numba as nb

WIDTH = 600 
MAX_ITER = 6000

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

view_mandelbrot(WIDTH, MAX_ITER, mandelbrot)
