import pygame
import numpy as np
import math
import random

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cubo e Pirâmide 3D")

# rotacao nos eixos X, Y, Z
def rotate_x(vertices, theta):
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, math.cos(theta), -math.sin(theta)],
        [0, math.sin(theta), math.cos(theta)]
    ])
    return np.dot(vertices, rotation_matrix)

def rotate_y(vertices, theta):
    rotation_matrix = np.array([
        [math.cos(theta), 0, math.sin(theta)],
        [0, 1, 0],
        [-math.sin(theta), 0, math.cos(theta)]
    ])
    return np.dot(vertices, rotation_matrix)

def rotate_z(vertices, theta):
    rotation_matrix = np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ])
    return np.dot(vertices, rotation_matrix)

# projecao 3D para 2D
def project(vertices):
    projection_matrix = np.array([
        [1, 0, 0],
        [0, 1, 0]
    ])
    projected_points = np.dot(vertices, projection_matrix.T)
    return projected_points

# transladar 
def translate_to_center(vertices, translation):
    translated = []
    for vertex in vertices:
        translated.append([vertex[0] * 100 + screen_width // 2 + translation[0], vertex[1] * 100 + screen_height // 2 + translation[1]])
    return np.array(translated)

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

cube_vertices = np.array([
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
])

cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # base inferior
    (4, 5), (5, 6), (6, 7), (7, 4),  # base superior
    (0, 4), (1, 5), (2, 6), (3, 7)   # verticais conectando as bases
]

pyramid_vertices = np.array([
    [-1, -1, -1],  # inferior esquerda
    [1, -1, -1],   # inferior direita
    [1, 1, -1],    # superior direita
    [-1, 1, -1],   # superior esquerda
    [0, 0, 1]      # vértice superior
])

pyramid_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # arestas da base
    (0, 4), (1, 4), (2, 4), (3, 4)   # arestas conectando a base ao vértice superior
]

shape_color = (255, 255, 255)  
draw_cube = True  
translation = [0, 0, 0]  

clock = pygame.time.Clock()
theta_x, theta_y, theta_z = 0, 0, 0

running = True
while running:
    screen.fill((0, 0, 0))
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_c]:
        shape_color = random_color()
    
    if keys[pygame.K_s]:
        draw_cube = not draw_cube
    
    if keys[pygame.K_LEFT]:
        translation[0] -= 5  # Move para a esquerda
    if keys[pygame.K_RIGHT]:
        translation[0] += 5  # Move para a direita
    if keys[pygame.K_UP]:
        translation[1] -= 5  # Move para cima
    if keys[pygame.K_DOWN]:
        translation[1] += 5  # Move para baixo
    
    if draw_cube:
        rotated_vertices = rotate_x(cube_vertices, theta_x)
        rotated_vertices = rotate_y(rotated_vertices, theta_y)
        rotated_vertices = rotate_z(rotated_vertices, theta_z)
        projected_vertices = project(rotated_vertices)
        projected_vertices = translate_to_center(projected_vertices, translation)
        
        # desenhar o cubo
        for edge in cube_edges:
            pygame.draw.line(screen, shape_color, projected_vertices[edge[0]], projected_vertices[edge[1]], 2)
    else:
        rotated_vertices = rotate_x(pyramid_vertices, theta_x)
        rotated_vertices = rotate_y(rotated_vertices, theta_y)
        rotated_vertices = rotate_z(rotated_vertices, theta_z)
        projected_vertices = project(rotated_vertices)
        projected_vertices = translate_to_center(projected_vertices, translation)
        
        # desenhar a pirâmide
        for edge in pyramid_edges:
            pygame.draw.line(screen, shape_color, projected_vertices[edge[0]], projected_vertices[edge[1]], 2)
    
    # atualizar as rotações
    theta_x += 0.01
    theta_y += 0.01
    theta_z += 0.01
    
    pygame.display.flip()
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
