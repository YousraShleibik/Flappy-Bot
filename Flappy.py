import random
import sys
import pygame
from pygame.locals import *
import numpy
import matplotlib.pyplot as plt
import time
import os

WIN_WODTH = 600
WIN_HEIGHT = 800

BIRD_IMG= [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs",'bird1.png')))]