from pico2d import *

#Meta_Knight
walking_focus = [ [3,58], [3,66], [10,66], [15,50], [6,50], [3,66], [5,66] ]
Charge_Attack_focus = [[2, 50],[110, 50],[220,60],[325, 75],[425,110], [425,110],[540, 100],[540, 100],[540, 100],[645,110]]
Normal_Attack_focus = [[110, 50],[220,60],[325, 75],[425,110], [425,110]]
Speed_Attack_focus = [ [2, 50, 485], [2, 50, 485], [755, 110, 480], [2, 100, 405],[110,100,400]]

Defense_focus = [[445, 30, 340],[498, 35, 340], [540, 35, 340],[592, 42, 330], [636, 42, 340],[0, 50, 210],[50, 50, 210],[113, 50, 210],[163, 50, 210]]
Counter_Attack_focus = [[0,52,275], [52,54,275], [106,52,275],[160,55,275],[215,65,275],[320,52,415],[320,52,415],[320,52,415],[425,65,405]]
Damaged_focus = [ [0, 40], [40, 40]]



open_canvas()
TUK_WIDTH, TUK_HEIGHT = 1000,800
open_canvas(TUK_WIDTH,TUK_HEIGHT)
Meta_Knight = load_image('resource/Meta_Knight_2.png')
frame = 0


#complete parts

def Standing_Animation(): #Meta_Knight
    global frame
    Meta_Knight.clip_draw(317 * frame + 3, 6027, 312, 347, 500, 400)
    frame = (frame + 1) % 5


def Walking_Animation(): #Meta_Knight
    global frame
    Meta_Knight.clip_draw(62 * frame + walking_focus[frame][0], 655, walking_focus[frame][1], 60, 500, 400, 400, 400)
    frame = (frame + 1) % 7


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

    #Damaged_Animation()
    #Normal_Attack_Animation()
    #Charge_Attack_Animation()
    #Speed_Attack_Animation()
    #Walking_Animation()
    #Counter_Animation()
    update_canvas()
    delay(0.1)

