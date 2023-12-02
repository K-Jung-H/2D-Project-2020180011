from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_a, SDLK_d, SDLK_LEFT, SDLK_RIGHT

import Mode_Select_mode
import game_framework
import two_player_mode
import stage_select_mode
import Round_score
import BGM_player

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

K_Standing_focus = [[223, 1195], [268, 1195], [315, 1195], [362, 1195]]
M_walking_focus = [[3, 58], [3, 66], [10, 66], [15, 50], [6, 50], [3, 66], [5, 66]]
SK_walk_focus = [[0, 25], [29, 28], [61, 31], [96, 32], [133, 32], [169, 28], [201, 24], [229, 23], [256, 23], [283, 28], [315, 25]] # 11개

Change_focus = [[0, 32], [36, 32], [72, 32], [109, 32]]

P1 = 0
P2 = 0

class P_Controller:
    def __init__(self):
        self.x1, self.y1 = 350, 150
        self.x2, self.y2 = 650, 150
        self.P1 = 0
        self.P2 = 1
        self.frame_k = 0
        self.frame_m = 0
        self.frame_sk = 0
        self.Select = 0
        self.image_Background = load_image('resource/Character_Select_Background.png')
        self.image_black = load_image('resource/black_page.png')
        self.image_k_portrait = load_image('resource/Kirby_Portrait.png')
        self.image_m_portrait = load_image('resource/Meta_Knight_Portrait.png')
        self.image_sk_portrait = load_image('resource/Sword_kirby_Portrait.png')
        self.image_m = load_image('resource/Meta_Knight_3.png')
        self.image_k = load_image('resource/Master_Kirby.png')
        self.image_sk = load_image('resource/Sword_Kirby/Sword_kirby_Walk.png')
        self.image_p1_p2 = load_image('resource/p1_p2.png')

        self.P_image = load_image('resource/change.png')
        self.Pointer_image =  load_image('resource/Pointer.png')

        self.font = load_font('resource/ENCR10B.TTF', 16)

    def update(self):
        self.frame_k = (self.frame_k + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.frame_m = (self.frame_m + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        self.frame_sk = (self.frame_sk + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11


    def draw_background(self):
        self.image_black.clip_draw(0, 0, 100, 100, 500, 300, 1000, 600)
        self.image_Background.clip_draw(0, 0, 1216, 907, 500, 300, 600, 600)

        if self.P1 == 0:
            self.image_k_portrait.clip_draw(0, 0, 451, 480, 100, 500, 200, 200)  # p1 일때 커비
        elif self.P1 == 1:
            self.image_m_portrait.clip_draw(0, 0, 375, 352, 100, 500, 200, 200) # p1 일때 메타 나이트
        elif self.P1 == 2:
            self.image_sk_portrait.clip_draw(0, 0, 221, 244, 100, 500, 200, 200)  # p1 일때 소드 커비


        if self.P2 == 0:
            self.image_k_portrait.clip_composite_draw(0, 0, 451, 480, 0, 'h', 900, 500, 200, 200)  # p2 일때 커비
        elif self.P2 == 1:
            self.image_m_portrait.clip_composite_draw(0, 0, 375, 352, 0, 'h', 900, 500, 200, 200) # p2 일때 메타 나이트
        elif self.P2 == 2:
            self.image_sk_portrait.clip_composite_draw(0, 0, 221, 244, 0, 'h', 900, 500, 200, 200)  # p2 일때 소드 커비




    def draw(self):
        frame_k = int(self.frame_k)
        frame_m = int(self.frame_m)
        frame_sk = int(self.frame_sk)
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
        elif self.P1 == 2:
            self.image_sk.clip_draw(SK_walk_focus[frame_sk][0], 0, SK_walk_focus[frame_sk][1], 41, x1, y1, SK_walk_focus[frame_sk][1] * 2,
                                    41 * 2)


        if self.P2 == 0:
            self.image_k.clip_composite_draw(K_Standing_focus[frame_k][0], K_Standing_focus[frame_k][1], 35, 45,
                                         0, 'h', x2, y2, 35 * 2, 45 * 2)
        elif self.P2 == 1:
            self.image_m.clip_composite_draw(62 * frame_m + M_walking_focus[frame_m][0], 655, M_walking_focus[frame_m][1], 60, 0, 'h', x2, y2,
                               M_walking_focus[frame_m][1] * 2, 60 * 2)
        elif self.P2 == 2:
            self.image_sk.clip_composite_draw(SK_walk_focus[frame_sk][0], 0, SK_walk_focus[frame_sk][1], 41,
                                              0, 'h', x2, y2, SK_walk_focus[frame_sk][1] * 2, 41 * 2)


    def draw_gui(self):
        frame = int(self.frame_sk) % 4
        self.image_p1_p2.clip_draw(0,0, 31, 27, 100, 100, 150, 150 )# p1
        self.image_p1_p2.clip_draw(66,0, 32, 27, 900, 100, 150, 150 )# p1
        self.P_image.clip_draw(Change_focus[frame][0], 0, Change_focus[frame][1], 24, 900, 250, 150, 100)
        self.P_image.clip_composite_draw(Change_focus[frame][0], 0, Change_focus[frame][1], 24, 0, 'h', 100, 250, 150, 100)
        self.Pointer_image.clip_draw(0, 0, 35, 16, 100, 350, 100, 50)
        self.Pointer_image.clip_draw(0, 0, 35, 16, 900, 350, 100, 50)


def P1_handle(event):
    if (event.key == SDLK_a or event.key == SDLK_d):
        return True
    return False

def P2_handle(event):
    if (event.key == SDLK_LEFT or event.key == SDLK_RIGHT):
        return True
    return False



def init():
    global Controller
    global bgm, select_effect
    global bgm_p
    bgm = load_music('resource/sound/Character_Select_bgm.mp3')
    select_effect = load_wav('resource/sound/Space_bar.wav')

    bgm.set_volume(64)
    select_effect.set_volume(64)
    bgm.play()

    Round_score.p1_score = 2
    Round_score.p2_score = 2

    Controller = P_Controller()
    bgm_p = BGM_player.BGM()
    pass

def finish():
    bgm.stop()
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            bgm_p.play(-3)
            game_framework.change_mode(Mode_Select_mode)

        elif P1_handle(event):

                if event.type == SDL_KEYDOWN and event.key == SDLK_d:
                    Controller.P1 = (Controller.P1 + 1) % 3
                elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
                    Controller.P1 = (Controller.P1 - 1) % 3

        elif P2_handle(event):

            if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
                Controller.P2 = (Controller.P2 + 1) % 3
            elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
                Controller.P2 = (Controller.P2 - 1) % 3


        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            select_effect.play()
            delay(1.0)
            game_framework.change_mode(stage_select_mode)


def update():
    global P1, P2
    Controller.update()
    P1 = Controller.P1
    P2 = Controller.P2




def draw():
    clear_canvas()
    Controller.draw_background()
    Controller.draw()
    Controller.draw_gui()
    update_canvas()
    pass

def pause(): pass

def resume(): pass





