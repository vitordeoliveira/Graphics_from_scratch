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

points = []

# all the cube vertices
points.append(np.matrix([0., 0., 1, 1.]))
points.append(np.matrix([1, 0., 1, 1.]))
points.append(np.matrix([1, 1, 1, 1.]))
points.append(np.matrix([0., 1, 1, 1.]))
points.append(np.matrix([0., 0., 0., 1.]))
points.append(np.matrix([1, 0., 0., 1.]))
points.append(np.matrix([1, 1, 0., 1.]))
points.append(np.matrix([0., 1, 0., 1.]))


a = HEIGHT/WIDTH
f = 1/(tan(90/2))

# x,y,z = afx, fy, z

zfar = 1000.
znear = 1.


l = (zfar/( zfar - znear))
l2 = -znear / (zfar * znear)

# x,y,z = afx, fy, lam*z - lam2

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
    vec[2] += offset
    result = np.dot(matrix, vec).astype(float)


    w = result[3][0]

    if(w > 0):
        result[0] /= w
        result[1] /= w
        result[2] /= w

    

    return result

projected_points = [
    [n, n] for n in range(len(points))
]


def connect_points(i, j, points):
    pygame.draw.line(
        screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


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
    for point in points:
        rotated2d = point.reshape((4, 1))
        # rotated2d = np.dot(rotation_z, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)
        rotated2d = np.dot(rotation_y, rotated2d)
        
        projected2d = perspective(projection_matrix, rotated2d)

        
        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, RED, (x, y), 5)
        i += 1

    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)

    pygame.display.update()