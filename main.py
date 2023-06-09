import pygame
import sys
import map_interpreter
import map_data
import os
from enemy import *

import DLAmap
from player import Player_Object
from map_interpreter import *
from map_data import *

winWidth = 640
winHeight = 480

def load_Map():
    map = DLAmap.map_gen()
    map.explode_map()
    map.map_convert()
    map.map_finalize()
    return map.final_map

def y_sort(render_layer): #Sorts from bottom to top to get render order.
    for i in range(len(render_layer)):
        for j in range(i, len(render_layer)):
            if render_layer[i][2] >= render_layer[j][2]:
                cache = render_layer[i]
                render_layer[i] = render_layer[j]
                render_layer[j] = cache

def initialize_pygame(): 
    """Sets starting parameters, WIDTH, HEIGHT, and TITILE parameters and instantilizes PyGame"""
    TITLE = "Dwelt"
    GAME_PNG = pygame.image.load("Sprites/GAMETITLEICON.png")
    win = pygame.display.set_mode((winWidth, winHeight),vsync=1)
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(GAME_PNG)
    pygame.init()

    clock = pygame.time.Clock()
    return win,clock

if __name__ == '__main__':
    win, clock = initialize_pygame()
    player = Player_Object(1792, 1792)
    enemy = Enemy(1792, 1792)
    tileset = load_Map()

    dungeon = TileMap(tileset)


    while True:
        render_layer0 = []
        render_layer1 = []
        render_layer2 = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.left = True
            else:
                player.left = False

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
               player.right = True
            else:
                player.right = False

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.up = True
            else:
                player.up = False

            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.down = True
            else:
                player.down = False

            if keys[pygame.K_SPACE] or keys[pygame.K_RCTRL]:
                player.dash_active = True
            else:
                player.dash_active = False

        tiles, floor_tiles = dungeon.read(win)

        enemy.update(player.x, player.y)
        player.update()
        player.check_collisions(tiles)
        enemy.check_collisions(tiles)



        timer_frame = None 

        if 450 < player.cooldown <= 600: # Mainline check to append the Player Cooldown icon to the screen following the Dash (Accessibility Function)
            render_layer2.append((player.timer_sprites[1],player.x,player.y-45))

        elif 300 < player.cooldown <= 450:
            render_layer2.append((player.timer_sprites[2],player.x,player.y-45))

        elif 150 < player.cooldown <= 300:
            render_layer2.append((player.timer_sprites[3],player.x,player.y-45))

        elif 50 < player.cooldown <= 150:
            render_layer2.append((player.timer_sprites[4],player.x,player.y-45))

        elif 0 < player.cooldown <= 50: 
            render_layer2.append((player.timer_sprites[5],player.x,player.y-45))



        #Camera movement section start.
        camera_x = (player.x - winWidth/2 + 16)/20
        camera_y = (player.y - winHeight/2 + 16)/20

        dungeon.x0 -= camera_x
        dungeon.y0 -= camera_y

        player.x -= camera_x
        player.y -= camera_y

        enemy.x -= camera_x
        enemy.y -= camera_y
        #Camera movement section end.

        #Add to render layer 1.
        render_layer1.append(player.draw(win))
        render_layer1.append(enemy.render(win))
        
        render_layer0 += floor_tiles
        render_layer1 += tiles
        tiles.clear()
        floor_tiles.clear()
        #End to render layer 1.

        y_sort(render_layer1)

        #Render loop.
        win.fill((12,24,36))

        #Render render layer 1.

        for i in range(len(render_layer0)): 
            win.blit(render_layer0[i][0], (render_layer0[i][1], render_layer0[i][2]))

        for i in range(len(render_layer1)): # Walls, Players, Enemies
            win.blit(render_layer1[i][0], (render_layer1[i][1], render_layer1[i][2]))

        for i in range(len(render_layer2)): # Rendered HUD icons, Projectiles, Items
            win.blit(render_layer2[i][0], (render_layer2[i][1], render_layer2[i][2]))

        enemy.render(win)

        pygame.display.flip()
        
        clock.tick(120)