from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEBUTTONDOWN

import game_framework
import two_player_character_select_mode
import one_player_character_select_mode
import Title_mode
import guide_mode
import BGM_player


TIME_PER_FRAME = 0.3
FRAME_PER_TIME = 1.0 / TIME_PER_FRAME
FRAMES_PER_BACK_EFFECT = 10


double_kirby = [[0, 34], [48, 34]]
solo_kirby = [[98, 40], [146, 40]]


class Message:
    image = None
    guide = None
    def __init__(self):
        if Message.image == None:
            Message.image = load_image('resource/select_mode_message.png')
            Message.guide = load_image('resource/Guide_message.png')
        self.x = 500
        self.y = 50

        self.gx = 500
        self.gy = 550

        self.start_time = get_time()

    def draw(self):
        if int(get_time() - self.start_time) % 2 == 1:
            self.image.clip_draw(0, 0, 626, 29, self.x, self.y, 600, 50)
        else:
            self.image.clip_draw(0, 30, 626, 59, self.x, self.y, 600, 50)

        if int(get_time() - self.start_time) % 2 == 1:
            self.guide.clip_draw(0, 0, 634, 30, self.gx, self.gy, 600, 50)
        else:
            self.guide.clip_draw(0, 30, 634, 61, self.gx, self.gy, 600, 50)





class Player_Button:
    def __init__(self):
        self.image = load_image('resource/selection.png') # 1002 x 373
        self.select_kirby = load_image('resource/Select.png')
        self.P1_right_pos = 0
        self.P2_left_pos = 1000
        self.selected = None # 선택된 모드
        self.mx = None
        self.my = None
        self.frame = 0


    def update(self):
        self.frame = (self.frame + FRAMES_PER_BACK_EFFECT * FRAME_PER_TIME * game_framework.frame_time) % 6
        self.P1_right_pos += 5
        self.P2_left_pos -= 5
        self.P1_right_pos = clamp(0, self.P1_right_pos, 417)
        self.P2_left_pos = clamp(582, self.P2_left_pos, 1000)

    def draw(self):
        frame = int(self.frame) % 2
        height = 37
        self.select_kirby.clip_draw(double_kirby[frame][0], 0, double_kirby[frame][1], height, self.P2_left_pos + 210, 300, double_kirby[frame][1] * 4,
                             height * 4)
        self.select_kirby.clip_draw(solo_kirby[frame][0], 0, solo_kirby[frame][1], height, self.P1_right_pos - 220, 300,
                                       solo_kirby[frame][1] * 4, height * 4)



def init():
    global Title_image
    global P_B
    global message
    global bgm, bgm_p
    bgm = load_music('resource/sound/Mode_Select_bgm.mp3')
    bgm.set_volume(128)
    bgm.play()

    Title_image = load_image('resource/Kirby_Title.png')
    P_B = Player_Button()
    message = Message()
    bgm_p = BGM_player.BGM()
    pass

def finish():
    bgm.stop()
    pass


def handle_events():
    global P_B
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            esc_effect = load_wav('resource/sound/esc.wav')
            esc_effect.play()
            delay(1.0)
            game_framework.change_mode(Title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_TAB:
            game_framework.change_mode(guide_mode)
            effect1 = load_wav('resource/sound/mode_select.wav')
            effect1.set_volume(64)
            effect1.play()
            delay(1.0)

        elif event.type == SDL_MOUSEBUTTONDOWN:
            P_B.mx, P_B.my = event.x, 600 - 1 - event.y
            if 0 <= P_B.mx <= 417 and 115 <= P_B.my <= 488: # 1인 모드
                game_framework.change_mode(one_player_character_select_mode)
                effect1 = load_wav('resource/sound/mode_select.wav')
                effect1.play()
                delay(1.0)
            elif 582 <= P_B.mx <= 1000 and 115 <= P_B.my <= 488: # 2인 모드
                game_framework.change_mode(two_player_character_select_mode)
                effect1 = load_wav('resource/sound/mode_select.wav')
                effect1.play()
                delay(1.0)



def update():
    P_B.update()
    pass


def draw():
    clear_canvas()
    Title_image.clip_draw(0, 0, 4210, 2571, 500, 300, 1000, 600)
    P_B.image.clip_draw(0, 0, 417, 373, P_B.P1_right_pos - 209, 300, 417, 373) # 0 ~ 417
    P_B.image.clip_draw(582, 0, 420, 373, P_B.P2_left_pos + 210, 300, 420, 373) # 582 ~ 1002
    P_B.draw()


    message.draw()
    update_canvas()
    pass





def pause(): pass

def resume(): pass