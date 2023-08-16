import sys
import os
import pickle as pk
import time

from .drawings import *
from .scores import *
from .utils import *


__version__ = "2.5.5"
bar_color1 = 'darkturquoise'

def love():
    """
    A simple demo.
    """
    x = np.hstack([np.linspace(-1,-0.99,10),np.linspace(-0.99,0.99,100),np.linspace(0.99,1,10)])

    y1 = np.sqrt(1-x**2)+np.abs(x)
    plt.plot(x,y1,color='r',linestyle='--',linewidth=2)

    y2 = -np.sqrt(1-x**2)+np.abs(x)
    plt.plot(x,y2,color='r',linestyle='--',linewidth=2)
    plt.fill_between(x, y1, y2, facecolor='pink')
    plt.title(r'$y=\left|x\right| \pm \sqrt{1-x^2}$')
    plt.show()

if __name__ == "__main__":
    love()
    
