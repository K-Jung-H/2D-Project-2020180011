from pico2d import *
import game_framework

import World
from Background import BackGround
from player_MetaKnight import MetaKnight
from player_Kirby import Kirby

def P1_handle(event):
    if (event.key == SDLK_q or event.key == SDLK_w or event.key == SDLK_a or event.key == SDLK_s
                            or event.key == SDLK_d or event.key == SDLK_e or event.key == SDLK_f):
        return True
    return False

def P2_handle(event):
    if (event.key == SDLK_COMMA or event.key == SDLK_PERIOD or event.key == SDLK_SLASH or event.key == SDLK_UP
                                or event.key == SDLK_DOWN or event.key == SDLK_LEFT or event.key == SDLK_RIGHT):
        return True
    return False


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if P1_handle(event):
                p1.handle_event(event)
            elif P2_handle(event):
                p2.handle_event(event)


def init():
    global background
    global p1, p2

    p2 = MetaKnight()
    p1 = Kirby()
    World.add_object(p1, 1)
    World.add_object(p2, 1)
    background = BackGround()
    World.add_object(background, 0)


def finish():
    World.clear()
    pass


def update():
    World.update()
    # delay(0.01)


def draw():
    clear_canvas()
    World.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

