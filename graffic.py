from math import cos, sin
import os
from time import time
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
FPS = 144

vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1],
]

colors = [
    (1, 0, 0),  # Red
    (0, 1, 0),  # Green
    (0, 0, 1),  # Blue
    (1, 1, 0),  # Yellow
    (1, 0, 1),  # Magenta
    (0, 1, 1),  # Cyan
]

surfaces = [
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (2, 3, 7, 6),
    (1, 2, 6, 5),
    (4, 7, 3, 0),
]

def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
    width, height = texture_surface.get_size()
    texture_id = glGenTextures(1)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    return texture_id

def draw_textured_plane(texture_id, z_coord, shift_x=0, shift_y=0):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-3 + shift_x, -3 + shift_y, z_coord)
    glTexCoord2f(1, 0)
    glVertex3f(3 + shift_x, -3 + shift_y, z_coord)
    glTexCoord2f(1, 1)
    glVertex3f(3 + shift_x, 3 + shift_y, z_coord)
    glTexCoord2f(0, 1)
    glVertex3f(-3 + shift_x, 3 + shift_y, z_coord)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def draw_colored_cube():
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glColor3fv(colors[i])  
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glColor3fv((1, 1, 1))  
    glEnd()

def opengl_3d_cube():
    pygame.init()
    display = (1220, 700)
    base_speed = 0.15  # Adjust the movement speed here
    ctrl_speed = 0.35  # Adjust the movement speed here
    sensivity = 0.5
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_MODELVIEW)
    modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    
    texture_id = load_texture("texture.jpg")  # Replace with the path to your image
    logo_id = load_texture("texture.png")  # Replace with the path to your image
    
    clock = pygame.time.Clock()
    while True:
        glPushMatrix()
        glLoadIdentity()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                os._exit(0)
                
            if event.type == MOUSEMOTION:
                if event.buttons[0]:
                    rx, ry = event.rel
                    glRotatef(ry * sensivity, 1, 0, 0)
                    glRotatef(rx * sensivity, 0, 1, 0)
        
        keys = pygame.key.get_pressed()
        if (keys[K_LCTRL] or keys[K_RCTRL]):
            speed = ctrl_speed
        else:
            speed = base_speed
            
        if keys[K_LEFT] or keys[K_a]:
            glTranslatef(1*speed, 0, 0)
        if keys[K_RIGHT] or keys[K_d]:
            glTranslatef(-1*speed, 0, 0)
        if keys[K_SPACE]:
            glTranslatef(0, -1*speed, 0)
        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            glTranslatef(0, 1*speed, 0)
        if keys[K_s] or keys[K_DOWN]:
            glTranslatef(0, 0, -1*speed)
        if keys[K_w] or keys[K_UP]:
            glTranslatef(0, 0, 1*speed)
        

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMultMatrixf(modelMatrix)
        modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()
        glMultMatrixf(modelMatrix)

        draw_colored_cube()  
        draw_textured_plane(texture_id, -7)  
        s_y = 3*sin(time()*3)
        s_x = 3*cos(time()*3)
        s_z = (s_y*2 + s_x)/3
        draw_textured_plane(logo_id, 7 + s_z, s_y, s_x)  
        glPopMatrix()
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    opengl_3d_cube()
