from pico2d import *

#Meta_Knight
walking_focus = [ [3,58], [3,66], [10,66], [15,50], [6,50], [3,66], [5,66] ]
Charge_Attack_focus = [[2, 50],[110, 50],[220,60],[325, 75],[425,110],[540, 100], [645,110],[645,110],[645,110]]




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

# 1c : 62 * 0 + 3 ~ 58
# 2c : 62 * 1 + 3 ~ 66
# 3c : 62 * 2 + 10 ~ 66
# 4c : 62 * 3 + 15 ~ 50
# 5c : 62 * 4 + 6  ~ 50
# 6c : 62 * 5 - 3  ~ 66
# 7c : 62 * 6 + 5  ~ 66


def Walking_Animation(): #Meta_Knight
    global frame
    Meta_Knight.clip_draw(62 * frame + walking_focus[frame][0], 655, walking_focus[frame][1], 60, 500, 400, 400, 400)
    frame = (frame + 1) % 7

# 1c : 55 * 0 + 2 ~ 50
# 2c : 62 * 1 + 55 ~ 50
# 3c : 62 * 2 + 10 ~ 66
# 4c : 62 * 3 + 15 ~ 50
# 5c : 62 * 4 + 6  ~ 50
# 6c : 62 * 5 - 3  ~ 66
# 7c : 62 * 6 + 5  ~ 66

def Charge_Attack_Animation(): #Meta_Knight
    global frame
    Meta_Knight.clip_draw(Charge_Attack_focus[frame][0], 480, Charge_Attack_focus[frame][1], 60, 500, 400,400,400)
    frame = (frame + 1) % 9



def Normal_Attack_Animation(): #Great_Husk_Sentry
    global frame
    if frame < 5:
        Meta_Knight.clip_draw((391 * frame) + 3, 3310, 388, 467, 500, 400)
    else:
        Meta_Knight.clip_draw((667 * (frame - 5)) + 3 * (frame - 3), 2864, 667, 424, 500 + 150, 400 - 20) # 사진이 조금 밀려서 그리는 위치를 옮김
    frame = (frame + 1) % 7


def Defense_Animation(): #Great_Husk_Sentry
    global frame
    if  frame < 4:
        Meta_Knight.clip_draw(367 * frame + 4, 4567, 363, 354, 500, 400)
    frame = (frame + 1) % 4


def Counter_Animation(): #Great_Husk_Sentry
    global frame
    if  frame < 3:
        Meta_Knight.clip_draw(445 * frame + 3, 1318, 442, 430, 500, 400)
    elif frame == 3:
        Meta_Knight.clip_draw(1370, 1107, 371, 641, 500, 400 + 100)
    elif 3 < frame < 7:
        Meta_Knight.clip_draw(421 * (frame-4) + 3, 650, 418, 430, 500, 400)
    frame = (frame + 1) % 7


# 카운터 동작 예시
def Defense_Counter_Animation(): #Great_Husk_Sentry
    global frame
    temp = 0
    if  frame < 4:
        Meta_Knight.clip_draw(367 * frame + 4, 4567, 363, 354, 500, 400)
    elif  frame < 7:
        temp = frame - 4
        Meta_Knight.clip_draw(445 * temp + 3, 1318, 442, 430, 500, 400)
    elif frame == 7:
        Meta_Knight.clip_draw(1370, 1107, 371, 641, 500, 400 + 100)
    elif 7 < frame < 12:
        temp = frame - 4
        Meta_Knight.clip_draw(421 * (temp-4) + 3, 650, 418, 430, 500, 400)
    frame = (frame + 1) % 11



def Damaged_Animation():
    global frame
    if frame % 2 == 0:
        Meta_Knight.clip_draw(3, 274, 379, 349, 500, 400)
    frame = (frame + 1) % 8


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

    Charge_Attack_Animation()
    update_canvas()
    delay(0.1)

