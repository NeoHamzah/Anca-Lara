from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from texture import *
import os, time
import pygame
from pygame.locals import *
import math
import random

menu = 0
lvl = 0
pos_x = 0
pos_y = 0
onbutton = False

pygame.init()

sounds = [pygame.mixer.Sound("assets/sound/bgmusic.wav"),
    pygame.mixer.Sound("assets/sound/mouse_point.wav"),
    pygame.mixer.Sound("assets/sound/jump.mp3")
    ]

def game(lvl):
    # create the game window
    game_width = 1600
    game_height = 800
    size = (game_width, game_height)
    pygame.display.set_caption('ANCA LARA')
    pygame_icon = pygame.image.load('assets/img/icon.png')
    pygame.display.set_icon(pygame_icon)
    game = pygame.display.set_mode(size)
    sounds[0].play(-1)
    # game variables
    score = 0
    speed = lvl

    class Player(pygame.sprite.Sprite):
        
        def __init__(self):
            
            pygame.sprite.Sprite.__init__(self)
            
            self.height = 400
            self.x = 25
            self.y = game_height - self.height
            self.action = 'running'
            self.health = 5
            self.spd = speed
            
            # load animasi run
            self.running_sprites = []
            self.running_sprite_index = 0
            for i in range(12):
                running_sprite = pygame.image.load(f'assets/img/char/running/run{i}.png').convert_alpha()
                scale = self.height / running_sprite.get_height() * 1.22
                new_width = running_sprite.get_width() * scale 
                new_height = running_sprite.get_height() * scale 
                running_sprite = pygame.transform.scale(running_sprite, (new_width, new_height))
                self.running_sprites.append(running_sprite)
                
            # load animasi jump
            self.jumping_sprites = []
            self.jumping_sprite_index = 0
            for i in range(6):
                jumping_sprite = pygame.image.load(f'assets/img/char/jumping/jump{i}.png').convert_alpha()
                scale = self.height / jumping_sprite.get_height() * 1.22
                new_width = jumping_sprite.get_width() * scale 
                new_height = jumping_sprite.get_height() * scale 
                jumping_sprite = pygame.transform.scale(jumping_sprite, (new_width, new_height))
                self.jumping_sprites.append(jumping_sprite)
                
            # set sprite rect
            self.rect = self.running_sprites[self.running_sprite_index].get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            
            # angka frame saat player menjadi invisible
            self.invincibility_frame = 0
            
        def draw(self):
            
            if self.action == 'running':
                running_sprite = self.running_sprites[int(self.running_sprite_index)]
                
                # tambah efek invisible saat player terkena obstacle
                if self.invincibility_frame > 0:
                    self.invincibility_frame -= 1
                if self.invincibility_frame % 10 == 0:
                    game.blit(running_sprite, (self.x, self.y))
                
            elif self.action == 'jumping' or self.action == 'landing':
                jumping_sprite = self.jumping_sprites[int(self.jumping_sprite_index)]
                
                # tambah efek invisible saat player terkena obstacle
                if self.invincibility_frame > 0:
                    self.invincibility_frame -= 1
                if self.invincibility_frame % 10 == 0:
                    game.blit(jumping_sprite, (self.x, self.y))
                
        def update(self):
            # update posisi y saat sprite melakukan jumping atau landing
            
            if self.action == 'running':
                
                self.running_sprite_index += 0.3 # tambah jika ingin animasi lari lebih cepat
                
                if self.running_sprite_index >= len(self.running_sprites):
                    self.running_sprite_index = 0
                    
                self.rect = self.running_sprites[int(self.running_sprite_index)].get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
                
                self.mask = pygame.mask.from_surface(self.running_sprites[int(self.running_sprite_index)])
                
            elif self.action == 'jumping' or self.action == 'landing':
                
                self.jumping_sprite_index += 0.2 # tambah jika ingin animasi lompat lebih cepat
                
                if self.jumping_sprite_index >= len(self.jumping_sprites):
                    self.jumping_sprite_index = 0
                    
                # ubah posisi y saat jumping dan landing
                if self.action == 'jumping':
                    self.y -= (8 + (0.5 * self.spd)) # kecepatan animasi lompat bertambah sesuai dengan game speed
                    
                    if self.y <= game_height - self.height * 1.7:
                        self.action = 'landing'
                        
                elif self.action == 'landing':
                    self.y += (8 +  (0.5 * self.spd)) # kecepatan animasi landing bertambah sesuai dengan game speed
                    
                    # ganti animasi menjadi run saat karakter menyentuh tanah
                    if self.y == game_height - self.height:
                        self.action = 'running'
                        
                self.rect = self.jumping_sprites[int(self.jumping_sprite_index)].get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
                
                self.mask = pygame.mask.from_surface(self.jumping_sprites[int(self.jumping_sprite_index)])
                
        def jump(self):
            # make the player go to jumping action when not already jumping or landing
            if self.action not in ['jumping', 'landing']:
                self.action = 'jumping'
                sounds[2].play(0)


    class Obstacle(pygame.sprite.Sprite):
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            
            # load gambar untuk obstacles
            self.obstacle_images = []
            for image_name in ['rock1', 'rock2', 'rock3', 'spikes']:
                image = pygame.image.load(f'assets/img/obstacles/{image_name}.png').convert_alpha()
                scale = 50 / image.get_width()
                new_width = image.get_width() * scale * 3
                new_height = image.get_height() * scale * 3
                image = pygame.transform.scale(image, (new_width, new_height))
                self.obstacle_images.append(image)
                
            # random image
            self.image = random.choice(self.obstacle_images)
            
            # posisi obstacles di sebelah paling kanan window
            self.x = game_width
            self.y = game_height - self.image.get_height()
            
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            
        def draw(self):
            game.blit(self.image, (self.x, self.y))
            
        def update(self):
            # ubah posisi obstacles
            # pindah ke kiri
            self.x -= speed
            
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            
            self.mask = pygame.mask.from_surface(self.image)
            
        def reset(self):
            # inisiasi obstacle baru dan reset posisinya
            
            self.image = random.choice(self.obstacle_images)
            self.x = game_width
            self.y = game_height - self.image.get_height()

    # set gambar sky
    sky = pygame.image.load('assets/img/gameBG/sky.png').convert_alpha()
    num_bg_tiles = math.ceil(game_width / sky.get_width()) + 1

    # set gambar terpisah untuk menghasilkan efek parallax
    bgs = []
    bgs.append(pygame.image.load('assets/img/gameBG/cloud.png').convert_alpha())
    bgs.append(pygame.image.load('assets/img/gameBG/tree_back.png').convert_alpha())
    bgs.append(pygame.image.load('assets/img/gameBG/tree_front.png').convert_alpha())

    parallax = []
    for x in range(len(bgs)):
        parallax.append(x)
        
    # inisiasi player
    player = Player()

    # inisiasi obstacles
    obstacles_group = pygame.sprite.Group()
    obstacle = Obstacle()
    obstacles_group.add(obstacle)

    # load gambar heart
    heart_sprites = []
    heart_sprite_index = 0
    for i in range(8):
        heart_sprite = pygame.image.load(f'assets/img/heart/heart{i}.png').convert_alpha()
        scale = 60 / heart_sprite.get_height()
        new_width = heart_sprite.get_width() * scale
        new_height = heart_sprite.get_height() * scale
        heart_sprite = pygame.transform.scale(heart_sprite, (new_width, new_height))
        heart_sprites.append(heart_sprite)

    # game loop
    clock = pygame.time.Clock()
    fps = 60
    quit = False
    while not quit:
                
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                quit = True
                
            # key space untuk jumping
            if event.type == KEYDOWN and event.key == K_SPACE:
                player.jump()                
            
        # draw sky
        for i in range(num_bg_tiles):
            game.blit(sky, (i * sky.get_width(), 0))
            
        # draw setiap background layer
        for i in range(len(bgs)):
            
            bg = bgs[i]
            
            for j in range(num_bg_tiles):
                game.blit(bg, (j * bg.get_width() + parallax[i], 0))
                
        # update berapa banyak setiap layer akan ter scroll 
        for i in range(len(parallax)):
            
            parallax[i] -= i + 4
            
            if abs(parallax[i]) > bgs[i].get_width():
                parallax[i] = 0
                
        # draw player
        player.draw()
        
        # update posisi player
        player.update()
        
        # draw obstacles
        obstacle.draw()
        
        # update posisi obstacle
        obstacle.update()
        
        # tambahkan score dan reset posisi obstacle
        if obstacle.x < obstacle.image.get_width() * -1:
            
            score += 1
            obstacle.reset()
            
            # menambah nilai speed saat berhasil melewati 2 obstacles
            if score % 2 == 0: #and speed < 10:
                speed += 1
                
        # cek apakah player menabrak obstacles
        if pygame.sprite.spritecollide(player, obstacles_group, True, pygame.sprite.collide_mask):
            player.health -= 1
            player.invincibility_frame = 30
            
            obstacles_group.remove(obstacle)
            obstacle = Obstacle()
            obstacles_group.add(obstacle)
            
        # menampilkan heart sebagai representasi nyawa player
        for life in range(player.health):
            heart_sprite = heart_sprites[int(heart_sprite_index)]
            x_pos = 10 + life * (heart_sprite.get_width() + 10)
            y_pos = 10
            game.blit(heart_sprite, (x_pos, y_pos))
            
        heart_sprite_index += 0.1
        
        if heart_sprite_index >= len(heart_sprites):
            heart_sprite_index = 0
            
        # menampilkan score
        brown = (102, 54, 34)
        font = pygame.font.Font(pygame.font.get_default_font(), 32)
        text = font.render(f'Score: {score}', True, brown)
        text_rect = text.get_rect()
        text_rect.center = (game_width - 110, 40)
        game.blit(text, text_rect)
                
        pygame.display.update()
        
        # gameover
        gameover = player.health == 0
        while gameover and not quit:
            
            # display game over message
            white = (255, 255, 255)
            pygame.draw.rect(game, brown, (0, 70, game_width, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 20)
            text = font.render('Game over. Play again? (Enter Y or N)', True, white)
            text_rect = text.get_rect()
            text_rect.center = (game_width / 2, 120)
            game.blit(text, text_rect)
            
            for event in pygame.event.get():
                
                if event.type == QUIT:
                    quit = True
                    
                # get the player's input (Y or N)
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        # reset the game
                        gameover = False
                        speed = lvl
                        score = 0
                        player = Player()
                        obstacle = Obstacle()
                        obstacles_group.empty()
                        obstacles_group.add(obstacle)
                    elif event.key == K_n:
                        quit = True
                        
            pygame.display.update()
    pygame.quit() 

def background(left, bottom, right, top, image):
        glBindTexture(GL_TEXTURE_2D, image)
        glBegin(GL_POLYGON)
        glTexCoord2f(0, 0)
        glVertex2f(left, bottom)
        glTexCoord2f(1, 0)
        glVertex2f(right, bottom)
        glTexCoord2f(1, 1)
        glVertex2f(right, top)
        glTexCoord2f(0, 1)
        glVertex2f(left, top)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, -1)

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glOrtho(0, 1600, 0, 800, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    load_texture()

def display():
    global menu, onbutton, lvl
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if menu == 0:
        glClearColor(0.2, 0.2, 0.2, 0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 1600, 0, 800, -1, 1)  # Adjusted for bottom-left origin
        glMatrixMode(GL_MODELVIEW)

        # CHANGE COLOR BACKGROUND WHEN MOUSE IN AREA BUTTON
        background(0, 0, 1600, 800, BG1)
        background(500, 400, 1100, 800, TITTLE)
        background(575, 220, 1025, 370, STARTCLICK if pos_x >= 575 and pos_x <= 1025 and pos_y >= 220 and pos_y <= 370 else START)
        background(575, 30, 1025, 180, EXITCLICK if pos_x >= 575 and pos_x <= 1025 and pos_y >= 30 and pos_y <= 180 else EXIT)
        glFlush()
        glutSwapBuffers()
        
    elif menu == 1:
        glClearColor(0.2, 0.2, 0.2, 0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 1600, 0, 800, 0, 1)  # Adjusted for bottom-left origin
        glMatrixMode(GL_MODELVIEW)

        # Rendering code with y-coordinates adjusted for the bottom-left origin
        background(0, 0, 1600, 800, BG1)
        background(575, 525, 1025, 675, EASYCLICK if pos_y >= 525 and pos_y <= 675 and pos_x >= 575 and pos_x <= 1025 else EASY)
        background(575, 325, 1025, 475, MEDIUMCLICK if pos_y >= 325 and pos_y <= 475 and pos_x >= 575 and pos_x <= 1025 else MEDIUM)
        background(575, 125, 1025, 275, HARDCLICK if pos_y >= 125 and pos_y <= 275 and pos_x >= 575 and pos_x <= 1025 else HARD)
        glFlush()
        glutSwapBuffers()
    
    elif menu == 2:
        game(lvl)
        
        os._exit(0)

def Timer(v):
    display()
    glutTimerFunc(10, Timer, 1)

def trackingMouse(x, y):
    global pos_x , pos_y, menu, onbutton, lvl
    pos_x = x
    pos_y = 800 - y

    if pos_x >= 575 and pos_x <= 1025 and pos_y >= 220 and pos_y <= 370 and menu == 0: # Button Home START
        if onbutton == False:
            sounds[1].play(0)
            onbutton = True
    elif pos_x >= 575 and pos_x <= 1025 and pos_y >= 30 and pos_y <= 180 and menu == 0: # Button Home Exit
        if onbutton == False:
            sounds[1].play(0)
            onbutton = True
    elif pos_y >= 525 and pos_y <= 675 and pos_x >= 575 and pos_x <= 1025 and menu == 1:  # Button Select Level Easy
        if onbutton == False:
            sounds[1].play(0)
            onbutton = True
            lvl = 10
    elif pos_y >= 325 and pos_y <= 475 and pos_x >= 575 and pos_x <= 1025 and menu == 1: # Button Select Level Medium
        if onbutton == False:
            sounds[1].play(0)
            onbutton = True
            lvl = 15
    elif pos_y >= 125 and pos_y <= 275 and pos_x >= 575 and pos_x <= 1025 and menu == 1: # Button Select Level Hard
        if onbutton == False:
            sounds[1].play(0)
            onbutton = True
            lvl = 20
    else :
        onbutton = False
        

def mouse(state, key, x, y):
    global menu
    if pos_y >= 220 and pos_y <= 370 and pos_x >= 575 and pos_x <= 1025 and key == GLUT_LEFT_BUTTON and menu == 0:
        menu = 1
    elif pos_y >= 30 and pos_y <= 180 and pos_x >= 575 and pos_x <= 1025 and key == GLUT_LEFT_BUTTON and menu == 0:
        os._exit(0)
    elif pos_y >= 525 and pos_y <= 675 and pos_x >= 575 and pos_x <= 1025 and key == GLUT_LEFT_BUTTON and menu == 1:
        menu = 2
    elif pos_y >= 325 and pos_y <= 475 and pos_x >= 575 and pos_x <= 1025 and key == GLUT_LEFT_BUTTON and menu == 1:
        menu = 2
    elif pos_y >= 125 and pos_y <= 275 and pos_x >= 575 and pos_x <= 1025 and menu == 1 and key == GLUT_LEFT_BUTTON and menu == 1:
        menu = 2


glutInit()
glutInitWindowSize(1600, 800)
glutInitWindowPosition(152, 110)
glutCreateWindow(b"ANCA LARA")
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
init()
glutPassiveMotionFunc(trackingMouse)
glutTimerFunc(10, Timer, 1)
glutMouseFunc(mouse)
glutDisplayFunc(display)
glutMainLoop()