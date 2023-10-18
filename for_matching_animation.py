from pico2d import *


open_canvas()
TUK_WIDTH, TUK_HEIGHT = 1000,800
open_canvas(TUK_WIDTH,TUK_HEIGHT)
Knight1 = load_image('resource/Great_Husk_Sentry.png')
frame = 0

pic_x = 312
pic_y = 6000

size = 340

#complete parts
#Great_Husk_Sentry
def Standing_Animation(): #Great_Husk_Sentry
    global frame
    Knight1.clip_draw(317 * frame + 3, 6027, 312, 347, 500, 400)
    frame = (frame + 1) % 5


def Walking_Animation(): #Great_Husk_Sentry
    global frame
    if  frame < 6:
        Knight1.clip_draw(318 * frame + 3, 5665, 312, 340, 500, 400)
    else:
        Knight1.clip_draw(315 * (frame - 6) + 6, 5321, 312, 340, 500, 400)
    frame = (frame + 1) % 8


def Normal_Attack_Animation(): #Great_Husk_Sentry
    global frame
    if frame < 5:
        Knight1.clip_draw((391 * frame) + 3, 3310, 388, 467, 500, 400)
    else:
        Knight1.clip_draw((667 * (frame - 5)) + 3 * (frame - 3), 2864, 667, 424, 500 + 150, 400 - 20) # 사진이 조금 밀려서 그리는 위치를 옮김
    frame = (frame + 1) % 7


def Defense_Animation(): #Great_Husk_Sentry
    global frame
    if  frame < 4:
        Knight1.clip_draw(367 * frame + 4, 4567, 363, 354, 500, 400)
    frame = (frame + 1) % 4


def Counter_Animation(): #Great_Husk_Sentry
    global frame
    if  frame < 3:
        Knight1.clip_draw(445 * frame + 3, 1318, 442, 430, 500, 400)
    elif frame == 3:
        Knight1.clip_draw(1370, 1107, 371, 641, 500, 400 + 100)
    elif 3 < frame < 7:
        Knight1.clip_draw(421 * (frame-4) + 3, 650, 418, 430, 500, 400)
    frame = (frame + 1) % 7


# 카운터 동작 예시
def Defense_Counter_Animation(): #Great_Husk_Sentry
    global frame
    temp = 0
    if  frame < 4:
        Knight1.clip_draw(367 * frame + 4, 4567, 363, 354, 500, 400)
    elif  frame < 7:
        temp = frame - 4
        Knight1.clip_draw(445 * temp + 3, 1318, 442, 430, 500, 400)
    elif frame == 7:
        Knight1.clip_draw(1370, 1107, 371, 641, 500, 400 + 100)
    elif 7 < frame < 12:
        temp = frame - 4
        Knight1.clip_draw(421 * (temp-4) + 3, 650, 418, 430, 500, 400)
    frame = (frame + 1) % 11



#=======================================================================================+
def handle_events():
    global running
    global pic_x,pic_y, size

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            pic_y += 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            pic_y -= 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            pic_x -= 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            pic_x += 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_PLUS:
            size += 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_MINUS:
            size -= 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            print(pic_x, pic_y)
        else:
            handle_events()


running = True
clear_canvas()


while(running):
    clear_canvas()
    handle_events()

    Defense_Counter_Animation()
    update_canvas()
    delay(0.1)

