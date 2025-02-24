import pygame # type: ignore
import itertools
from collections import defaultdict
import threading
import timeit
import random

speed = 0.5

coords = [[]]
current_object = 1
block_queue = []
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

def spawn_block(which):
    global running
    global current_object
    global block_queue
    global coords 

    which = block_queue[0]
    block_queue.pop(0)
    current_object = which
    
    if which == 1:
        coords = [[4, 0], [5, 0], [4, 1],[5,1]] 
        play_field[4][0] = 1
        play_field[5][0] = 1
        play_field[4][1] = 1
        play_field[5][1] = 1
    elif which == 2:
        coords = [[4, 0], [5, 0], [5, 1],[6,1]] 
        play_field[4][0] = 2
        play_field[5][0] = 2
        play_field[5][1] = 2
        play_field[6][1] = 2
    elif which == 3:
        coords = [[4, 1], [5, 1], [5, 0],[6,0]] 
        play_field[4][1] = 3
        play_field[5][1] = 3
        play_field[5][0] = 3
        play_field[6][0] = 3
    elif which == 4:
        coords = [[4, 0], [5, 0], [5, 1],[5,2]] 
        play_field[4][0] = 4
        play_field[5][0] = 4
        play_field[5][1] = 4
        play_field[5][2] = 4
    elif which == 5:
        coords = [[4, 0], [5, 0], [4, 1],[4,2]] 
        play_field[4][0] = 5
        play_field[5][0] = 5
        play_field[4][1] = 5
        play_field[4][2] = 5
    elif which == 6:
        coords = [[4, 0], [4, 1], [3, 1],[5,1]] 
        play_field[4][0] = 6
        play_field[4][1] = 6
        play_field[3][1] = 6
        play_field[5][1] = 6
    elif which == 7:
        coords = [[4, 0], [5, 0], [6, 0],[7,0]] 
        play_field[4][0] = 7
        play_field[5][0] = 7
        play_field[6][0] = 7
        play_field[7][0] = 7
    if check_floor():
        running = False

def move_block(which_side, value):
    global coords
    if coords: 
        original_number = play_field[coords[0][0]][coords[0][1]] 
        new_coords = []  

        for x, y in coords:
            if which_side == 0: 
                if check_floor():
                    spawn_block(random.randint(1,7)) 
                    return 
                new_coords.append([x, y + 1])

            elif which_side == 1:  
                if 0 <= x + value < 10: 
                    new_coords.append([x + value, y])
                else:
                    return 

        for x, y in coords:
            play_field[x][y] = 0  

        coords = new_coords
        for x, y in coords:
            play_field[x][y] = original_number 



def rotate_block():
    global coords, play_field
    if coords:
        pivot = coords[0]
        new_coords = []

        for x, y in coords:
            new_x = pivot[0] + (y - pivot[1])
            new_y = pivot[1] - (x - pivot[0])
            new_coords.append([new_x, new_y])

        print("Old coords:", coords)
        print("New coords:", new_coords)

        valid_move = True

        for x, y in new_coords:
            if not (0 <= x < 10 and 0 <= y < 20):
                valid_move = False
                print(f"Out of bounds: {x}, {y}")
                break

            if play_field[x][y] >= 10:
                valid_move = False
                print(f"Collision at: {x}, {y}")
                break

        if valid_move:
            for x, y in coords:
                play_field[x][y] = 0 

            coords = new_coords

            for x, y in coords:
                play_field[x][y] = current_object 

def check_floor():
    global coords
    global stop_timer
    freeze = False
    if coords:
        for x,y in coords:
            if play_field[x][y+1]>10  or y>=19:
                if y == 0:
                    stop_timer = True
                    pygame.quit()
                freeze = True
        if freeze:
            for x,y in coords:
                block_queue.append(random.randint(1,7))
                play_field[x][y]+=10
    return freeze

def start_timer():
    if stop_timer == False:
        print("time")
        threading.Timer(speed, continue_timer).start()

def continue_timer():
    move_block(0,1)
    if stop_timer == False:
        print("time")
        threading.Timer(speed, continue_timer).start()


def rmenu():
    screen.fill("purple")
    pygame.draw.rect(screen,"grey",(0,0,800,1000))
    pygame.draw.rect(screen,"black",(250,350,300,200))
    pygame.draw.rect(screen,"white",(263,263+100*select_option,274,74))

    pygame.draw.rect(screen,(192,191,188),(265,365,270,70))
    screen.blit(helvetica.render("play",False,(0,0,0)),(265,365))

    pygame.draw.rect(screen,(192,191,188),(265,465,270,70))
    screen.blit(helvetica.render("exit",False,(0,0,0)),(265,465))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop_timer = True
            running = False
        if game_stage ==1:
            if event.type == pygame.KEYUP:
                if event.key ==pygame.K_s:
                    select_option +=1
                    if select_option > 2:
                        select_option = 1
                elif event.key == pygame.K_w:
                    select_option -=1
                    if select_option <=0:
                        select_option = 2
                elif event.key == pygame.K_RETURN:
                    if select_option ==1:
                        game_stage = 2
                        while len(block_queue) <5:
                            block_queue.append(random.randint(1,7))
                        start_timer()
                        spawn_block(1)
                    elif select_option == 2:
                        running = False
        elif game_stage == 2:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    move_block(1,1)
                elif event.key == pygame.K_a:
                    move_block(1,-1)
                elif event.key == pygame.K_SPACE:
                    rotate_block()

    if  game_stage == 1:
        rmenu()

    elif game_stage == 2:
        offset = 200
        ite = 200
        frame_w = 10
        rect_size = 40
        screen.fill("purple")
        pygame.draw.rect(screen,"grey",(0,0,800,1000))
        pygame.draw.rect(screen,"blue",(0,1000-(rect_size*20)-(frame_w*2),rect_size*10+(frame_w*2),rect_size*20+(frame_w*2)))    
        pygame.draw.rect(screen,"black",(420,180,200,800))
        if block_queue:
            for x in range(0,len(block_queue)):
                if block_queue[x] == 1:
                    pygame.draw.rect(screen,"green",(460,offset+ite*x,80,80))
                elif block_queue[x] == 2:
                    pygame.draw.rect(screen,"red",(460,offset+ite*x,80,40))
                    pygame.draw.rect(screen,"red",(500,40+offset+ite*x,80,40))
                elif block_queue[x] == 3:
                    pygame.draw.rect(screen,"orange",(500,-40+offset+ite*x,80,40))
                    pygame.draw.rect(screen,"orange",(460,offset+ite*x,80,40))
                elif block_queue[x] == 4:
                    pygame.draw.rect(screen,"cyan",(460,offset+ite*x,80,40))
                    pygame.draw.rect(screen,"cyan",(500,40+offset+ite*x,40,80))
                elif block_queue[x] == 5:
                    pygame.draw.rect(screen,"purple",(460,offset+ite*x,80,40))
                    pygame.draw.rect(screen,"purple",(460,40+offset+ite*x,40,80))
                elif block_queue[x] == 6:
                    pygame.draw.rect(screen,"violet",(460,offset+ite*x,40,40))
                    pygame.draw.rect(screen,"violet",(420,40+offset+ite*x,120,40))
                elif block_queue[x] == 7:
                    pygame.draw.rect(screen,"pink",(460,offset+ite*x,40,160))

        for j in range(20):
            filled = 0
            for i in range(10):
                if play_field[i][j] == 1:
                     pygame.draw.rect(screen,'green',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))   
                elif play_field[i][j] ==2:
                    pygame.draw.rect(screen,'red',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))
                elif play_field[i][j] ==3:
                    pygame.draw.rect(screen,'orange',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))
                elif play_field[i][j] ==4:
                    pygame.draw.rect(screen,'cyan',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))
                elif play_field[i][j] ==5:
                    pygame.draw.rect(screen,'purple',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))
                elif play_field[i][j] ==6:
                    pygame.draw.rect(screen,'violet',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))
                elif play_field[i][j] ==7:
                    pygame.draw.rect(screen,'pink',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))
                elif play_field[i][j] >10:
                    pygame.draw.rect(screen,'blue',(frame_w+(rect_size*i),1000-(rect_size*20)-frame_w+(rect_size*j),rect_size,rect_size))
                    filled+=1

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
                if filled == 10:
                    speed -= 0.01
                    print(speed)
                    for x, y in coords:
                         play_field[x][y] = 0  

                    for k in range(j, 0, -1):
                         for i in range(10):
                            play_field[i][k] = play_field[i][k - 1]

                    for i in range(10):
                        play_field[i][0] = 0

                    for x, y in coords:
                        play_field[x][y] = current_object  

    pygame.display.flip()

pygame.quit()


