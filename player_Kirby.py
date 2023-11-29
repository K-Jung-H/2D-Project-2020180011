from pico2d import (get_time, load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE,
                    SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN, SDLK_COMMA, SDLK_PERIOD, SDLK_SLASH,
                    SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDLK_f, SDLK_e, SDLK_q, draw_rectangle, load_font )


import World
import game_framework
from K_Sword_Attack import Master_Kirby_Sword_Strike as Sword_Strike
from K_Attack_Area import Kirby_Attack_Area

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
FAST_RUN_SPEED_PPS = RUN_SPEED_PPS * 1.8



TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10
FRAMES_PER_JUMP_ACTION = 15
FRAMES_PER_FALLING_ATTACK = 10

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 10      # 일반 공격 동작 속도
FRAMES_PER_FAST_ATTACK = 15 # 빠른 공격 동작 속도 더 빠르게
FRAMES_PER_CHARGE_ATTACK = 8
FRAMES_PER_UPPER_ATTACK = 15
FRAMES_PER_DROP_ATTACK = 20



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


def Get_Damage(e):
    return e[0] == 'Damaged'

def RUN(e):
    return e[0] == 'RUN'

def STOP(e):
    return e[0] == 'STOP'

def Normal_Attack_Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_f or e[1].key == SDLK_PERIOD)

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


#reforged
stand_focus = [[0, 32], [44, 33], [92, 30], [139, 31]]
walk_focus = [[0, 22], [39, 27], [80, 30], [120, 37], [167, 37], [214, 32], [259, 29], [299, 20]]
Run_focus = [[0, 34], [41, 30], [83, 29], [122, 34], [165, 30], [210, 34]]
Jump_focus = [[0, 32], [47, 35], [97, 30], [138, 21], [177, 22], [218, 20], [253, 21], [290, 20], [318, 22], [352, 24], [386, 33], [437, 39], [500, 34], [564, 30], [614, 30], [666, 30], [717, 28]]
damaged_focus = [[0, 34], [42, 39]]
Upper_attack_focus = [[0, 24], [42, 24], [92, 24], [144, 28], [210, 50], [299, 56], [387, 76], [489, 80], [606, 92], [739, 20], [804, 26], [867, 28]]
Drop_attack_focus = [[0, 39], [66, 44], [141, 56], [249, 76], [354, 28]] #jump 2,3,4,5,6 이미지 후 연결
Falling_attack_focus = [[0, 53], [54, 53], [110, 53], [116, 53], [218, 53], [277, 53], [331, 53], [386, 53] , [0, 53], [54, 53], [110, 53], [116, 53], [218, 53], [277, 53], [331, 53], [386, 53], [0, 53], [54, 53], [110, 53], [116, 53], [218, 53], [277, 53], [331, 53], [386, 53]] #점프의 12, 13, 14번째 이미지를 쓰고 하기
charge_focus = [[0, 56], [68, 58], [139, 65], [215, 41], [267, 41], [320, 40], [370, 40], [440, 62], [528, 70], [629, 70], [733, 92]]
charge_location = [[-33, -9], [- 35, -9], [-42, -9], [- 18, -9], [ -18, -9], [-17, -9], [-17, -9], [- 16, -9], [- 17 ,-9], [-21, -9], [-21,-9]]
Normal_Attack_focus = [[45, 800, 45, 50],[97,800, 60, 50],[160, 800, 60, 50],[227, 800, 45, 50], [290, 800, 55, 50], [362, 785, 90, 50], [455, 785, 95, 50],[555, 785, 70, 50] ]
Speed_Attack_focus = [[40, 700, 55, 50], [105, 700, 55, 50], [165, 700, 55, 50], [230, 700, 75, 50], [310, 695, 65, 50],  [390, 690, 85, 50], [570,616,85,50], [670,616,70,50], ]
Defense_focus = [[0,23], [29, 26], [61, 30], [98, 18], [122, 24], [152, 32], [189, 22], [218, 24], [250, 25], [282, 25]]


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
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4


    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = stand_focus[frame][1]
        p_size_y = 45
        if p1.dir == 1:
            p1.stand_image.clip_draw(stand_focus[frame][0], 0, p_size_x, p_size_y,
                               p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)

        if p1.dir == -1:
            p1.stand_image.clip_composite_draw(stand_focus[frame][0], 0, p_size_x, p_size_y,
                                         0, 'h', p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)



class Walk:

    @staticmethod
    def enter(p1, e):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
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

        elif not (p1.Left_Move and p1.Right_Move):
            p1.state_machine.handle_event(('STOP', 0))


    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = walk_focus[frame][1]
        p_size_y = 49

        if p1.dir == 1:
            p1.walk_image.clip_draw(walk_focus[frame][0], 0, p_size_x, p_size_y, p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)

        elif p1.dir == -1:
            p1.walk_image.clip_composite_draw(walk_focus[frame][0], 0, p_size_x, p_size_y,
                                         0, 'h', p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)




class Run:
    @staticmethod
    def enter(p1, e):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        p1.Last_Input_Direction = None


    @staticmethod
    def exit(p1, e):
        print("Running off")
        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
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
        p_size_x = Run_focus[frame][1]
        p_size_y = 44
        if p1.dir == 1:
            p1.run_image.clip_composite_draw(Run_focus[frame][0], 0, p_size_x, p_size_y, 0, 'h', p1.x, p1.y + 10,
                                             p_size_x * 2, p_size_y * 2)
        elif p1.dir == -1:
            p1.run_image.clip_draw(Run_focus[frame][0], 0, p_size_x, p_size_y, p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)




class Jump:
    @staticmethod
    def enter(p1, e):
        if p1.state_machine.last_state != Jump and p1.state_machine.last_state != Falling_Attack\
                and p1.state_machine.last_state != Upper_Attack:
            p1.jump_value = 20
            p1.frame = 0
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
        p1.frame = int(p1.frame) % 17



    @staticmethod
    def exit(p1, e):
        #p1.jump_value = 0
        pass



    @staticmethod
    def do(p1):
        if int(p1.frame) != 16:
            p1.frame = (p1.frame + 25 * ACTION_PER_TIME * game_framework.frame_time) % 17


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
        p_height = 54
        if p1.dir == 1:
            p1.jump_image.clip_draw(p_start_x, p_start_y, p_width, p_height, p1.x, p1.y + 10, p_width * 2, p_height * 2)

        elif p1.dir == -1:
            p1.jump_image.clip_composite_draw(p_start_x, p_start_y, p_width, p_height, 0, 'h', p1.x, p1.y + 10, p_width * 2, p_height * 2)


class Hurt:

    @staticmethod
    def enter(p1, e):
        p1.damaged_amount = e[2]
        p1.Life -= p1.damaged_amount
        p1.frame = 0
        p1.jump_value = 5
        p1.y += p1.jump_value
        p1.damaged_time = get_time()

    @staticmethod
    def exit(p1, e):
        p1.jump_value = 0
        p1.damaged_amount = 0
        p1.dir *= -1
        p1.Left_Move = False
        p1.Right_Move = False


    @staticmethod
    def do(p1):
        if int(p1.frame) != 1:
            p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        p1.damaged_motion += 1
        p1.x += p1.dir * RUN_SPEED_PPS * game_framework.frame_time * (p1.damaged_amount * 0.5)
        p1.x = clamp(25, p1.x, 1000 - 25)

        if p1.y > 150:
            p1.y += p1.jump_value
            p1.jump_value -= 1
            p1.y = clamp(150, p1.y, 1000 - 25)

        if get_time() - p1.damaged_time >= 0.2 * p1.damaged_amount:
            if p1.y == 150:
                p1.state_machine.handle_event(('TIME_OUT', 0))


    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = damaged_focus[frame][1]
        p_size_y = 35
        if p1.damaged_motion % 2 == 0:
            if p1.dir == -1:
                p1.damaged_image.clip_draw(damaged_focus[frame][0], 0, p_size_x, p_size_y, p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)

            elif p1.dir == 1:
                p1.damaged_image.clip_composite_draw(damaged_focus[frame][0], 0, p_size_x, p_size_y, 0, 'h', p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)




class Normal_Attack:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        p1.Attacking = False

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 9

        if 5 <= int(p1.frame) <= 7:
            p1.Attacking = True
        else:
            p1.Attacking = False

        if int(p1.frame) == 8:
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Normal_Attack_focus[frame][2]
        p_size_y = Normal_Attack_focus[frame][3]
        if p1.dir == 1:
            if frame <= 4:
                p1.image.clip_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x, p_size_y, p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)
            elif frame > 4:
                p1.image.clip_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x, p_size_y, p1.x + 5*frame, p1.y -5, p_size_x * 2, p_size_y * 2)

        elif p1.dir == -1:
            if frame <= 4:
                p1.image.clip_composite_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x, p_size_y,
                                             0, 'h', p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)
            elif frame > 4:
                p1.image.clip_composite_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x, p_size_y,
                                             0, 'h', p1.x - 5*frame, p1.y -5, p_size_x * 2, p_size_y * 2)


class Speed_Attack:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0


    @staticmethod
    def exit(p1, e):
        p1.Attacking = False

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_FAST_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 9

        if 6 <= int(p1.frame) <= 8:
            p1.Attacking = True
        else:
            p1.Attacking = False

        if int(p1.frame) == 8:
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Speed_Attack_focus[frame][2]
        p_size_y = Speed_Attack_focus[frame][3]

        if p1.dir == 1:
            if frame < 3:
                p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y, p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)
            elif 3 <= frame < 6:
                p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y, p1.x + 10 * frame, p1.y + 10 , p_size_x * 2, p_size_y * 2)
            else:
                p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y, p1.x+ 40, p1.y, p_size_x * 2, p_size_y * 2)
            draw_rectangle(p1.x - 5, p1.y - 45, p1.x + 35, p1.y - 5)
        elif p1.dir == -1:
            if frame < 3:
                p1.image.clip_composite_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y,
                                             0, 'h', p1.x, p1.y, p_size_x * 2, p_size_y * 2)
            elif 3 <= frame < 6:
                p1.image.clip_composite_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y,
                                             0, 'h', p1.x - 10 * frame, p1.y, p_size_x * 2, p_size_y * 2)
            else:
                p1.image.clip_composite_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y,
                                             0, 'h', p1.x - 40, p1.y - 10, p_size_x * 2, p_size_y * 2)



class Charge_Attack:

    @staticmethod
    def enter(p1, e):
        if Charge_Attack_Down(e):
            p1.frame = 0
            p1.charging = True
            p1.Charging_Time = get_time()

        elif Charge_Attack_Up(e):
            p1.charging = False
            p1.Attacking = True

        if Right_Move_Down(e) and p1.charging:
            p1.Right_Move, p1.dir = True, 1

        if Left_Move_Down(e) and p1.charging:
            p1.Left_Move, p1.dir = True, -1

        if Right_Move_Up(e) and p1.charging:
            p1.Right_Move = False

        if Left_Move_Up(e) and p1.charging:
            p1.Left_Move = False

        if p1.Right_Move:
            p1.dir = 1
        elif p1.Left_Move:
            p1.dir = -1
            

            
    @staticmethod
    def exit(p1, e):
        p1.Attacking = False

    @staticmethod
    def do(p1):

        if not (p1.charging or p1.Attacking) and int(p1.frame) < 3: #차징 준비 동작
            p1.frame = (p1.frame + FRAMES_PER_CHARGE_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 4
            if int(p1.frame) == 3:
                p1.charging = True
        elif p1.charging:   #차징
            p1.frame = max(3, p1.frame)
            p1.frame = (p1.frame + FRAMES_PER_CHARGE_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 7
            p1.frame = max(3, p1.frame)
            p1.Charging_Point = int(get_time() - p1.Charging_Time)
        elif not p1.charging:
            p1.frame = max(p1.frame, 7)
            p1.frame = (p1.frame + FRAMES_PER_CHARGE_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 12
        if int(p1.frame) == 11:
            if p1.Charging_Point >= 1:
                p1.SwordStrike()
                p1.Charging_Point = 0
            p1.state_machine.handle_event(('STOP', 0))

        if 8 <= int(p1.frame) <= 10:
            p1.Attacking = True
        else:
            p1.Attacking = False

    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = charge_focus[frame][1]
        p_size_y = 60
        if p1.dir == 1:
            p1.charge_attack_image.clip_draw(charge_focus[frame][0], 0, p_size_x, p_size_y, p1.x + charge_location[frame][0],
                                             p1.y + 10, p_size_x * 2, p_size_y * 2)

        elif p1.dir == -1:
            p1.charge_attack_image.clip_composite_draw(charge_focus[frame][0], 0, p_size_x, p_size_y,
                                         0, 'h', p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)

        if p1.charging == True:
            p1.font.draw(p1.x - 10, p1.y + 50, f'{p1.Charging_Point:02d}', (255, 255, 0))




class Defense:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        p1.Right_Move = False
        p1.Left_Move = False
        p1.Defensing = False
        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        p1.Defensing = True
        if int(p1.frame) == 9:
            p1.Defensing = False
            p1.state_machine.handle_event(('STOP', 0))

    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Defense_focus[frame][1]
        p_size_y = 22
        if p1.dir == 1:
            p1.defense_image.clip_draw(Defense_focus[frame][0], 0, p_size_x, p_size_y, p1.x, p1.y,
                               p_size_x * 2, p_size_y * 2)

        elif p1.dir == -1:
            p1.defense_image.clip_composite_draw(Defense_focus[frame][0], 0, p_size_x, p_size_y,
                                         0, 'h', p1.x, p1.y, p_size_x * 2, p_size_y * 2)



class Upper_Attack:
    @staticmethod
    def enter(p1, e):
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        p1.Attacking = False

    @staticmethod
    def do(p1):

        if (4 <= int(p1.frame) <= 8):
            p1.y += 10
        else:
            p1.y += 1
        p1.jump_value -= 0.1

        p1.frame = (p1.frame + FRAMES_PER_UPPER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 12
        if int(p1.frame) == 11:

            p1.state_machine.handle_event(('STOP', 0))

        if 4 <= int(p1.frame) <= 9:
            p1.Attacking = True
        else:
            p1.Attacking = False



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Upper_attack_focus[frame][1]
        p_size_y = 79
        if p1.dir == 1:
            p1.upper_attack_image.clip_draw(Upper_attack_focus[frame][0], 0, p_size_x, p_size_y, p1.x, p1.y,
                                        p_size_x * 2, p_size_y * 2)

        elif p1.dir == -1:
            p1.upper_attack_image.clip_composite_draw(Upper_attack_focus[frame][0], 0, p_size_x, p_size_y, 0, 'h',
                                        p1.x, p1.y, p_size_x * 2, p_size_y * 2)



class Drop_Attack:
    @staticmethod
    def enter(p1, e):
        if Drop_Attack_DOWN(e):
            p1.frame = 0
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
        p1.Attacking = False

    @staticmethod
    def do(p1):
        if int(p1.frame) <= 4:
            p1.frame = (p1.frame + FRAMES_PER_DROP_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 10
        elif int(p1.frame) <= 8:
            p1.frame = (p1.frame + FRAMES_PER_DROP_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 10
            p1.jump_value -= 0.5
        else:
            p1.y += p1.jump_value
            p1.jump_value -= 1.5

        if p1.y <= 150:
            p1.Attacking = False
            p1.y = 150
            p1.state_machine.handle_event(('STOP', 0))

        if 4 <= int(p1.frame) <= 9:
            p1.Attacking = True
        else:
            p1.Attacking = False



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)


        if frame <= 4:
            p_start_x = Jump_focus[frame][0]
            p_start_y = 0
            p_width = Jump_focus[frame][1]
            p_height = 54
            if p1.dir == 1:
                p1.jump_image.clip_draw(p_start_x, p_start_y, p_width, p_height, p1.x, p1.y, p_width * 2, p_height * 2)

            elif p1.dir == -1:
                p1.jump_image.clip_composite_draw(p_start_x, p_start_y, p_width, p_height, 0, 'h', p1.x, p1.y,
                                                  p_width * 2, p_height * 2)
        else:
            frame = frame - 5
            p_size_x = Drop_attack_focus[frame][1]
            p_size_y = 86
            if p1.dir == 1:
                p1.drop_attack_image.clip_draw(Drop_attack_focus[frame][0], 0, p_size_x, p_size_y, p1.x, p1.y,
                                                p_size_x * 2, p_size_y * 2)

            elif p1.dir == -1:
                p1.drop_attack_image.clip_composite_draw(Drop_attack_focus[frame][0], 0, p_size_x, p_size_y, 0, 'h',
                                                          p1.x, p1.y, p_size_x * 2, p_size_y * 2)


class Falling_Attack:
    @staticmethod
    def enter(p1, e):
        if p1.state_machine.last_state != Falling_Attack:
            p1.frame = 0
        else: # 공격 도중에 새로운 입력을 받는 경우
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
        p1.Attacking = False

    @staticmethod
    def do(p1):

        if p1.Left_Move and p1.Right_Move:
            p1.dir = p1.Last_Input_Direction

        elif p1.Left_Move or p1.Right_Move:
                p1.x += (p1.dir * RUN_SPEED_PPS * game_framework.frame_time)
        p1.x = clamp(25, p1.x, 1000 - 25)


        if int(p1.frame) != 26:
            p1.y += p1.jump_value/10
            p1.jump_value -= 0.1
            p1.frame = (p1.frame + 50 * ACTION_PER_TIME * game_framework.frame_time) % 27
        else:
            p1.state_machine.handle_event(('STOP', 0))

        if p1.y <= 150:
            p1.Attacking = False
            p1.y = 150
            p1.state_machine.handle_event(('STOP', 0))

        if 4 <= int(p1.frame) <= 25:
            p1.Attacking = True
        else:
            p1.Attacking = False

    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        if frame <= 2:
            p_start_x = Jump_focus[frame][0]
            p_start_y = 0
            p_width = Jump_focus[frame][1]
            p_height = 54
            if p1.dir == 1:
                p1.jump_image.clip_draw(p_start_x, p_start_y, p_width, p_height, p1.x, p1.y, p_width * 2, p_height * 2)

            elif p1.dir == -1:
                p1.jump_image.clip_composite_draw(p_start_x, p_start_y, p_width, p_height, 0, 'h', p1.x, p1.y,
                                                  p_width * 2, p_height * 2)
        else:
            frame = frame - 3
            p_size_x = Falling_attack_focus[frame][1]
            p_size_y = 53
            if p1.dir == 1:
                p1.falling_attack_image.clip_draw(Falling_attack_focus[frame][0], 0, p_size_x, p_size_y, p1.x, p1.y,
                                                p_size_x * 2, p_size_y * 2)
            elif p1.dir == -1:
                p1.falling_attack_image.clip_composite_draw(Falling_attack_focus[frame][0], 0, p_size_x, p_size_y, 0, 'h',
                                                            p1.x, p1.y, p_size_x * 2, p_size_y * 2)



class StateMachine:
    def __init__(self, kirby):
        self.player = kirby
        self.cur_state = Idle
        self.last_state = None
        self.transitions = {
            Idle: {Right_Move_Down: Walk, Left_Move_Down: Walk, Right_Move_Up: Walk, Left_Move_Up: Walk,
                   Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                   Defense_Down: Defense, Jump_Button_Down: Jump, Get_Damage: Hurt, },

            Walk: {Right_Move_Down: Idle, Left_Move_Down: Idle, Right_Move_Up: Idle, Left_Move_Up: Idle,
                   Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                   Defense_Down: Defense, STOP: Idle, RUN: Run, Jump_Button_Down: Jump, Get_Damage: Hurt, },

            Run: {Right_Move_Down: Idle, Left_Move_Down: Idle, Right_Move_Up: Idle, Left_Move_Up: Idle,
                  Normal_Attack_Down: Normal_Attack, Fast_Attack_Down: Speed_Attack, Charge_Attack_Down: Charge_Attack,
                  Defense_Down: Defense, STOP: Idle, Jump_Button_Down: Jump, Get_Damage: Hurt, },

            Jump: {STOP: Walk, Right_Move_Down: Jump, Left_Move_Down: Jump, Right_Move_Up: Jump, Left_Move_Up: Jump,
                   Upper_Attack_DOWN: Upper_Attack, Drop_Attack_DOWN: Drop_Attack, Falling_Attack_DOWN: Falling_Attack,
                   Get_Damage: Hurt, },

            Hurt: {Time_Out: Idle, },

            Normal_Attack: {STOP: Walk, Right_Move_Down: Walk, Left_Move_Down: Walk, Right_Move_Up: Walk,
                            Left_Move_Up: Walk, Get_Damage: Hurt},

            Speed_Attack: {STOP: Walk, Right_Move_Down: Walk, Left_Move_Down: Walk, Right_Move_Up: Walk,
                           Left_Move_Up: Walk, Get_Damage: Hurt},

            Charge_Attack: {Charge_Attack_Up: Charge_Attack, STOP: Walk,
                            Right_Move_Down: Charge_Attack, Left_Move_Down: Charge_Attack, Right_Move_Up: Charge_Attack,
                            Left_Move_Up: Charge_Attack, Get_Damage: Hurt},

            Upper_Attack: {STOP: Jump, Get_Damage: Hurt, },

            Drop_Attack: {STOP: Walk, Right_Move_Down: Drop_Attack, Left_Move_Down: Drop_Attack,
                          Right_Move_Up: Drop_Attack, Left_Move_Up: Drop_Attack, Get_Damage: Hurt, },

            Falling_Attack: {STOP: Jump, Right_Move_Down: Falling_Attack, Left_Move_Down: Falling_Attack,
                             Right_Move_Up: Falling_Attack, Left_Move_Up: Falling_Attack, Get_Damage: Hurt},

            Defense: {Defense_Up: Idle, STOP: Idle, Get_Damage: Hurt}

        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)
        self.player.attack_area.update(self.cur_state)

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
        self.player.attack_area.draw()
        self.player.font.draw(self.player.x - 10, self.player.y + 60, f'{self.player.Life:02d}', (255, 0, 0))


class Kirby:

    def __init__(self, Player = "p1"):
        self.x, self.y = 400, 150
        self.Life = 20
        self.damaged_amount = 0
        self.Picked_Player = Player
        if Player == "p1":
            self.dir = 1
            self.x, self.y = 200, 150
        else:
            self.dir = -1
            self.x, self.y = 800, 150
        self.frame = 0

        self.Last_Input_time = None # 대쉬 파악용
        self.Last_Input_Direction = None  # 대쉬 파악용

        self.jump_value = 0 #점프 구현
        self.Defensing = False
        self.Defense_time = None # 방어 지속 시간 체크
        self.Defense_cooltime = 0  # 방어 재사용 대기시간

        self.attack_area = Kirby_Attack_Area(self)
        self.Attacking = False
        self.charging = False
        self.Charging_Point = 0
        self.Charging_Time = 0

        self.damaged_time = None # 맞은 시점
        self.damaged_motion = 1
        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.Left_Move = False
        self.Right_Move = False
        self.image = load_image('resource/Master_Kirby.png')
        self.stand_image = load_image('resource/Kirby_Stand.png')
        self.walk_image = load_image('resource/Kirby_Walk.png')
        self.run_image = load_image('resource/Kirby_Run.png')
        self.jump_image = load_image('resource/Kirby_Jump.png')
        self.damaged_image = load_image('resource/Kirby_Damaged.png')
        self.defense_image = load_image('resource/Sword_Kirby/Defense_Kirby.png')
        self.charge_attack_image = load_image('resource/Kirby_Charge_Attack.png')
        self.upper_attack_image = load_image('resource/Kirby_Upper_Attack.png')
        self.drop_attack_image = load_image('resource/Kirby_Drop_Attack.png')
        self.falling_attack_image = load_image('resource/Kirby_Falling_Attack.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if self.jump_value > 0:
            self.state_machine.handle_event(('INPUT', event, "Air_Up"))
        elif self.jump_value < 0:
            self.state_machine.handle_event(('INPUT', event, "Air_Down"))
        else:
            self.state_machine.handle_event(('INPUT', event, "Ground"))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())


    def SwordStrike(self):
        K_S_S = Sword_Strike(self.x, self.y, self.Charging_Point * self.dir)
        World.add_object(K_S_S, 2)
        if self.Picked_Player == 'p1':
            World.add_collision_pair('p2 : p1_Sword_Skill', None, K_S_S)
            World.add_collision_pair('p1_Sword_Skill : p2_Sword_Skill', K_S_S, None)
        elif self.Picked_Player == 'p2':
            World.add_collision_pair('p1 : p2_Sword_Skill', None, K_S_S)
            World.add_collision_pair('p1_Sword_Skill : p2_Sword_Skill', None, K_S_S)




    def get_bb(self):
        if self.state_machine.cur_state == Idle:
            if self.dir == 1:
                return self.x - 12, self.y - 35, self.x + 32, self.y + 5
            elif self.dir == -1:
                return self.x - 32, self.y - 35, self.x + 12, self.y + 5

        elif self.state_machine.cur_state == Walk or self.state_machine.cur_state == Run:
            if self.dir == 1:
                return self.x - 12, self.y - 35, self.x + 32, self.y + 5
            elif self.dir == -1:
                return self.x - 32, self.y - 35, self.x + 12, self.y + 5
            else:
                if self.Last_Input_Direction == 1:
                    return self.x - 12, self.y - 35, self.x + 32, self.y + 5
                elif self.Last_Input_Direction == -1:
                    return self.x - 32, self.y - 35, self.x + 12, self.y + 5


        elif self.state_machine.cur_state == Jump: # 점프 상황에서 피격 범위만 정하면 끝
            if self.dir == 1:
                return self.x - 12, self.y - 35, self.x + 32, self.y + 5
            elif self.dir == -1:
                return self.x - 32, self.y - 25, self.x + 12, self.y + 45
            else:
                if self.Last_Input_Direction == 1:
                    return self.x - 12, self.y - 35, self.x + 32, self.y + 5
                elif self.Last_Input_Direction == -1:
                    return self.x - 32, self.y - 35, self.x + 12, self.y + 5


        elif self.state_machine.cur_state == Normal_Attack:
            if self.dir == 1:
                return self.x - 35, self.y - 45, self.x + 35, self.y + 15
            elif self.dir == -1:
                return self.x - 45, self.y - 45, self.x + 25, self.y + 15

        elif self.state_machine.cur_state == Charge_Attack:
            if self.dir == 1:
                return self.x - 35, self.y - 45, self.x + 25, self.y + 15
            elif self.dir == -1:
                return self.x - 35, self.y - 45, self.x + 25, self.y + 15

        elif self.state_machine.cur_state == Defense:
            if self.dir == 1:
                return self.x - 25, self.y - 30, self.x + 25, self.y + 20
            elif self.dir == -1:
                return self.x - 25, self.y - 30, self.x + 25, self.y + 20

        elif self. state_machine.cur_state == Upper_Attack:
            return self.x - 20, self.y - 60, self.x + 20, self.y - 20

        elif self.state_machine.cur_state == Drop_Attack:
            return self.x - 20, self.y - 40, self.x + 20, self.y + 10

        elif self.state_machine.cur_state == Falling_Attack:
            return self.x - 20, self.y - 20, self.x + 20, self.y + 20


        else:
            return 0, 0, 0, 0


    def handle_collision(self, group, other):
        if self.Picked_Player == "p1":
            if group == 'p1 : p2_attack_range' or group == 'p1 : p2_Sword_Skill':
                if other.Attacking:
                    # 직접적인 공격 받고, 강공격이 아니라면 반사하기
                    if self.Defensing and group == 'p1 : p2_attack_range' and other.charge_attack == False:
                        print("p1 Defensed")
                        other.p.state_machine.handle_event(('Damaged', 0, other.power))
                        other.p.dir = self.dir
                    else:
                        if other.power != 0:
                            print("p1 is damaged")
                            self.state_machine.handle_event(('Damaged', 0, other.power))
                            self.dir = other.p_dir

        else:
            if group == 'p2 : p1_attack_range' or group == 'p2 : p1_Sword_Skill':
                if other.Attacking:
                    if other.Attacking:
                        # 직접적인 공격 받고, 강공격이 아니라면 반사하기
                        if self.Defensing and group == 'p2 : p1_attack_range' and other.charge_attack == False:
                            print("p2 Defensed")
                            other.p.state_machine.handle_event(('Damaged', 0, other.power))
                            other.p.dir = self.dir
                        else:
                            if other.power != 0:
                                print("p2 is damaged")
                                self.state_machine.handle_event(('Damaged', 0, other.power))
                                self.dir = other.p_dir


    def remove(self):
        self.attack_area = None
        del self
