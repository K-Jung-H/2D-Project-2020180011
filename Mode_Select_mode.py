from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, clamp
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEBUTTONDOWN

import game_framework
import two_player_character_select_mode
import one_player_character_select_mode


class Message:
    image = None
    def __init__(self):
        if Message.image == None:
            Message.image = load_image('resource/select_mode_message.png')
        self.x = 500
        self.y = 50
        self.start_time = get_time()

    def draw(self):
        if int(get_time() - self.start_time) % 2 == 1:
            self.image.clip_draw(0, 0, 626, 29, self.x, self.y, 600, 50)
        else:
            self.image.clip_draw(0, 30, 626, 59, self.x, self.y, 600, 50)


class Player_Button:
    def __init__(self):
        self.image = load_image('resource/Player_Button.png') # 1002 x 373
        self.P1_right_pos = 0
        self.P2_left_pos = 1000
        self.selected = None # 선택된 모드
        self.mx = None
        self.my = None


    def update(self):
        self.P1_right_pos += 5
        self.P2_left_pos -= 5
        self.P1_right_pos = clamp(0, self.P1_right_pos, 417)
        self.P2_left_pos = clamp(582, self.P2_left_pos, 1000)



def init():
    global Title_image
    global P_B
    global message
    Title_image = load_image('resource/Kirby_Title.png')
    P_B = Player_Button()
    message = Message()
    pass

def finish():
    pass


def handle_events():
    global P_B
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            P_B.mx, P_B.my = event.x, 600 - 1 - event.y
            if 0 <= P_B.mx <= 417 and 115 <= P_B.my <= 488: # 1인 모드
                game_framework.change_mode(one_player_character_select_mode)
            elif 582 <= P_B.mx <= 1000 and 115 <= P_B.my <= 488: # 2인 모드
                game_framework.change_mode(two_player_character_select_mode)
            else:
                print(P_B.mx, P_B.my)


def update():
    P_B.update()
    pass


def draw():
    clear_canvas()
    Title_image.clip_draw(0, 0, 4210, 2571, 500, 300, 1000, 600)
    P_B.image.clip_draw(0, 0, 417, 373, P_B.P1_right_pos - 209, 300, 417, 373) # 0 ~ 417
    P_B.image.clip_draw(582, 0, 420, 373, P_B.P2_left_pos + 210, 300, 420, 373) # 582 ~ 1002
    message.draw()
    update_canvas()
    pass





def pause(): pass

def resume(): pass