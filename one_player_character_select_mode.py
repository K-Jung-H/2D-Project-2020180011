from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, load_font
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT


import game_framework
import one_player_mode
import Mode_Select_mode

K_walk_focus = [[0, 22], [39, 27], [80, 30], [120, 37], [167, 37], [214, 32], [259, 29], [299, 20]]
M_walk_focus = [[2,39], [51,36], [100, 34], [149, 37], [203, 36], [258, 40], [316, 41], [377, 38] ]
SK_walk_focus = [[0, 25], [29, 28], [61, 31], [96, 32], [133, 32], [169, 28], [201, 24], [229, 23], [256, 23], [283, 28], [315, 25]] # 11개


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
        self.image_Background.clip_draw(0, 0, 1495, 998, 500, 300, 600, 600)

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


def init():
    global Controller
    Controller = P1_Controller()


def finish():
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.change_mode(Mode_Select_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        if event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            Controller.P_character = (Controller.P_character + 1) % 3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            Controller.P_character = (Controller.P_character - 1) % 3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT: # 좌측 키세팅 선택
            Controller.P_side = 'Left'
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT: # 우측 키세팅 선택
            Controller.P_side = 'Right'
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(one_player_mode)



def update():
    global Player
    global Player_side
    global Controller
    Controller.update()
    Player = Controller.P_character
    Player_side = Controller.P_side
    print(Player, Player_side)






def draw():
    clear_canvas()
    Controller.draw_background()
    Controller.draw()
    update_canvas()
    pass

def pause(): pass

def resume(): pass



