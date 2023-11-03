from pico2d import *
import game_framework

import World
from Background import BackGround
from player import MetaKnight


# Game object class here

def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            p1.handle_event(event)


def init():
    global background
    global p1

    p1 = MetaKnight()
    World.add_object(p1, 1)

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

