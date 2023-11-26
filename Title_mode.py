from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import Mode_Select_mode

class Message:
    image = None
    def __init__(self):
        if Message.image == None:
            Message.image = load_image('resource/start_message.png')
        self.x = 500
        self.y = 100
        self.start_time = get_time()

    def draw(self):
        if int(get_time() - self.start_time) % 2 == 1:
            self.image.clip_draw(0, 0, 696, 30, self.x, self.y, 600, 50)
        else:
            self.image.clip_draw(0, 30, 696, 59, self.x, self.y, 600, 50)

def init():
    global image
    global message
    image = load_image('resource/Kirby_Title.png')
    message = Message()
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
        elif event.type == SDL_KEYDOWN:
            game_framework.change_mode(Mode_Select_mode)
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.clip_draw(0, 0, 4210, 2571, 500, 300, 1000, 600)
    message.draw()
    update_canvas()
    pass

def pause(): pass

def resume(): pass