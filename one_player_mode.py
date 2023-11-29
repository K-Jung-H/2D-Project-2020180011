from pico2d import *
import game_framework

import World
import Round_score
import one_player_character_select_mode
import Enemy_matching_mode
import one_player_mode
import Title_mode
from Background import BackGround
from ai_metaknight import MetaKnight as AI_MetaKnight
from ai_sword_kirby import Sword_Kirby as AI_Sword_Kirby
from player_MetaKnight import MetaKnight
from player_Kirby import Kirby
from player_sword_Kirby import Sword_Kirby


def P_handle_L(event):
    if (event.key == SDLK_q or event.key == SDLK_w or event.key == SDLK_a or event.key == SDLK_s
                            or event.key == SDLK_d or event.key == SDLK_e or event.key == SDLK_f):
        return True
    return False

def P_handle_R(event):
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
            game_framework.quit()
        else:
            if P_handle_L(event) and one_player_character_select_mode.Player_side == 'Left':
                Player.handle_event(event)
            elif P_handle_R(event) and one_player_character_select_mode.Player_side == 'Right':
                Player.handle_event(event)


def init():
    global background
    global Player, Com
    global Check_Victory, hp_bar, score
    global p1, p2

    picked_side = None
    computer_side = None

    picked_character = one_player_character_select_mode.Player
    computer_difficulty = Round_score.difficulty
    computer_character = 1

    if one_player_character_select_mode.Player_side == 'Left':
        picked_side, computer_side = 'p1', 'p2'

    elif one_player_character_select_mode.Player_side == 'Right':
        picked_side, computer_side = 'p2', 'p1'



    if picked_character == 0:
        Player = Kirby(picked_side)
    elif picked_character == 1:
        Player = MetaKnight(picked_side)
    elif picked_character == 2:
        Player = Sword_Kirby(picked_side)



    if computer_difficulty == 1:
        Com = AI_MetaKnight(computer_side)
        computer_character = 1
    elif computer_difficulty == 2:
        Com = AI_Sword_Kirby(computer_side)
        computer_character = 2
    # elif computer_difficulty == 3:
    #     Com = AI_Master_Kirby(computer_side)
    #     computer_character = 3


    World.add_object(Player, 1)
    World.add_object(Com, 1)

    if picked_side == 'p1':
        World.add_collision_pair('p1 : p2_attack_range', Player, Com.attack_area)
        World.add_collision_pair('p1 : p2_Sword_Skill', Player, None)

        World.add_collision_pair('p2 : p1_attack_range', Com, Player.attack_area)
        World.add_collision_pair('p2 : p1_Sword_Skill', Com, None)

        World.add_collision_pair('p1_Sword_Skill : p2_Sword_Skill', None, None)

        p1, p2 = Player, Com
    elif picked_side == 'p2':
        World.add_collision_pair('p1 : p2_attack_range', Com, Player.attack_area)
        World.add_collision_pair('p1 : p2_Sword_Skill', Com, None)

        World.add_collision_pair('p2 : p1_attack_range', Player, Com.attack_area)
        World.add_collision_pair('p2 : p1_Sword_Skill', Player, None)

        World.add_collision_pair('p1_Sword_Skill : p2_Sword_Skill', None, None)

        p1, p2 = Com, Player

    background = BackGround()
    World.add_object(background, 0)

    Check_Victory = KO()
    hp_bar = HP_BAR(picked_character, computer_character, picked_side)
    score = Round_score.Score()


def finish():
    World.clear()
    pass


def update():
    World.update()
    World.handle_collisions()
    Check_Victory.update()
    hp_bar.update()



def draw():
    clear_canvas()
    World.render()
    Check_Victory.draw()
    hp_bar.draw()
    score.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass


def Compare_set_win():
    if p1.Life >= p2.Life: # p1이 이겼다면?
        Round_score.p2_score -= 1
    else:
        Round_score.p1_score -= 1


def Compare_game_win():
    if Round_score.p1_score == -1 or Round_score.p2_score == -1:
        if Player.Life >= 0:
            if Round_score.player_side == 'Left':
                Round_score.p1_score += 2
                Round_score.p2_score = 2
            else:
                Round_score.p1_score = 2
                Round_score.p2_score += 2
            Round_score.difficulty += 1
            game_framework.change_mode(Enemy_matching_mode)
        else:
            game_framework.change_mode(Lose_mode)
    else:
        game_framework.change_mode(one_player_mode)


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
            if self.Round_end_time is None: # KO가 아직 안일어났다면 승부 판단
               Compare_set_win()
               self.Round_end_time = get_time()

        # 체력 판별
        if self.Round_end == False:
            if Player.Life <= 0 or Com.Life <= 0:
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
                    if get_time() - self.KO_time >= 3: # 3초만 깜빡이게
                        self.spotlight = 0
                        if self.Round_end_time is None: # 타임 아웃이 안일어났다면 KO 출력 3초후 종료하게
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
    def __init__(self, player_character, com_character, player_side):
        if HP_BAR.HP_image == None:
            HP_BAR.HP_image = load_image('resource/HP_bar.png')
        self.p1_bar_x, self.p1_bar_y = 230, 550
        self.p2_bar_x, self.p2_bar_y = 780, 550
        self.p1_health = 20
        self.p2_health = 20

        self.player_character = player_character
        self.com_character = com_character

        self.p1_character = 0
        self.p2_character = 0
        self.player_side = player_side

        self.metaknight_pic = load_image('resource/Meta_Knight_Portrait.png')
        self.kirby_pic = load_image('resource/Kirby_Portrait.png')
        self.sword_kirby_pic = load_image('resource/Sword_kirby_Portrait.png')


    def update(self):
        if self.player_side == 'p1':
            self.p1_character = self.player_character
            self.p2_character = self.com_character
            self.p1_health = Player.Life
            self.p2_health = Com.Life

        elif self.player_side == 'p2':
            self.p2_character = self.player_character
            self.p1_character = self.com_character
            self.p1_health = Com.Life
            self.p2_health = Player.Life



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

