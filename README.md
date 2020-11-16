# mandelbrot-numba

This repository contains the Mandelbrot Set Generator code with zoom feature. It is a good starting point for new `numba` users to witness the various ways in which one can achieve code speed-up using `numba`.

Each implementation has a dedicated branch and the recommended learning sequence that should be followed is provided below:

| Branch | Data Layer | `@njit` | `parallel = True` | Link |
|--|--|--|--|--|
| `python-list` | Native `list` | - | - | [Link](https://github.com/animator/mandelbrot-numba/tree/python-list) |
| `njit-python-list` | Native `list` | Yes | - | [Link](https://github.com/animator/mandelbrot-numba/tree/njit-python-list) |
| `njit-parallel-python-list` | Native `list` | Yes | Yes | [Link](https://github.com/animator/mandelbrot-numba/tree/njit-parallel-python-list) |
| `numpy-array` | NumPy array | - | - | [Link](https://github.com/animator/mandelbrot-numba/tree/numpy-array) |
| `njit-numpy-array` | NumPy array | Yes | - | [Link](https://github.com/animator/mandelbrot-numba/tree/njit-numpy-array) |
| `njit-parallel-numpy-array` | NumPy array | Yes | Yes | [Link](https://github.com/animator/mandelbrot-numba/tree/njit-parallel-numpy-array) |

To execute the code just run:

```
$ python3 mandelbrot.py
```

A Tkinter GUI will pop-up. You can use `left` mouse button to drag and select an area to zoom into. `Right` click to reset the canvas.

![](mandelbrot.gif)

Install the following dependencies:

```
$ pip3 install numba numpy Pillow
```

`Tk` comes pre-installed with Python.




