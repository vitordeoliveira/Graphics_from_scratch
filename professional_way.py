import pygame
import numpy as np
from math import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 1200, 800
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 1000
circle_pos = [WIDTH/2, HEIGHT/2]  # x, y
angle = 1

class Point:
    def __init__(self, points) -> None:
        self.x = points[0]
        self.y = points[1]
        self.z = points[2]
        self.w = 1
        self.matrix = np.matrix([[self.x], [self.y], [self.z], [1.]])

class Triangule:
    def __init__(self, a:Point, b:Point, c:Point) -> None:
        self.a = a
        self.b = b
        self.c = c

class Mesh:
    tris = []

    def add(self, a, b, c):
        self.tris.append(Triangule(Point(a), Point(b), Point(c)))

meshCube = Mesh()

# all the cube vertices
# // SOUTH
meshCube.add((0.0, 0.0, 0.0), (0.0, 1.0, 0.0) , (1.0, 1.0, 0.0))    

# meshCube.add(0.0, 0.0, 0.0)    
# meshCube.add(1.0, 1.0, 0.0)    
# meshCube.add(1.0, 0.0, 0.0)

# // EAST                                                      
# meshCube.add(1.0, 0.0, 0.0)    
# meshCube.add(1.0, 1.0, 0.0)    
# meshCube.add(1.0, 1.0, 1.0)
# meshCube.add(1.0, 0.0, 0.0)    
# meshCube.add(1.0, 1.0, 1.0)    
# meshCube.add(1.0, 0.0, 1.0)

# // NORTH                                                     
# meshCube.add(1.0, 0.0, 1.0)    
# meshCube.add(1.0, 1.0, 1.0)    
# meshCube.add(0.0, 1.0, 1.0)
# meshCube.add(1.0, 0.0, 1.0)    
# meshCube.add(0.0, 1.0, 1.0)    
# meshCube.add(0.0, 0.0, 1.0)

# // WEST                                                      
# meshCube.add(0.0, 0.0, 1.0)    
# meshCube.add(0.0, 1.0, 1.0)    
# meshCube.add(0.0, 1.0, 0.0)
# meshCube.add(0.0, 0.0, 1.0)    
# meshCube.add(0.0, 1.0, 0.0)    
# meshCube.add(0.0, 0.0, 0.0)

# // TOP                                                       
# meshCube.add(0.0, 1.0, 0.0)    
# meshCube.add(0.0, 1.0, 1.0)    
# meshCube.add(1.0, 1.0, 1.0)
# meshCube.add(0.0, 1.0, 0.0)    
# meshCube.add(1.0, 1.0, 1.0)    
# meshCube.add(1.0, 1.0, 0.0)

# // BOTTOM                                                    
# meshCube.add(1.0, 0.0, 1.0)    
# meshCube.add(0.0, 0.0, 1.0)    
# meshCube.add(0.0, 0.0, 0.0)
# meshCube.add(1.0, 0.0, 1.0)    
# meshCube.add(0.0, 0.0, 0.0)    
# meshCube.add(1.0, 0.0, 0.0)


a = HEIGHT/WIDTH
f = 1/(tan(90/2))
zfar = 1000.
znear = 1.
l = (zfar/( zfar - znear))
l2 = -znear / (zfar * znear)

# MATRIX
projection_matrix = np.matrix([
    [a*f, 0 , 0  , 0   ],
    [0  , f , 0  , 0   ],
    [0  , 0 , l  , l2  ],
    [0  , 0 , 1  , 0   ]
])

# Perspective divide
def perspective(matrix, vec):

    offset = 6
    data = vec.copy()
    data[2] += offset


    result = np.dot(matrix, data).astype(float)

    w = result[3]

    if(w != 0):
        result[0] /= w
        result[1] /= w
        result[2] /= w

    return result


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
        # rotated2d = tri
        # rotated2da = np.dot(rotation_x, tri.a)
        # rotated2db = np.dot(rotation_x, tri.b)
        # rotated2dc = np.dot(rotation_x, tri.c)


        # # rotated2d = np.dot(rotation_z, rotated2d)
        # projected2d = perspective(projection_matrix, rotated2d.a)
        # projected2d = perspective(projection_matrix, rotated2d.b)
        # projected2d = perspective(projection_matrix, rotated2d.c)


        # x = int((projected2d[0][0]) * scale) + circle_pos[0]
        # y = int((projected2d[1][0]) * scale) + circle_pos[1]

        # projected_points[i] = [x, y]

        # pygame.draw.circle(screen, RED, (x, y), 5)
        
        pygame.draw.polygon(screen,BLACK,[(0, 30), (30, 60), (60, 0)],True)
        i += 1

    pygame.display.update()