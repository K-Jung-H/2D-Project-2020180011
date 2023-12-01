from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time, clamp
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MOUSEBUTTONDOWN, SDL_MOUSEMOTION

import game_framework
import two_player_character_select_mode
import two_player_mode
import Round_score


TIME_PER_FRAME = 0.3
FRAME_PER_TIME = 1.0 / TIME_PER_FRAME
FRAMES_PER_BACK_EFFECT = 10

black_holl = [0, 260, 520, 780, 1040, 1300]
double_kirby = [[0, 34], [48, 34]]



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



class Stage_Selector:
    def __init__(self):
        self.back_image = load_image('resource/Start_Loading_Background.png')
        self.select_kirby = load_image('resource/Select.png')
        self.stage1 = load_image('resource/Stage_Background.png')
        self.stage2 = load_image('resource/Background_Valley.png')
        self.stage3 = load_image('resource/boss_map.png')
        self.stage4 = load_image('resource/Background_Water.png')

        self.s1_x, self.s1_y = 300, 450
        self.s2_x, self.s2_y = 700, 450
        self.s3_x, self.s3_y = 300, 200
        self.s4_x, self.s4_y = 700, 200

        self.selected_map = None # 선택된 맵
        self.Pointed_map = None # 마우스 올려진 맵
        self.mx = None
        self.my = None
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_BACK_EFFECT * FRAME_PER_TIME * game_framework.frame_time) % 6

    def draw_map(self):
        self.stage1.clip_draw(0, 0, 1000, 1000, self.s1_x, self.s1_y, 300, 200)
        self.stage2.clip_draw(0, 0, 1000, 1000, self.s2_x, self.s2_y, 300, 200)
        self.stage3.clip_draw(0, 0, 1000, 1000, self.s3_x, self.s3_y, 300, 200)
        self.stage4.clip_draw(0, 0, 1000, 1000, self.s4_x, self.s4_y, 300, 200)


    def draw_black(self):
        frame = int(self.frame)
        self.back_image.clip_draw(black_holl[frame], 0, 240, 158, 500, 300, 1000, 600)

    def draw_Pointed(self):
        if self.Pointed_map is not None:
            frame = int(self.frame) % 2
            height = 37
            p_x, p_y = 0, 0
            if self.Pointed_map == 1 or self.Pointed_map == 2:
                p_y = 450
            elif self.Pointed_map == 3 or self.Pointed_map == 4:
                p_y = 200

            if self.Pointed_map == 1 or self.Pointed_map == 3:
                p_x = 100
                self.select_kirby.clip_draw(double_kirby[frame][0], 0, double_kirby[frame][1], height,
                                            p_x, p_y, double_kirby[frame][1] * 2, height * 2)
            elif self.Pointed_map == 2 or self.Pointed_map == 4:
                p_x = 900
                self.select_kirby.clip_composite_draw(double_kirby[frame][0], 0, double_kirby[frame][1], height, 0, 'h',
                                            p_x, p_y, double_kirby[frame][1] * 2, height * 2)







def init():
    global S_select
    global message
    S_select = Stage_Selector()
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
            game_framework.change_mode(two_player_character_select_mode)
        elif event.type == SDL_MOUSEMOTION:
            S_select.mx, S_select.my = event.x, 600 - 1 - event.y
            if (300 - 150 <= S_select.mx <= 300 + 150) and (450 - 100 <= S_select.my <= 450 + 100):
                S_select.Pointed_map = 1
            elif (700 - 150 <= S_select.mx <= 700 + 150) and (450 - 100 <= S_select.my <= 450 + 100):
                S_select.Pointed_map = 2
            elif (300 - 150 <= S_select.mx <= 300 + 150) and (200 - 100 <= S_select.my <= 200 + 100):
                S_select.Pointed_map = 3
            elif (700 - 150 <= S_select.mx <= 700 + 150) and (200 - 100 <= S_select.my <= 200 + 100):
                S_select.Pointed_map = 4
            else:
                S_select.Pointed_map = None

        if event.type == SDL_MOUSEBUTTONDOWN and  S_select.Pointed_map is not None:
            Round_score.Background_stage = S_select.Pointed_map
            game_framework.change_mode(two_player_mode)


def update():
    S_select.update()
    pass


def draw():
    clear_canvas()
    S_select.draw_black()
    S_select.draw_map()
    S_select.draw_Pointed()
    message.draw()
    update_canvas()
    pass



def pause(): pass

def resume(): pass