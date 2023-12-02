from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import Mode_Select_mode
import game_framework
import BGM_player


class Guide:
    image = None
    def __init__(self):
        if Guide.image == None:
            Guide.image = load_image('resource/guide.png')
        self.x, self.y = 500, 300

    def draw(self):
        self.image.clip_draw(0, 0, 526, 378, self.x, self.y, 1000, 600)


def init():
    global guide
    global bgm
    bgm = BGM_player.BGM()
    bgm.play(0)
    guide = Guide()

def finish():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            bgm.play(-3)
            game_framework.change_mode(Mode_Select_mode)



def update():
    pass


def draw():
    clear_canvas()
    guide.draw()
    update_canvas()

def pause(): pass

def resume(): pass