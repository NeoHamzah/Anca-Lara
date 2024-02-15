import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


#creating a list of texture names that will be used to identify each texture.
texture_names = [0,1,2,3,4,5,6,7,8,9,10,11]

# assigning a unique integer identifier to each texture using global constants, which makes it easier to refer to textures throughout the code.
BG1 = 0
START = 1
EXIT = 2
TITTLE = 3
STARTCLICK = 4
EXITCLICK = 5
EASY = 6
EASYCLICK = 7
MEDIUM = 8
MEDIUMCLICK = 9
HARD = 10
HARDCLICK = 11

def load_texture():
    """
    enables 2D texture mapping for OpenGL, loads all the texture images and stores them as a list of texture binary data.
    It then generates a unique texture name for each image and sets up the texture parameters for each texture using the setup_texture() function.
    """
    glEnable(GL_TEXTURE_2D)

    images = []

    # Loges.append(pygame.image.load("assets/img/trainer.png"))
    images.append(pygame.image.load("assets/img/Background/BG.png"))
    images.append(pygame.image.load("assets/img/Button/START.png"))
    images.append(pygame.image.load("assets/img/Button/EXIT.png"))
    images.append(pygame.image.load("assets/img/Tittle.png"))
    images.append(pygame.image.load("assets/img/Button/START-CLICK.png"))
    images.append(pygame.image.load("assets/img/Button/EXIT-CLICK.png"))
    images.append(pygame.image.load("assets/img/Button/EASY.png"))
    images.append(pygame.image.load("assets/img/Button/EASY-CLICK.png"))
    images.append(pygame.image.load("assets/img/Button/MEDIUM.png"))
    images.append(pygame.image.load("assets/img/Button/MEDIUM-CLICK.png"))
    images.append(pygame.image.load("assets/img/Button/HARD.png"))
    images.append(pygame.image.load("assets/img/Button/HARD-CLICK.png"))
    
    # Convert the images to raw binary image data
    textures = [pygame.image.tostring(img,"RGBA", 1) for img in images]

    # Generate texture IDs
    glGenTextures(len(images), texture_names)

    # Bind each texture and set texture parameters
    for i in range(len(images)):
        setup_texture(textures[i],
                      texture_names[i],
                      images[i].get_width(),
                      images[i].get_height())


def setup_texture(binary_img, texture_iden, width, height):
    """
    binds the texture to the texture identifier, sets texture parameters, and then loads the texture binary data.
    """
    glBindTexture(GL_TEXTURE_2D, texture_iden)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width,
                 height, 0, GL_RGBA, GL_UNSIGNED_BYTE, binary_img)
