from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT

import math
import Round_score
import Enemy_matching_mode
import game_framework
import one_player_mode
import Mode_Select_mode
import BGM_player

K_walk_focus = [[0, 22], [39, 27], [80, 30], [120, 37], [167, 37], [214, 32], [259, 29], [299, 20]]
M_walk_focus = [[2,39], [51,36], [100, 34], [149, 37], [203, 36], [258, 40], [316, 41], [377, 38] ]
SK_walk_focus = [[0, 25], [29, 28], [61, 31], [96, 32], [133, 32], [169, 28], [201, 24], [229, 23], [256, 23], [283, 28], [315, 25]] # 11개
C_list = ['Master_Kirby', 'Meta_Knight', 'Sword_Kirby']


Change_focus = [[0, 32], [36, 32], [72, 32], [109, 32]]



TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

Player = 0
Player_side = None

class P1_Controller:
    def __init__(self):
        self.x, self.y = 500, 150
        self.P_character = 0
        self.P_side = 'Left'
        self.frame_k = 0
        self.frame_m = 0
        self.frame_sk = 0

        self.image_Background = load_image('resource/spot_light_solo.png')
        self.image_black = load_image('resource/black_page.png')
        self.image_k_portrait = load_image('resource/Kirby_Portrait.png')
        self.image_m_portrait = load_image('resource/Meta_Knight_Portrait.png')
        self.image_sk_portrait = load_image('resource/Sword_kirby_Portrait.png')
        self.image_m = load_image('resource/Meta_Knight_Walk.png')
        self.image_k = load_image('resource/Kirby_Walk.png')
        self.image_sk = load_image('resource/Sword_Kirby/Sword_kirby_Walk.png')

        self.font = load_font('resource/ENCR10B.TTF', 16)

    def update(self):
        self.frame_k = (self.frame_k + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.frame_m = (self.frame_m + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        self.frame_sk = (self.frame_sk + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11

    def draw_background(self):
        self.image_black.clip_draw(0, 0, 100, 100, 500, 300, 1000, 600)
        self.image_Background.clip_draw(0, 0, 1495, 998, 500, 280, 600, 500)

        if self.P_side == 'Left':
            if self.P_character == 0:
                self.image_k_portrait.clip_draw(0, 0, 451, 480, 100, 500, 200, 200)  # p1 일때 커비
            elif self.P_character == 1:
                self.image_m_portrait.clip_draw(0, 0, 375, 352, 100, 500, 200, 200)  # p1 일때 메타 나이트
            elif self.P_character == 2:
                self.image_sk_portrait.clip_draw(0, 0, 221, 244, 100, 500, 200, 200)  # p1 일때 소드 커비

        elif self.P_side == 'Right':
            if self.P_character == 0:
                self.image_k_portrait.clip_composite_draw(0, 0, 451, 480, 0, 'h', 900, 500, 200, 200)  # p1 일때 커비
            elif self.P_character == 1:
                self.image_m_portrait.clip_composite_draw(0, 0, 375, 352, 0, 'h', 900, 500, 200, 200) # p1 일때 메타 나이트
            elif self.P_character == 2:
                self.image_sk_portrait.clip_composite_draw(0, 0, 221, 244, 0, 'h', 900, 500, 200, 200)  # p2 일때 소드 커비




    def draw(self):
        #select kirby
        if self.P_character == 0:
            frame = int(self.frame_k)
            p_size_x = K_walk_focus[frame][1]
            p_size_y = 49
            if self.P_side == 'Left':
                self.image_k.clip_draw(K_walk_focus[frame][0], 0, p_size_x, p_size_y, self.x, self.y + 10, p_size_x * 2, p_size_y * 2)
            elif self.P_side == 'Right':
                    self.image_k.clip_composite_draw(K_walk_focus[frame][0], 0, p_size_x, p_size_y, 0, 'h', self.x, self.y + 10, p_size_x * 2, p_size_y * 2)
        #select Meta
        elif self.P_character == 1:
            frame = int(self.frame_m)
            p_start_x = M_walk_focus[frame][0]
            p_size_x = M_walk_focus[frame][1]
            p_size_y = 36
            if self.P_side == 'Left':
                self.image_m.clip_draw(p_start_x, 0, p_size_x, p_size_y, self.x, self.y, p_size_x * 2, p_size_y * 2)
            elif self.P_side == 'Right':
                self.image_m.clip_composite_draw(p_start_x, 0, p_size_x, p_size_y, 0, 'h', self.x, self.y, p_size_x * 2, p_size_y * 2)
        #select SK
        elif self.P_character == 2:
            frame = int(self.frame_sk)
            p_start_x = SK_walk_focus[frame][0]
            p_size_x = SK_walk_focus[frame][1]
            p_size_y = 41
            if self.P_side == 'Left':
                self.image_sk.clip_draw(p_start_x, 0, p_size_x, p_size_y, self.x, self.y, p_size_x * 2, p_size_y * 2)
            elif self.P_side == 'Right':
                self.image_sk.clip_composite_draw(p_start_x, 0, p_size_x, p_size_y, 0, 'h', self.x, self.y, p_size_x * 2, p_size_y * 2)



class UI:
    def __init__(self):
        self.P_image = load_image('resource/change.png')
        self.image_p1_p2 = load_image('resource/p1_p2.png')
        self.Pointer_image =  load_image('resource/Pointer.png')
        self.Direction = None
        self.frame = 0
        self.cx = 500
        self.cy = 530
        self.p1_x = 300
        self.p1_y = 530
        self.p2_x = 700
        self.p2_y = 530

        self.p3_x = 100
        self.p3_y = 300
        self.p4_x = 900
        self.p4_y = 300

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

    def change_icon_draw(self):
        frame = int(self.frame) % 4
        if Player_side == 'Left':
            self.P_image.clip_draw(Change_focus[frame][0], 0, Change_focus[frame][1], 24, self.cx, self.cy, 150, 100)
            self.image_p1_p2.clip_draw(0, 0, 31, 27, 100, 100, 150, 150)
            self.Pointer_image.clip_composite_draw(44, 0, 39, 16,  math.pi/2, 'h', self.p3_x, self.p3_y, 200, 100)

        elif Player_side == 'Right':
            self.P_image.clip_composite_draw(Change_focus[frame][0], 0, Change_focus[frame][1], 24, 0, 'h', self.cx, self.cy, 150, 100)
            self.image_p1_p2.clip_draw(66,0, 32, 27, 900, 100, 150, 150)
            self.Pointer_image.clip_composite_draw(44, 0, 39, 16,  math.pi/2, 'h', self.p4_x, self.p4_y, 200, 100)

        self.Pointer_image.clip_draw(0, 0, 15, 16, self.p1_x, self.p1_y, 100, 100)
        self.Pointer_image.clip_draw(20, 0, 15, 16, self.p2_x, self.p2_y, 100, 100)



def init():
    global Controller, ui
    global bgm, select_effect
    global bgm_p
    bgm = load_music('resource/sound/Character_Select_bgm.mp3')
    select_effect = load_wav('resource/sound/Space_bar.wav')
    bgm.set_volume(64)
    select_effect.set_volume(64)
    bgm.play()
    Controller = P1_Controller()
    ui = UI()
    bgm_p = BGM_player.BGM()

def finish():
    global Controller
    Round_score.player_character = C_list[Controller.P_character]
    Round_score.player_side = Controller.P_side
    Round_score.p1_score = 2
    Round_score.p2_score = 2
    Round_score.difficulty = 1
    bgm.stop()


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            bgm_p.play(-3)
            game_framework.change_mode(Mode_Select_mode)
        if event.type == SDL_KEYDOWN and (event.key == SDLK_UP or event.key == SDLK_w):
            Controller.P_character = (Controller.P_character + 1) % 3
        elif event.type == SDL_KEYDOWN and (event.key == SDLK_DOWN or event.key == SDLK_s):
            Controller.P_character = (Controller.P_character - 1) % 3
        elif event.type == SDL_KEYDOWN and (event.key == SDLK_LEFT or event.key == SDLK_a): # 좌측 키세팅 선택
            Controller.P_side = 'Left'
        elif event.type == SDL_KEYDOWN and (event.key == SDLK_RIGHT or event.key == SDLK_d): # 우측 키세팅 선택
            Controller.P_side = 'Right'
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            select_effect.play()
            delay(0.5)
            game_framework.change_mode(Enemy_matching_mode)



def update():
    global Player
    global Player_side
    global Controller
    Controller.update()
    ui.update()

    Player = Controller.P_character
    Player_side = Controller.P_side







def draw():
    clear_canvas()
    Controller.draw_background()
    Controller.draw()
    ui.change_icon_draw()
    update_canvas()
    pass

def pause(): pass

def resume(): pass



