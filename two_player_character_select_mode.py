from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, load_font
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_a, SDLK_d, SDLK_LEFT, SDLK_RIGHT


import game_framework
import two_player_mode

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

P1 = 0
P2 = 0

class P1_Controller:
    def __init__(self):
        self.x1, self.y1 = 350, 150
        self.x2, self.y2 = 650, 150
        self.P1 = 0
        self.P2 = 1
        self.frame_k = 0
        self.frame_m = 0
        self.Select = 0
        self.image_m = load_image('resource/Meta_Knight_3.png')
        self.image_k = load_image('resource/Master_Kirby.png')
        self.font = load_font('resource/ENCR10B.TTF', 16)

    def update(self):
        self.frame_k = (self.frame_k + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.frame_m = (self.frame_m + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4




    def draw(self):
        frame_k = int(self.frame_k)
        frame_m = int(self.frame_m)
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2

        if self.P1 == 0:
            self.image_k.clip_draw(K_Standing_focus[frame_k][0], K_Standing_focus[frame_k][1], 35, 45,
                            x1, y1, 35 * 2, 45 * 2)
        elif self.P1 == 1:
            self.image_m.clip_draw(62 * frame_m + M_walking_focus[frame_m][0], 655,M_walking_focus[frame_m][1], 60, x1,
                                   y1, M_walking_focus[frame_m][1] * 2, 60 * 2)

        if self.P2 == 0:
            self.image_k.clip_composite_draw(K_Standing_focus[frame_k][0], K_Standing_focus[frame_k][1], 35, 45,
                                         0, 'h', x2, y2, 35 * 2, 45 * 2)
        elif self.P2 == 1:
            self.image_m.clip_composite_draw(62 * frame_m + M_walking_focus[frame_m][0], 655, M_walking_focus[frame_m][1], 60, 0, 'h', x2, y2,
                               M_walking_focus[frame_m][1] * 2, 60 * 2)



def P1_handle(event):
    if (event.key == SDLK_a or event.key == SDLK_d):
        return True
    return False

def P2_handle(event):
    if (event.key == SDLK_LEFT or event.key == SDLK_RIGHT):
        return True
    return False



def init():
    global B_image
    global Controller
    B_image = load_image('resource/Character_Select_Background.png')
    Controller = P1_Controller()
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

        elif P1_handle(event):

                if event.type == SDL_KEYDOWN and event.key == SDLK_d:
                    Controller.P1 = (Controller.P1 + 1) % 2
                elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
                    Controller.P1 = (Controller.P1 - 1) % 2

        elif P2_handle(event):

            if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
                Controller.P2 = (Controller.P2 + 1) % 2
            elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
                Controller.P2 = (Controller.P2 - 1) % 2


        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(two_player_mode)

    print(f"P1: {Controller.P1}, P2: {Controller.P2}")


def update():
    global P1, P2
    Controller.update()
    P1 = Controller.P1
    P2 = Controller.P2




def draw():
    clear_canvas()
    B_image.clip_draw(0, 0, 1216, 907, 500, 300, 1000, 600)
    Controller.draw()
    update_canvas()
    pass

def pause(): pass

def resume(): pass



K_Standing_focus = [[223, 1195], [268, 1195], [315, 1195], [362, 1195]]
M_walking_focus = [[3, 58], [3, 66], [10, 66], [15, 50], [6, 50], [3, 66], [5, 66]]


