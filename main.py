from pico2d import *

import World
from Background import BackGround
from player import Player


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
            player.handle_event(event)


def create_world():
    global running
    global background
    global player

    running = True

    player = Player()
    World.add_object(player, 1)

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
    delay(0.01)
# finalization code
close_canvas()
