from pico2d import *

#Meta_Knight






open_canvas()
TUK_WIDTH, TUK_HEIGHT = 1000, 800
open_canvas(TUK_WIDTH,TUK_HEIGHT)
Kirby = load_image('resource/Sword_Kirby.png')
frame = 0


#complete parts

def Standing_Animation(): #Kirby
    global frame
    Kirby.clip_draw(30 * frame + 9, 2100, 30, 53, 500, 400,300, 300)
    frame = (frame + 1) % 1


walking_focus = [[9,2100],]

def Walking_Animation(): #Kirby
    global frame
    Kirby.clip_draw(30 * frame + 9, 2010, 30, 43, 500, 400, 300, 300)
    frame = 3 # (frame + 1) % 3


def Charge_Attack_Animation(): #Meta_Knight
    global frame
    Meta_Knight.clip_draw(Charge_Attack_focus[frame][0], 480, Charge_Attack_focus[frame][1], 60, 500, 400,400,400)
    frame = (frame + 1) % 10


def Normal_Attack_Animation(): #Meta_Knight
    global frame
    global frame
    Meta_Knight.clip_draw(Normal_Attack_focus[frame][0], 480, Normal_Attack_focus[frame][1], 60, 500, 400,400,400)
    frame = (frame + 1) % 5




def Speed_Attack_Animation(): #Meta_Knight
    global frame
    Meta_Knight.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][2], Speed_Attack_focus[frame][1], 60, 500, 400,400,400)
    frame = (frame + 1) % 5



def Defense_Animation(): #Great_Husk_Sentry
    global frame
    Meta_Knight.clip_draw(Defense_focus[frame][0], Defense_focus[frame][2], Defense_focus[frame][1], 70, 500, 400)
    frame = (frame + 1) % 9



def Counter_Animation(): #Meta_Knight
    global frame

    Meta_Knight.clip_draw(Counter_Attack_focus[frame][0], Counter_Attack_focus[frame][2], Counter_Attack_focus[frame][1], 60, 500, 400)
    frame = (frame + 1) % 9


def Damaged_Animation():
    global frame
    if frame % 2 == 0:
        if frame < 5 == 0:
            Meta_Knight.clip_draw(Damaged_focus[0][0], 600, Damaged_focus[0][1], 60, 500, 400)
        else:
            Meta_Knight.clip_draw(Damaged_focus[1][0], 600, Damaged_focus[1][1], 60, 500, 400)
    frame = (frame + 1) % 9


def Lose_Animation():
    global frame
    if frame < 3:
        Meta_Knight.clip_draw(382 * frame + 3, 274, 379, 349, 500, 400)
    else:
        Meta_Knight.clip_draw(388 * (frame-3) + 3, 3, 385, 249, 500, 400)
    frame = (frame + 1) % 6


#=======================================================================================


def handle_events():
    global running
    global pic_x,pic_y, size

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            print(pic_x, pic_y)
        else:
            handle_events()


running = True
clear_canvas()


while(running):
    clear_canvas()
    handle_events()
    #Standing_Animation()
    Walking_Animation()
    #Damaged_Animation()
    #Normal_Attack_Animation()
    #Charge_Attack_Animation()
    #Speed_Attack_Animation()

    #Counter_Animation()
    update_canvas()
    delay(0.1)

