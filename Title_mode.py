from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import Play_mode
import Character_Select_mode

def init():
    global image
    image = load_image('resource/Kirby_Title.png')
    pass

def finish():
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(Character_Select_mode)
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.clip_draw(0, 0, 4210, 2571, 500, 300, 1000, 600)
    update_canvas()
    pass

def pause(): pass

def resume(): pass