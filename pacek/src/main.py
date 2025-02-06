import pygame
import itertools
from collections import defaultdict
import threading
import timeit


coords = [[]]
pygame.init()
screen = pygame.display.set_mode((800, 1000))
clock = pygame.time.Clock()
running = True
stop_timer = False
game_stage = 1
select_option = 2
w, h = 10, 20

play_field = defaultdict(lambda: defaultdict(lambda: 0))
coord_size = 3

pygame.font.init()
helvetica = pygame.font.SysFont('helvetica', 30)

def spawn_block():
    global coords  # Modify the global coords
    coords = [[4, 0], [5, 0], [6, 0]]  # Initialize the coords list with the block positions
    play_field[4][0] = 1
    play_field[5][0] = 1
    play_field[6][0] = 1
    print(coords[0][0])
  

def move_block():
    global coords
    if coords:  # Check if coords is not empty
        for x in range(len(coords)):
            coords[x][1] += 1

            play_field[coords[x][0]][coords[x][1]-1] = 0 
            play_field[coords[x][0]][coords[x][1]] = 1  
    else:
        print("No blocks to move, coords is empty.")

def start_timer():
    if stop_timer == False:
        print("time")
        threading.Timer(3, continue_timer).start()

def continue_timer():
    move_block()
    if stop_timer == False:
        print("time")
        threading.Timer(3, continue_timer).start()


def rmenu():
    screen.fill("purple")
    pygame.draw.rect(screen,"grey",(0,0,800,1000))
    pygame.draw.rect(screen,"black",(250,350,300,400))
    pygame.draw.rect(screen,"white",(263,263+100*select_option,274,74))

    pygame.draw.rect(screen,(192,191,188),(265,365,270,70))
    screen.blit(helvetica.render("play",False,(0,0,0)),(265,365))

    pygame.draw.rect(screen,(192,191,188),(265,465,270,70))
    screen.blit(helvetica.render("highscore",False,(0,0,0)),(265,465))

    pygame.draw.rect(screen,(192,191,188),(265,565,270,70))
    screen.blit(helvetica.render("options",False,(0,0,0)),(265,565))

    pygame.draw.rect(screen,(192,191,188),(265,665,270,70))
    screen.blit(helvetica.render("exit",False,(0,0,0)),(265,665))

timeit.timeit('print("hello")',number =1000)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop_timer = True
            running = False
        if game_stage ==1:
            if event.type == pygame.KEYUP:
                if event.key ==pygame.K_s:
                    select_option +=1
                    if select_option > 4:
                        select_option = 1
                elif event.key == pygame.K_w:
                    select_option -=1
                    if select_option <=0:
                        select_option = 4
                elif event.key == pygame.K_RETURN:
                    if select_option ==1:
                        game_stage = 2
                        start_timer()
                        spawn_block()
                    elif select_option == 4:
                        running = False
        #elif game_stage == 2:

    if  game_stage == 1:
        rmenu()

    elif game_stage == 2:
        frame_w = 10
        rect_size = 40
        screen.fill("purple")
        pygame.draw.rect(screen,"grey",(0,0,800,1000))
        pygame.draw.rect(screen,"blue",(0,1000-(rect_size*20)-(frame_w*2),rect_size*10+(frame_w*2),rect_size*20+(frame_w*2)))       
        for i in range(10):
            for j in range(20):
                if play_field[i][j] == 1:
                     pygame.draw.rect(screen,'green',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))   
                else:
                    if j %2 != 0:
                        if i % 2 == 0:
                            pygame.draw.rect(screen,'grey',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))
                        else:
                            pygame.draw.rect(screen,'black',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))
                    if j % 2 == 0:
                        if i % 2 == 0:    
                            pygame.draw.rect(screen,'black',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))
                        else:
                            pygame.draw.rect(screen,'grey',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))

        


    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()


