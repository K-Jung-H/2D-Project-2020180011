from pico2d import *

import World
from Background import BackGround
from player import MetaKnight


# Game object class here

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            metaknight.handle_event(event)


def create_world():
    global running
    global background
    global metaknight

    running = True

    metaknight = MetaKnight()
    World.add_object(metaknight, 1)

    background = BackGround()
    World.add_object(background, 0)


def update_world():
    World.update()
    pass


def render_world():
    clear_canvas()
    World.render()
    update_canvas()


open_canvas(1000,600)
create_world()
# game loop

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.03)
# finalization code
close_canvas()
