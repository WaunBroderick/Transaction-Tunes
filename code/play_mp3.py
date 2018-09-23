import pandas as pd 
import numpy as np 
import pygame
from pygame import mixer

#import vlc

#p = vlc.MediaPlayer('/Users/kendallmccormick/documents/hackathon/happy1.mp3')
#p.play()

file = "/Users/kendallmccormick/documents/hackathon/happy1.mp3"
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
print("done")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy(): 
    pygame.time.Clock().tick(10)
#pygame.event.wait()