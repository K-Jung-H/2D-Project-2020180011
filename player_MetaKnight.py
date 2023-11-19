﻿from pico2d import (get_time, load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE,
                    SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN, SDLK_COMMA, SDLK_PERIOD, SDLK_SLASH,
                    SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDLK_f, SDLK_e, SDLK_q, draw_rectangle, load_font )
import World
import game_framework
from M_Sword_Attack import Meta_Knight_Sword_Strike as Sword_Strike

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
FAST_RUN_SPEED_PPS = RUN_SPEED_PPS * 1.8

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 8      # 일반 공격 동작 속도
FRAMES_PER_FAST_ATTACK = 10 # 빠른 공격 동작 속도 더 빠르게
FRAMES_PER_CHARGE_ATTACK = 10
FRAMES_PER_DROP_ATTACK = 12
FRAMES_PER_FALLING_ATTACK = 5


#walking_focus = [[3, 58], [3, 66], [10, 66], [15, 50], [6, 50], [3, 66], [5, 66]]
Normal_Attack_focus = [[110, 50],[220,60],[325, 75],[425,110], [425,110]]
Speed_Attack_focus = [[2, 50, 485], [2, 50, 485], [755, 110, 480], [2, 100, 405],[110,100,400]]
Charge_Attack_focus = [[2, 50],[110, 50],[220,60],[325, 75],[425,110], [425,110],[540, 100],[540, 100],[540, 100],[645,110]]
Defense_focus = [[445, 30, 340],[498, 35, 340], [540, 35, 340], [592, 42, 330], [636, 42, 340], [0, 50, 210], [50, 50, 210], [113, 50, 210], [163, 50, 210]]
Drop_attack_focus = [[0, 28], [48, 26], [96, 26], [136, 28], [188, 27], [242, 30], [290, 37],[355, 27], [405, 27]]
Falling_attack_focus = [[0, 33], [55,32], [112, 34], [166, 37], [227, 33], [284, 33], [339, 32], [396, 34], [451, 32], [509, 32]]
Faf_player_location = [[0,0], [-15, -15], [-25, 0], [0, -5], [-25, -15], [0,0], [-15, -15], [-25, 0], [0,0], [0,0]]




def Right_Move_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_RIGHT or e[1].key == SDLK_d)


def Right_Move_Up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and (e[1].key == SDLK_RIGHT or e[1].key == SDLK_d)


def Left_Move_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_LEFT or e[1].key ==  SDLK_a)


def Left_Move_Up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and (e[1].key == SDLK_LEFT or e[1].key ==  SDLK_a)

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def Jump_Button_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_UP or e[1].key == SDLK_w)

def Time_Out(e):
    return e[0] == 'TIME_OUT'


def Normal_Attack_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_f or e[1].key == SDLK_PERIOD)

def RUN(e):
    return e[0] == 'RUN'

def STOP(e):
    return e[0] == 'STOP'

def Defense_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_s or e[1].key == SDLK_DOWN)

def Defense_Up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and (e[1].key == SDLK_s or e[1].key == SDLK_DOWN)

def Fast_Attack_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_e or e[1].key == SDLK_COMMA)


def Charge_Attack_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_q or e[1].key == SDLK_SLASH)

def Charge_Attack_Up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and (e[1].key == SDLK_q or e[1].key == SDLK_SLASH)


#Air Command

def Upper_Attack_DOWN(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_f or e[1].key == SDLK_PERIOD)
            and e[2] == "Air_Up")

def Drop_Attack_DOWN(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_f or e[1].key == SDLK_PERIOD)
            and e[2] == "Air_Down")

def Falling_Attack_DOWN(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_q or e[1].key == SDLK_SLASH)
            and (e[2] == "Air_Up" or e[2] == "Air_Down"))

#reforged_frame

#start_x, width
Walk_focus = [[2,39], [51,36], [100, 34], [149, 37], [203, 36], [258, 40], [316, 41], [377, 38] ]
Run_focus = [[7,25], [59,23], [100, 34], [147, 23], [189, 23] ]
Fly_focus = [[3, 58], [3, 66], [10, 66], [15, 50], [6, 50], [3, 66], [5, 66]]
Jump_focus = [[9, 32],[57, 27], [101, 28], [143, 26], [187, 26], [230, 26], [274, 27], [315, 27], [357, 28], [401, 32]]
Upper_attack_focus = [[130, 29], [178, 48], [240, 33], [291, 25], [337, 29] ]



class Idle:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        if Right_Move_Down(e):
            p1.Right_Move, p1.dir = True, 1
        if Left_Move_Down(e):
            p1.Left_Move, p1.dir = True, -1
        if Right_Move_Up(e):
            p1.Right_Move, p1.dir = False, 1
        if Left_Move_Up(e):
            p1.Left_Move, p1.dir = False, -1


    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.frame = 0


    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        if p1.dir == 1:
            p1.walk_image.clip_draw(44 * frame, 0, 44, 36, p1.x, p1.y, 44 * 2, 36 * 2)

        elif p1.dir == -1:
            p1.walk_image.clip_composite_draw(44 * frame, 0,44, 36, 0, 'h', p1.x, p1.y, 44 * 2, 36 * 2)


class Walk:
    @staticmethod
    def enter(p1, e):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        if Right_Move_Down(e):
            p1.Right_Move, p1.dir = True, 1

        if Left_Move_Down(e):
            p1.Left_Move, p1.dir = True, -1

        if Right_Move_Up(e):
            p1.Right_Move = False

        if Left_Move_Up(e):
            p1.Left_Move = False

        if p1.Right_Move:
            p1.dir = 1
        elif p1.Left_Move:
            p1.dir = -1


        if Left_Move_Down(e) or Right_Move_Down(e):
            if p1.Last_Input_time == None:
                p1.Last_Input_time = get_time()
                p1.Last_Input_Direction = p1.dir
            else:
                Input_time = get_time() - p1.Last_Input_time
                if Input_time <= 0.5:    # 1초 안에 2번 입력했다면
                    if p1.Last_Input_Direction == p1.dir:  # 이전과 같은 방향 이동을 시도했다면
                        p1.state_machine.handle_event(('RUN', 0))
                        print("Running_Start")
                p1.Last_Input_time = get_time()
                p1.Last_Input_Direction = p1.dir



    @staticmethod
    def exit(p1, e):
        pass



    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        if p1.Left_Move and p1.Right_Move:
            p1.dir = p1.Last_Input_Direction

        elif p1.Left_Move or p1.Right_Move:
            p1.x += p1.dir * RUN_SPEED_PPS * game_framework.frame_time
            p1.x = clamp(25, p1.x, 1000 - 25)

        elif not(p1.Left_Move and p1.Right_Move):
            p1.state_machine.handle_event(('STOP', 0))

    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_start_x = Walk_focus[frame][0]
        p_start_y = 0
        p_width = Walk_focus[frame][1]
        p_height = 36
        if p1.dir == 1:
            p1.walk_image.clip_draw(p_start_x, p_start_y, p_width, p_height, p1.x, p1.y, p_width * 2, p_height * 2)

        elif p1.dir == -1:
            p1.walk_image.clip_composite_draw(p_start_x, p_start_y, p_width, p_height, 0, 'h', p1.x, p1.y, p_width * 2, p_height * 2)


class Run:
    @staticmethod
    def enter(p1, e):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        p1.Last_Input_Direction = None



    @staticmethod
    def exit(p1, e):
        print("Running off")
        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if p1.Left_Move and p1.Right_Move:
            p1.dir = 0

        elif p1.Left_Move or p1.Right_Move:
            p1.x += p1.dir * FAST_RUN_SPEED_PPS * game_framework.frame_time
            p1.x = clamp(25, p1.x, 1000 - 25)

        elif not (p1.Left_Move and p1.Right_Move):
            p1.state_machine.handle_event(('STOP', 0))

    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_start_x = Run_focus[frame][0]
        p_start_y = 0
        p_width = Run_focus[frame][1]
        p_height = 39
        if p1.dir == 1:
            p1.run_image.clip_draw(p_start_x, p_start_y, p_width, p_height, p1.x, p1.y, p_width * 2, p_height * 2)

        elif p1.dir == -1:
            p1.run_image.clip_composite_draw(p_start_x, p_start_y, p_width, p_height, 0, 'h', p1.x, p1.y, p_width * 2,
                                              p_height * 2)

class Jump:
    @staticmethod
    def enter(p1, e):
        if  p1.state_machine.last_state != Jump and p1.state_machine.last_state != Falling_Attack:
            p1.jump_value = 20
            p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7 #10
        else: # 점프 도중에 새로운 입력을 받는 경우
            if Right_Move_Down(e):
                p1.Right_Move, p1.dir = True, 1

            if Left_Move_Down(e):
                p1.Left_Move, p1.dir = True, -1

            if Right_Move_Up(e):
                p1.Right_Move = False

            if Left_Move_Up(e):
                p1.Left_Move = False

            if p1.Right_Move:
                p1.dir = 1
            elif p1.Left_Move:
                p1.dir = -1

            p1.Last_Input_Direction = p1.dir



    @staticmethod
    def exit(p1, e):
        #p1.jump_value = 0
        pass



    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7


        if p1.Left_Move and p1.Right_Move:
            p1.dir = p1.Last_Input_Direction

        elif p1.Left_Move or p1.Right_Move:
            if p1.state_machine.last_state == Walk:
                p1.x += (p1.dir * RUN_SPEED_PPS * game_framework.frame_time) * 2
            elif p1.state_machine.last_state == Run:
                p1.x += (p1.dir * FAST_RUN_SPEED_PPS * game_framework.frame_time) * 2
            elif p1.state_machine.last_state == Jump:
                p1.x += (p1.dir * RUN_SPEED_PPS * game_framework.frame_time)

        p1.x = clamp(25, p1.x, 1000 - 25)

        # 점프: y값 변경
        p1.y += p1.jump_value
        p1.jump_value -= 1
        if p1.y <= 150:  # 나중엔 충돌 체크로 바꿀 것
            p1.y = 150
            p1.state_machine.handle_event(('STOP', 0))





    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_start_x = Jump_focus[frame][0]
        p_start_y = 0
        p_width = Jump_focus[frame][1]
        p_height = 45
        if p1.dir == 1:
            p1.jump_image.clip_draw(p_start_x, p_start_y, p_width, p_height, p1.x, p1.y, p_width * 2, p_height * 2)

        elif p1.dir == -1:
            p1.jump_image.clip_composite_draw(p_start_x, p_start_y, p_width, p_height, 0, 'h', p1.x, p1.y, p_width * 2, p_height * 2)




class Normal_Attack:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.Attacking = True
        p1.frame = (p1.frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 5
        if int(p1.frame) == 4:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Normal_Attack_focus[frame][1]
        p_size_y = 60
        if p1.dir == 1:
            p1.image.clip_draw(Normal_Attack_focus[frame][0], 480, p_size_x, p_size_y, p1.x + 30, p1.y, p_size_x * 2, p_size_y * 2)

        elif p1.dir == -1:
            p1.image.clip_composite_draw(Normal_Attack_focus[frame][0], 480, p_size_x, p_size_y, 0, 'h', p1.x - 30, p1.y,
                               p_size_x * 2, p_size_y * 2)


class Speed_Attack:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.Attacking = True
        p1.frame = (p1.frame + FRAMES_PER_FAST_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 5
        if int(p1.frame) == 4:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Speed_Attack_focus[frame][1]
        p_size_y = 60
        if p1.dir == 1:
            p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][2], p_size_x, p_size_y, p1.x + 30, p1.y, p_size_x * 2, p_size_y * 2)

        elif p1.dir == -1:
            p1.image.clip_composite_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][2], p_size_x, p_size_y,
                               0, 'h', p1.x - 30, p1.y, p_size_x * 2, p_size_y * 2)


class Charge_Attack:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        if Charge_Attack_Down(e):
            p1.charging = True
            p1.Charging_Time = get_time()

        elif Charge_Attack_Up(e):
            p1.charging = False
            p1.Attacking = True

        if Right_Move_Down(e):
            p1.Right_Move, p1.dir = True, 1

        if Left_Move_Down(e):
            p1.Left_Move, p1.dir = True, -1

        if Right_Move_Up(e):
            p1.Right_Move = False

        if Left_Move_Up(e):
            p1.Left_Move = False

        if p1.Right_Move:
            p1.dir = 1
        elif p1.Left_Move:
            p1.dir = -1

    @staticmethod
    def exit(p1, e):
        pass


    @staticmethod
    def do(p1):
        if p1.charging == True:
            p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
            p1.Charging_Point = int(get_time() - p1.Charging_Time)
        elif  p1.charging == False:
            p1.frame = (p1.frame + FRAMES_PER_CHARGE_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 10

        if int (p1.frame) == 5: # 투사체 발사
            if p1.Charging_Point >= 2:
                p1.SwordStrike()
                p1.Charging_Point = 0

        if int(p1.frame) == 9:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Charge_Attack_focus[frame][1]
        p_size_y = 60
        if p1.dir == 1:
            p1.image.clip_draw(Charge_Attack_focus[frame][0], 480, p_size_x, p_size_y, p1.x + 30, p1.y, p_size_x * 2, p_size_y * 2)
        elif p1.dir == -1:
            p1.image.clip_composite_draw(Charge_Attack_focus[frame][0], 480, p_size_x, p_size_y,
                               0, 'h', p1.x - 30, p1.y, p_size_x * 2, p_size_y * 2)

        if p1.charging == True:
            p1.font.draw(p1.x - 10, p1.y + 50, f'{p1.Charging_Point:02d}', (255, 255, 0))



class Upper_Attack:
    @staticmethod
    def enter(p1, e):
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.y += 3
        p1.jump_value -= 0.5
        p1.Attacking = True
        p1.frame = (p1.frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 6
        if int(p1.frame) == 5:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))

    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Upper_attack_focus[frame][1]
        p_size_y = 78
        if p1.dir == 1:
            p1.upper_attack_image.clip_draw(Upper_attack_focus[frame][0], 0, p_size_x, p_size_y, p1.x, p1.y,
                                        p_size_x * 2, p_size_y * 2)

        elif p1.dir == -1:
            p1.upper_attack_image.clip_composite_draw(Upper_attack_focus[frame][0], 0, p_size_x, p_size_y, 0, 'h',
                                        p1.x, p1.y, p_size_x * 2, p_size_y * 2)


class Drop_Attack:
    @staticmethod
    def enter(p1, e):
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):

        p1.Attacking = True
        if int(p1.frame) != 8:
            #p1.y += p1.jump_value
            #p1.jump_value -= 0.5
            p1.frame = (p1.frame + FRAMES_PER_DROP_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 9
        else:
            p1.y += p1.jump_value
            p1.jump_value -= 1

        if p1.y <= 150:
            p1.Attacking = False
            p1.y = 150
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Drop_attack_focus[frame][1]
        p_size_y = 46
        if p1.dir == 1:
            p1.drop_attack_image.clip_draw(Drop_attack_focus[frame][0], 0, p_size_x, p_size_y, p1.x, p1.y,
                                            p_size_x * 2, p_size_y * 2)

        elif p1.dir == -1:
            p1.drop_attack_image.clip_composite_draw(Drop_attack_focus[frame][0], 0, p_size_x, p_size_y, 0, 'h',
                                                      p1.x, p1.y, p_size_x * 2, p_size_y * 2)

class Falling_Attack:
    @staticmethod
    def enter(p1, e):
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):

        p1.Attacking = True
        if int(p1.frame) != 9:
            p1.y += p1.jump_value/10
            p1.jump_value -= 0.1
            p1.frame = (p1.frame + FRAMES_PER_FALLING_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 10
        else:
            p1.state_machine.handle_event(('STOP', 0))

    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Falling_attack_focus[frame][1]
        p_size_y = 40
        p_x = p1.x + Faf_player_location[frame][0] * p1.dir
        p_y = p1.y + Faf_player_location[frame][1]
        if p1.dir == 1:
            p1.falling_attack_image.clip_draw(Falling_attack_focus[frame][0], 0, p_size_x, p_size_y, p_x, p_y,
                                            p_size_x * 2, p_size_y * 2)
        elif p1.dir == -1:
            p1.falling_attack_image.clip_composite_draw(Falling_attack_focus[frame][0], 0, p_size_x, p_size_y, 0, 'h',
                                                        p_x, p_y, p_size_x * 2, p_size_y * 2)




class Defense:

    @staticmethod
    def enter(p1, e):
        waiting_time = int(get_time() - p1.Defense_cooltime)
        print(waiting_time)
        if p1.Defense_cooltime == 0 or waiting_time > 3: # 첫 사용 또는 재사용 대기시간이 지났을 때
            p1.frame = 0
            p1.Defense_time = get_time()

        elif waiting_time <= 3:
            p1.state_machine.handle_event(('STOP', 0))





    @staticmethod
    def exit(p1, e):
        p1.Right_Move = False
        p1.Left_Move = False
        p1.dir = p1.Last_Input_Direction

        if Defense_Up(e):
            p1.Defense_cooltime = get_time()
        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 9
        if int(get_time() - p1.Defense_time) == 5:
            p1.state_machine.handle_event(('STOP', 0))
            p1.Defense_cooltime = get_time()



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Defense_focus[frame][1]
        p_size_y = 70

        if p1.dir == 1:
            p1.image.clip_draw(Defense_focus[frame][0], Defense_focus[frame][2], p_size_x, p_size_y, p1.x + 20, p1.y, p_size_x * 1.8, p_size_y * 1.8)
        elif p1.dir == -1:
            p1.image.clip_composite_draw(Defense_focus[frame][0], Defense_focus[frame][2], p_size_x, p_size_y,
                               0, 'h', p1.x - 20, p1.y, p_size_x * 1.8, p_size_y * 1.8)


class StateMachine:
    def __init__(self, meta_knight):
        self.player = meta_knight
        self.cur_state = Idle
        self.last_state = None
        self.transitions = {
            Idle: { Right_Move_Down: Walk, Left_Move_Down: Walk, Right_Move_Up: Walk, Left_Move_Up: Walk,
                   Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                   Defense_Down: Defense, Jump_Button_Down: Jump},

            Walk: { Right_Move_Down: Idle, Left_Move_Down: Idle, Right_Move_Up: Idle, Left_Move_Up: Idle,
                   Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                   Defense_Down: Defense, STOP: Idle, RUN: Run, Jump_Button_Down: Jump, },

            Run: {Right_Move_Down: Idle, Left_Move_Down: Idle, Right_Move_Up: Idle, Left_Move_Up: Idle,
                  Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                  Defense_Down: Defense, STOP: Idle, Jump_Button_Down: Jump},

            Jump: {STOP: Walk,  Right_Move_Down: Jump, Left_Move_Down: Jump, Right_Move_Up: Jump, Left_Move_Up: Jump,
                   Upper_Attack_DOWN: Upper_Attack, Drop_Attack_DOWN: Drop_Attack, Falling_Attack_DOWN: Falling_Attack },

            #Fly: {},


            Normal_Attack: {STOP: Walk, Right_Move_Down: Walk, Left_Move_Down: Walk, Right_Move_Up: Walk, Left_Move_Up: Walk},

            Speed_Attack: {STOP: Walk, Right_Move_Down: Walk, Left_Move_Down: Walk, Right_Move_Up: Walk, Left_Move_Up: Walk},

            Charge_Attack: {Charge_Attack_Up: Charge_Attack, STOP: Walk,
                            Right_Move_Down: Charge_Attack, Left_Move_Down: Charge_Attack, Right_Move_Up: Charge_Attack, Left_Move_Up: Charge_Attack},

            Upper_Attack: {STOP: Jump, },

            Drop_Attack: { STOP: Idle, },

            Falling_Attack: {STOP: Jump, },

            Defense: { Defense_Up: Idle, STOP: Idle, }


        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)
        #print(self.cur_state)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.last_state = self.cur_state
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)


class MetaKnight:

    def __init__(self, Player = "p1"):
        self.x, self.y = 400, 150
        self.Picked_Player = Player
        if Player == "p1":
            self.dir = 1
        else:
            self.dir = -1
        self.frame = 0

        self.Last_Input_time = None # 대쉬 파악용
        self.Last_Input_Direction = None  # 대쉬 파악용

        self.jump_value = 0 #점프 구현
        self.Defense_time = None # 방어 지속 시간 체크
        self.Defense_cooltime = 0  # 방어 재사용 대기시간
        self.charging = False
        self.Attacking = False
        self.Charging_Point = 0
        self.Charging_Time = 0
        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.Left_Move = False
        self.Right_Move = False
        self.image = load_image('resource/Meta_Knight_3.png')
        self.walk_image = load_image('resource/Meta_Knight_Walk.png')
        self.run_image = load_image('resource/Meta_Knight_Run.png')
        self.jump_image = load_image('resource/Meta_Knight_Jump.png')
        self.upper_attack_image = load_image('resource/Meta_Knight_Upper_Attack.png')
        self.drop_attack_image = load_image('resource/Meta_Knight_Air_Attack.png')
        self.falling_attack_image = load_image('resource/Meta_Knight_Air_Hard_Attack.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if self.jump_value > 0:
            self.state_machine.handle_event(('INPUT', event, "Air_Up"))
            print("command in air")
        elif self.jump_value < 0:
            self.state_machine.handle_event(('INPUT', event, "Air_Down"))
            print("command in air")
        else:
            self.state_machine.handle_event(('INPUT', event, "Ground"))
            print("command on ground")

    def draw(self):
        self.state_machine.draw()
        #남은 체력 표기하기
        #self.font.draw(self.x - 10, self.y + 50, f'{self.Charging_Point:02d}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def SwordStrike(self):
        if self.dir == 1:
            S_S = Sword_Strike(self.x, self.y, self.Charging_Point)
            World.add_object(S_S, 2)
        elif self.dir == -1:
            S_S = Sword_Strike(self.x, self.y, -self.Charging_Point)
            World.add_object(S_S, 2)

    def get_bb(self):

        if self.state_machine.cur_state == Idle:
            if self.Picked_Player == 'p1':
                return self.x - 15, self.y - 25, self.x + 25, self.y + 15
            elif self.Picked_Player == 'p2':
                return self.x - 25, self.y - 25, self.x + 15, self.y + 15

        if self.state_machine.cur_state == Speed_Attack:
            if self.Picked_Player == 'p1':
                return self.x + 25, self.y - 25, self.x + 65, self.y + 20
            elif self.Picked_Player == 'p2':
                return self.x - 65, self.y - 20, self.x - 25, self.y + 20


        elif self.state_machine.cur_state == Walk:
            if self.dir == 1:
                return self.x - 15, self.y - 25, self.x + 25, self.y + 15
            elif self.dir == -1:
                return self.x - 25, self.y - 25, self.x + 15, self.y + 15
            else:
                if self.Picked_Player == 'p1':
                    return self.x - 15, self.y - 25, self.x + 25, self.y + 15
                elif self.Picked_Player == 'p2':
                    return self.x - 25, self.y - 25, self.x + 15, self.y + 15

        elif self.state_machine.cur_state == Normal_Attack:
            if self.Picked_Player == 'p1':
                return self.x + 25, self.y - 25, self.x + 65, self.y + 20
            elif self.Picked_Player == 'p2':
                return self.x - 65, self.y - 20, self.x - 25, self.y + 20

        elif self.state_machine.cur_state == Charge_Attack:
            if self.Picked_Player == 'p1':
                return self.x + 5, self.y - 45, self.x + 65, self.y + 25
            elif self.Picked_Player == 'p2':
                return self.x - 65, self.y - 45, self.x - 5, self.y + 25

        elif self.state_machine.cur_state == Defense:
            if self.Picked_Player == 'p1':
                return self.x - 15, self.y - 45, self.x + 45, self.y + 25
            elif self.Picked_Player == 'p2':
                return self.x - 45, self.y - 45, self.x + 15, self.y + 25

        else:
            return 0,0,0,0
