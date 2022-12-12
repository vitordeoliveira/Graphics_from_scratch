from asyncio import constants
import pygame
import numpy as np
from math import *

# CONSTANTS

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 1200, 800

# Variables
scale = 1000
circle_pos = [WIDTH/2, HEIGHT/2]  # x, y
angle = 1
aspectRatio = HEIGHT/WIDTH
angleOfView=90
fieldOfView = 1/(tan(angleOfView/2))
zfar = 1000.
znear = 1.
l = (zfar/( zfar - znear))
l2 = -znear / (zfar * znear)

pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))



class Point:
    def __init__(self, points) -> None:
        self.matrix = np.matrix([[points[0]], [points[1]], [points[2]], [1.]])

    def __str__(self) -> str:
        return str(self.matrix)


class Triangule:
    def __init__(self, a:Point, b:Point, c:Point) -> None:
        self.a = a
        self.b = b
        self.c = c
    

class Mesh:
    tris = []

    def add(self, a, b, c):
        self.tris.append(Triangule(Point(a), Point(b), Point(c)))




# MATRIX
projection_matrix = np.matrix([
    [aspectRatio*fieldOfView, 0 , 0  , 0   ],
    [0  , fieldOfView , 0  , 0   ],
    [0  , 0 , l  , l2  ],
    [0  , 0 , 1  , 0   ]
])

# Perspective divide
def perspective(matrix, vec):

    offset = 6
    data = vec.copy()
    data[2] += offset


    result = np.matmul(matrix, data).astype(float)

    w = result[3]

    if(w != 0):
        result[0] /= w
        result[1] /= w
        result[2] /= w

    return result



meshCube = Mesh()

# all the cube vertices
# // SOUTH
meshCube.add((0.0, 0.0, 0.0), (0.0, 1.0, 0.0) , (1.0, 1.0, 0.0))    
meshCube.add((0.0, 0.0, 0.0), (1.0, 1.0, 0.0) , (1.0, 0.0, 0.0))    

# // EAST                                                      
meshCube.add((1.0, 0.0, 0.0),(1.0, 1.0, 0.0),(1.0, 1.0, 1.0))
meshCube.add((1.0, 0.0, 0.0) ,(1.0, 1.0, 1.0) ,(1.0, 0.0, 1.0))

# // NORTH                                                     
meshCube.add((1.0, 0.0, 1.0),(1.0, 1.0, 1.0),(0.0, 1.0, 1.0))
meshCube.add((1.0, 0.0, 1.0),(0.0, 1.0, 1.0),(0.0, 0.0, 1.0))

# // WEST                                                      
meshCube.add((0.0, 0.0, 1.0),(0.0, 1.0, 1.0),(0.0, 1.0, 0.0))
meshCube.add((0.0, 0.0, 1.0),(0.0, 1.0, 0.0),(0.0, 0.0, 0.0))

# // TOP                                                       
meshCube.add((0.0, 1.0, 0.0),(0.0, 1.0, 1.0),(1.0, 1.0, 1.0))
meshCube.add((0.0, 1.0, 0.0),(1.0, 1.0, 1.0),(1.0, 1.0, 0.0))

# // BOTTOM                                                    
meshCube.add((1.0, 0.0, 1.0),(0.0, 0.0, 1.0),(0.0, 0.0, 0.0))
meshCube.add((1.0, 0.0, 1.0),(0.0, 0.0, 0.0),(1.0, 0.0, 0.0))


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
    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0,  0],
        [sin(angle), cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ])

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle), 0],
        [0, 1, 0, 0],
        [-sin(angle), 0, cos(angle), 0],
        [0, 0, 0, 0],
    ])

    rotation_x = np.matrix([
        [1, 0, 0, 1],
        [0, cos(angle), -sin(angle), 1],
        [0, sin(angle), cos(angle), 1],
        [0, 0, 0, 0],
    ])
    angle += 0.01

    screen.fill(WHITE)
    # drawining stuff

    i = 0
    for tri in meshCube.tris:
        rotatedX = Triangule    
        rotatedX.a = Point(np.matmul(rotation_x, tri.a.matrix))
        rotatedX.b = Point(np.matmul(rotation_x, tri.b.matrix))
        rotatedX.c = Point(np.matmul(rotation_x, tri.c.matrix))

        rotatedXZ = Triangule    
        rotatedXZ.a = Point(np.matmul(rotation_z, rotatedX.a.matrix))
        rotatedXZ.b = Point(np.matmul(rotation_z, rotatedX.b.matrix))
        rotatedXZ.c = Point(np.matmul(rotation_z, rotatedX.c.matrix))

        projected = Triangule    
        projected.a = Point(perspective(projection_matrix, rotatedXZ.a.matrix))
        projected.b = Point(perspective(projection_matrix, rotatedXZ.b.matrix))
        projected.c = Point(perspective(projection_matrix, rotatedXZ.c.matrix))

        xa = int((projected.a.matrix[0][0]) * scale) + circle_pos[0]
        ya = int((projected.a.matrix[1][0]) * scale) + circle_pos[1]

        xb = int((projected.b.matrix[0][0]) * scale) + circle_pos[0]
        yb = int((projected.b.matrix[1][0]) * scale) + circle_pos[1]

        xc = int((projected.c.matrix[0][0]) * scale) + circle_pos[0]
        yc = int((projected.c.matrix[1][0]) * scale) + circle_pos[1]


        # DRAW FIGURE

        pygame.draw.circle(screen, RED, (xa, ya), 2)
        pygame.draw.circle(screen, RED, (xb, yb), 2)
        pygame.draw.circle(screen, RED, (xc, yc), 2)
        
        pygame.draw.polygon(screen,BLACK,[(xa,ya), (xb,yb), (xc,yc)], True)
        i += 1

    pygame.display.update()