from pico2d import *

import game_framework
import Round_score
import falling_zone
import World
import two_player_character_select_mode
import Title_mode
import two_player_mode
from Background import BackGround
from player_MetaKnight import MetaKnight
from player_Kirby import Kirby
from player_sword_Kirby import Sword_Kirby


def P1_handle(event):
    if (event.key == SDLK_q or event.key == SDLK_w or event.key == SDLK_a or event.key == SDLK_s
                            or event.key == SDLK_d or event.key == SDLK_e or event.key == SDLK_f):
        return True
    return False

def P2_handle(event):
    if (event.key == SDLK_COMMA or event.key == SDLK_PERIOD or event.key == SDLK_SLASH or event.key == SDLK_UP
                                or event.key == SDLK_DOWN or event.key == SDLK_LEFT or event.key == SDLK_RIGHT):
        return True
    return False


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(two_player_character_select_mode)
        else:
            if P1_handle(event):
                p1.handle_event(event)
            elif P2_handle(event):
                p2.handle_event(event)


def init():
    global background
    global p1, p2
    global picked_p1, picked_p2
    global Check_Victory
    global HP_gui
    global score
    global F_Z

    F_Z = falling_zone.Falling_area(Round_score.Background_stage)
    background = BackGround(500, 300, Round_score.Background_stage)
    World.add_object(background, 0)


    picked_p1 = two_player_character_select_mode.P1
    picked_p2 = two_player_character_select_mode.P2

    if picked_p1 == 0:
        p1 = Kirby("p1")
    elif picked_p1 == 1:
        p1 = MetaKnight("p1")
    elif picked_p1 == 2:
        p1 = Sword_Kirby("p1")

    if picked_p2 == 0:
        p2 = Kirby("p2")
    elif picked_p2 == 1:
        p2 = MetaKnight("p2")
    elif picked_p2 == 2:
        p2 = Sword_Kirby("p2")

    World.add_object(p1, 1)
    World.add_object(p2, 1)

    World.add_collision_pair('p1 : p2_attack_range', p1, p2.attack_area)
    World.add_collision_pair('p1 : p2_Sword_Skill', p1, None)
    World.add_collision_pair('p1 : Falling_area', p1, F_Z)

    World.add_collision_pair('p2 : p1_attack_range', p2, p1.attack_area)
    World.add_collision_pair('p2 : p1_Sword_Skill', p2, None)
    World.add_collision_pair('p2 : Falling_area', p2, F_Z)


    World.add_collision_pair('p1_Sword_Skill : p2_Sword_Skill', None, None)



    HP_gui = HP_BAR()
    Check_Victory = KO()
    score = Round_score.Score()



def finish():
    World.clear()
    pass


def update():
    World.update()
    World.handle_collisions()

    #stage_clamp(Round_score.Background_stage)
    stage_clamp(Round_score.Background_stage)
    Check_Victory.update()
    HP_gui.update()
    F_Z.update()


def draw():
    clear_canvas()
    World.render()
    HP_gui.draw()
    F_Z.draw()
    Check_Victory.draw()
    score.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass


def custom_clamp(value, lower_bound1, upper_bound1, lower_bound2, upper_bound2):
    if lower_bound1 <= value <= upper_bound1:
        return value
    elif lower_bound2 <= value <= upper_bound2:
        return value
    else:
        range1_distance = min(abs(value - lower_bound1), abs(value - upper_bound1))
        range2_distance = min(abs(value - lower_bound2), abs(value - upper_bound2))

        if range1_distance < range2_distance:
            return max(lower_bound1, min(value, upper_bound1))
        else:
            return max(lower_bound2, min(value, upper_bound2))


def stage_clamp(stage_num):
    if stage_num == 1:
        if not p1.Get_Damage:
            p1.x = clamp(80, p1.x, 1000 - 80)
        if not p2.Get_Damage:
            p2.x = clamp(80, p2.x, 1000 - 80)


    elif stage_num == 2:
        if p1.y == 150:
            p1.x = custom_clamp(p1.x, 0, 380, 600, 1000)
        elif (p1.Get_Damage and p1.y < 150):
            p1.x = clamp(400, p1.x, 600)

        if p2.y == 150:
            p2.x = custom_clamp(p2.x, 0, 380, 600, 1000)
        elif (p2.Get_Damage and p2.y < 150):
            p2.x = clamp(400, p2.x, 600)

    elif stage_num == 3:
        p1.x = clamp(20, p1.x, 980)
        p2.x = clamp(20, p2.x, 980)



def Compare_set_win():
    if p1.Life >= p2.Life: # p1이 이겼다면?
        Round_score.p2_score -= 1
    else:
        Round_score.p1_score -= 1


def Compare_game_win():
    if Round_score.p1_score == -1 or Round_score.p2_score == -1:
        game_framework.change_mode(two_player_character_select_mode)
    else:
        game_framework.change_mode(two_player_mode)



class KO:
    KO_image = None
    Time_over_image = None
    def __init__(self):
        if KO.KO_image == None:
            KO.KO_image = load_image('resource/KO.png')
        if KO.Time_over_image == None:
            KO.Time_over_image = load_image('resource/Time_over.png')
        self.font = load_font('resource/ENCR10B.TTF', 70) # 타이머
        self.KO_time = None
        self.KO_drawing = False
        self.pos_x = 0
        self.spotlight = 0

        self.Time_drawing = False
        self.stage_time = 30
        self.remain_time = 0
        self.stage_start_time = get_time()

        self.Round_end = False # 이걸로 해당 라운드 끝났는지 확인
        self.Round_end_time = None

    def update(self):
        # 시간 판별
        if self.Round_end == False:
            self.remain_time = int(self.stage_time - (get_time() - self.stage_start_time))
            self.remain_time = max(0, self.remain_time)
        if self.remain_time == 0:
            self.Round_end = True
            self.Time_drawing = True
            if self.Round_end_time is None:  # KO가 아직 안일어났다면 승부 판단
                Compare_set_win()
                self.Round_end_time = get_time()

        # 체력 판별
        if self.Round_end == False:
            if p1.Life <= 0 or p2.Life <= 0:
                self.KO_drawing = True
                self.Round_end = True

        if self.KO_drawing:
            if self.pos_x < 500:
                self.pos_x += 10
            else:
                max(self.pos_x, 500)
                if self.KO_time is None:
                    Compare_set_win()
                    self.KO_time = get_time()

                if self.KO_time is not None:
                    self.spotlight += 1
                    if get_time() - self.KO_time >= 3:  # 3초만 깜빡이게
                        self.spotlight = 0
                        if self.Round_end_time is None:  # 타임 아웃이 안일어났다면 KO 출력 3초후 종료하게
                            self.Round_end_time = get_time()

        # 3초후 게임 재시작
        if self.Round_end_time is not None:
            if int(get_time() - self.Round_end_time) >= 3:
                Compare_game_win()


    def draw(self):
        if self.KO_drawing:
            if self.spotlight % 2 == 0 or self.spotlight > 100:
                self.KO_image.clip_draw(0, 0, 473, 228, self.pos_x, 300, 300, 150)

        self.font.draw(465, 550, f'{self.remain_time:02d}', (255, 165, 0))

        if self.Time_drawing:
            self.Time_over_image.clip_draw(0, 0, 614, 98, 500, 300, 600, 100)






class HP_BAR:
    HP_image = None
    def __init__(self):
        if HP_BAR.HP_image == None:
            HP_BAR.HP_image = load_image('resource/HP_bar.png')
        self.p1_bar_x, self.p1_bar_y = 230, 550
        self.p2_bar_x, self.p2_bar_y = 780, 550
        self.p1_health = 20
        self.p2_health = 20
        self.p1_character = None
        self.p2_character = None
        self.metaknight_pic = load_image('resource/Meta_Knight_Portrait.png')
        self.kirby_pic = load_image('resource/Kirby_Portrait.png')
        self.sword_kirby_pic = load_image('resource/Sword_kirby_Portrait.png')



    def update(self):
        self.p1_health = p1.Life
        self.p2_health = p2.Life
        self.p1_character = picked_p1
        self.p2_character = picked_p2

        if p1.y <= 50 and p1.Life != 0:
            p1.Life -= 1

        if p2.y <= 50 and p2.Life != 0:
            p2.Life -= 1

    def draw(self):
        self.HP_image.clip_draw(94, 2, 85, 60, self.p1_bar_x + 35 - (20 - self.p1_health) * (370/40), self.p1_bar_y, (370/20) * self.p1_health, 90) # 1p 체력
        self.HP_image.clip_draw(2, 72, 560, 80, self.p1_bar_x, self.p1_bar_y, 450, 100)

        self.HP_image.clip_draw(94, 2, 85, 60, self.p2_bar_x - 30 - (20 - self.p2_health) * (350/40), self.p2_bar_y, (350/20) * self.p2_health, 90) # 2p 체력
        self.HP_image.clip_composite_draw(2, 72, 560, 80, 0, 'h', self.p2_bar_x, self.p2_bar_y, 420, 100)



        # 초상화
        if self.p1_character == 0:
            self.kirby_pic.clip_draw(0, 0, 451, 480, self.p1_bar_x - 195, self.p1_bar_y, 50, 50)  # p1 일때 커비
        elif self.p1_character == 1:
            self.metaknight_pic.clip_draw(0, 0, 375, 352, self.p1_bar_x - 195, self.p1_bar_y, 50, 50) # p1 일때 메타 나이트
        elif self.p1_character == 2:
            self.sword_kirby_pic.clip_draw(0, 0, 221, 244, self.p1_bar_x - 195, self.p1_bar_y, 50, 50)  # p1 일때 소드 커비

        if self.p2_character == 0:
            self.kirby_pic.clip_composite_draw(0, 0, 451, 480, 0, 'h', self.p2_bar_x + 180, self.p2_bar_y, 50, 50)  # p1 일때 커비
        elif self.p2_character == 1:
            self.metaknight_pic.clip_composite_draw(0, 0, 375, 352, 0, 'h', self.p2_bar_x + 180, self.p2_bar_y, 50, 50) # p1 일때 메타 나이트
        elif self.p2_character == 2:
            self.sword_kirby_pic.clip_composite_draw(0, 0, 221, 244, 0, 'h', self.p2_bar_x + 180, self.p2_bar_y, 50, 50)  # p1 일때 소드 커비



