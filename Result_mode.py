from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, clamp
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import Mode_Select_mode
import Round_score

TIME_PER_FRAME = 0.3
FRAME_PER_TIME = 1.0 / TIME_PER_FRAME
FRAMES_PER_BACK_EFFECT = 10



class Result_Motion:
    def __init__(self):
        self.lose_image = load_image('resource/Loser.png')
        self.win_image = load_image('resource/Winner.png')
        self.x, self.y = 500, 300

    def draw(self):
        if Round_score.solo_mode_result == 'Win':
            self.win_image.clip_draw(0, 0, 240, 139, self.x, self.y, 1000, 600)
        elif Round_score.solo_mode_result == 'Lose':
            self.lose_image.clip_draw(0, 0, 240, 160, self.x, self.y, 1000, 600)




def init():
    global R_M

    R_M = Result_Motion()

def finish():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.change_mode(Mode_Select_mode)



def update():
    pass


def draw():
    clear_canvas()
    R_M.draw()
    update_canvas()

def pause(): pass

def resume(): pass