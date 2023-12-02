from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, load_font
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT


import game_framework
import one_player_mode
import Mode_Select_mode
import Round_score

K_Standing_focus = [[223, 1195], [268, 1195], [315, 1195], [362, 1195]]
M_walking_focus = [[3, 58], [3, 66], [10, 66], [15, 50], [6, 50], [3, 66], [5, 66]]
SK_walk_focus = [[0, 25], [29, 28], [61, 31], [96, 32], [133, 32], [169, 28], [201, 24], [229, 23], [256, 23], [283, 28], [315, 25]] # 11개


TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

class P_Controller:
    def __init__(self):
        self.x1, self.y1 = 350, 150
        self.x2, self.y2 = 650, 150
        self.P1 = 0
        self.P2 = 0
        self.frame_k = 0
        self.frame_m = 0
        self.frame_sk = 0
        self.Select_side = None
        self.image_Background = load_image('resource/Character_Select_Background.png')
        self.image_black = load_image('resource/black_page.png')
        self.image_gui = load_image('resource/solo_p_gui.png')

        self.image_k_portrait = load_image('resource/Kirby_Portrait.png')
        self.image_m_portrait = load_image('resource/Meta_Knight_Portrait.png')
        self.image_sk_portrait = load_image('resource/Sword_kirby_Portrait.png')
        self.image_m = load_image('resource/Meta_Knight_3.png')
        self.image_k = load_image('resource/Master_Kirby.png')
        self.image_sk = load_image('resource/Sword_Kirby/Sword_kirby_Walk.png')

        self.font = load_font('resource/ENCR10B.TTF', 16)

    def update(self):
        self.frame_k = (self.frame_k + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.frame_m = (self.frame_m + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        self.frame_sk = (self.frame_sk + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11
        print(self.P1, self.P2)


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

        if self.Select_side == 'Left':
            self.image_gui.clip_draw(0, 0, 17, 32, 100, 100, 150, 150)
            self.image_gui.clip_draw(47, 0, 55, 32, 900, 100, 150, 150)
        elif self.Select_side == 'Right':
            self.image_gui.clip_draw(0, 0, 17, 32, 900, 100, 150, 150)
            self.image_gui.clip_draw(47, 0, 55, 32, 100, 100, 150, 150)



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


def init():
    global Controller
    Controller = P_Controller()

    player_character = None

    if Round_score.player_character == 'Master_Kirby':
        player_character = 0
    elif Round_score.player_character == 'Meta_Knight':
        player_character = 1
    elif Round_score.player_character == 'Sword_Kirby':
        player_character = 2

    if Round_score.player_side == 'Left':
        Controller.P1 = player_character
        Controller.Select_side = 'Left'

        if Round_score.difficulty == 1:
            Controller.P2 = 1
            Round_score.Background_stage = 4
        elif Round_score.difficulty == 2:
            Controller.P2 = 2
            Round_score.Background_stage = 1
        elif Round_score.difficulty == 3:
            Controller.P2 = 0
            Round_score.Background_stage = 3

    elif Round_score.player_side == 'Right':
        Controller.P2 = player_character
        Controller.Select_side = 'Right'
        if Round_score.difficulty == 1:
            Controller.P1 = 1
            Round_score.Background_stage = 4
        elif Round_score.difficulty == 2:
            Controller.P1 = 2
            Round_score.Background_stage = 1
        elif Round_score.difficulty == 3:
            Controller.P1 = 0
            Round_score.Background_stage = 3





def finish():
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.change_mode(Mode_Select_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(Mode_Select_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(one_player_mode)



def update():
    global Player
    global Player_side
    global Controller
    Controller.update()




def draw():
    clear_canvas()
    Controller.draw_background()
    Controller.draw()
    update_canvas()
    pass

def pause(): pass

def resume(): pass



