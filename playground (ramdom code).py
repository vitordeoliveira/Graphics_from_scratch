import pygame
import numpy as np
from math import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# // Projection Matrix
fNear = 0.1
fFar = 1000.0
fFov = 90.0
fAspectRatio = HEIGHT / WIDTH
fFovRad = 1.0 / tan(fFov * 0.5 / 180.0 * 3.14159)

# MATRIX

projection_matrix = np.matrix([
    [fAspectRatio * fFovRad , 0       , 0                                  , 0   ],
    [0                      , fFovRad , 0                                  , 0   ],
    [0                      , 0       , fFar / (fFar - fNear)              , 1   ],
    [0                      , 0       , (-fFar * fNear) / (fFar - fNear)  ,  0    ]
])


clock = pygame.time.Clock()
while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # update stuff

    # drawining stuff

    pygame.display.update()