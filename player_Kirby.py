from pico2d import get_time, load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_f, SDLK_e, SDLK_q, SDLK_s, draw_rectangle
import World
import game_framework

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


# Boy Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10


TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 10      # 일반 공격 동작 속도
FRAMES_PER_FAST_ATTACK = 15 # 빠른 공격 동작 속도 더 빠르게



def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

def F_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f

def STOP(e):
    return e[0] == 'STOP'

def S_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def E_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e


def Q_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_q

def Q_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_q





Standing_focus = [[223,1195],[268,1195],[315,1195], [362,1195]]
walking_focus = [[25, 1070], [70, 1070], [111, 1070], [152, 1070], [197, 1070], [240, 1070], ]
Normal_Attack_focus = [[45, 800, 45, 50],[97,800, 60, 50],[160, 800, 60, 50],[227, 800, 45, 50], [290, 800, 55, 50], [362, 785, 90, 50], [455, 785, 95, 50],[555, 785, 70, 50] ]
Speed_Attack_focus = [[40, 700, 55, 50], [105, 700, 55, 50], [165, 700, 55, 50], [230, 700, 75, 50], [310, 695, 65, 50],  [390, 690, 85, 50], [570,616,85,50], [670,616,70,50], ]


#to do

Defense_focus = [[445, 30, 340],[498, 35, 340], [540, 35, 340], [592, 42, 330], [636, 42, 340], [0, 50, 210], [50, 50, 210], [113, 50, 210], [163, 50, 210]]



class Idle:

    @staticmethod
    def enter(p1, e):
        p1.dir = 0
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            p1.Left_Move, p1.Right_Move = False, False
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            p1.Left_Move, p1.Right_Move = False, False
        print('IDLE')
        p1.frame = 0
        p1.wait_time = get_time() # pico2d import 필요
        pass

    @staticmethod
    def exit(p1, e):

        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4


    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = 35
        p_size_y = 45
        p1.image.clip_draw(Standing_focus[frame][0], Standing_focus[frame][1], p_size_x, p_size_y, p1.x,
                                   p1.y, p_size_x * 2, p_size_y * 2)
        draw_rectangle(p1.x - p_size_x, p1.y - p_size_y, p1.x + p_size_x, p1.y + p_size_y)

        # if right_down(e) or left_up(e):  # 오른쪽으로 RUN
        #     p1.Left_Move, p1.Right_Move = False, True
        # elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
        #     p1.Left_Move, p1.Right_Move = True, False


class Run:

    @staticmethod
    def enter(p1, e):
        if right_down(e):
            p1.Right_Move, p1.dir = True, 1
        if left_down(e):
            p1.Left_Move, p1.dir = True, -1
        if right_up(e):
            p1.Left_Move, p1.Right_Move, p1.dir = True, False, -1
        if left_up(e):
            p1.Left_Move, p1.Right_Move, p1.dir = False, True, 1
        # if right_down(e) or left_up(e): # 오른쪽으로 RUN
        #     p1.dir, p1.Left_Move, p1.Right_Move = 1,  False, True
        # elif left_down(e) or right_up(e): # 왼쪽으로 RUN
        #     p1.dir, p1.Left_Move, p1.Right_Move = -1, True, False

        p1.frame = 0


    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):

        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if p1.Left_Move  and p1.Right_Move:
            p1.state_machine.handle_event(('STOP', 0))

        elif p1.Left_Move  or p1.Right_Move:
            p1.x += p1.dir * RUN_SPEED_PPS * game_framework.frame_time
            p1.x = clamp(25, p1.x, 1000 - 25)

        elif not(p1.Left_Move  and p1.Right_Move):
            p1.state_machine.handle_event(('STOP', 0))

        print(p1.Left_Move,p1.Right_Move)


    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = 40
        p_size_y = 45
        p1.image.clip_draw(walking_focus[frame][0], walking_focus[frame][1], p_size_x, p_size_y, p1.x, p1.y, p_size_x * 2, p_size_y * 2)
        draw_rectangle(p1.x - p_size_x, p1.y - p_size_y, p1.x + p_size_x, p1.y + p_size_y)



class Normal_Attack:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        if right_down(e):
            p1.Right_Move =  True
        if left_down(e): p1.Left_Move = True
        if right_up(e): p1.Right_Move =  False
        if left_up(e): p1.Left_Move = False


    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.Attacking = True
        p1.frame = (p1.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 9
        if int(p1.frame) == 8:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Normal_Attack_focus[frame][2]
        p_size_y = Normal_Attack_focus[frame][3]
        if  frame <= 4:
            p1.image.clip_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x, p_size_y, p1.x, p1.y + 10, p_size_x * 2, p_size_y * 2)
        elif frame > 4:
            p1.image.clip_draw(Normal_Attack_focus[frame][0], Normal_Attack_focus[frame][1], p_size_x, p_size_y, p1.x + 5*frame, p1.y -5, p_size_x * 2, p_size_y * 2)
        draw_rectangle(p1.x - p_size_x, p1.y - p_size_y, p1.x + p_size_x, p1.y + p_size_y)



class Speed_Attack:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        p1.do_call_count = 0

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.Attacking = True
        p1.frame = (p1.frame + FRAMES_PER_FAST_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 9
        if int(p1.frame) == 8:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Speed_Attack_focus[frame][2]
        p_size_y = Speed_Attack_focus[frame][3]
        if frame < 3:
            p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y, p1.x, p1.y, p_size_x * 2, p_size_y * 2)
        elif 3 <= frame < 6:
            p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y, p1.x + 10 * frame, p1.y , p_size_x * 2, p_size_y * 2)
        else:
            p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][1], p_size_x, p_size_y, p1.x+ 40, p1.y - 10, p_size_x * 2, p_size_y * 2)


class Charge_Attack:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0
        if Q_down(e):
            p1.charging = True
        elif Q_up(e):
            p1.charging = False
            p1.Attacking = True

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        if p1.charging == True:
            #0,1,2 이후로 차징 모션 3 ~ 6 인덱스 반복 # 그냥 차징 동작, 배기 동작으로 상태를를 나누자
            p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
            p1.frame = max(p1.frame, 3)
        elif  p1.charging == False:
            p1.frame = max(p1.frame, 7)
            p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        if int(p1.frame) == 9:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Charge_Attack_focus[frame][2]
        p_size_y = Charge_Attack_focus[frame][3]
        p1.image.clip_draw(Charge_Attack_focus[frame][0], Charge_Attack_focus[frame][1], p_size_x, p_size_y, p1.x, p1.y, p_size_x * 2, p_size_y * 2)


Charge_Attack_focus = [(140, 566, 60, 40), (205, 560, 65, 40),(275, 560, 75, 40), (355, 560, 45, 40), (405, 560, 45, 40), (460, 560, 45, 40),  (510, 560, 45, 40),   ]



class Defense:

    @staticmethod
    def enter(p1, e):
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 9
        if int(p1.frame) == 8:
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Defense_focus[frame][1]
        p_size_y = 60
        p1.image.clip_draw(Defense_focus[frame][0], Defense_focus[frame][2], Defense_focus[frame][1], 70, p1.x + 30, p1.y, p_size_x * 2, p_size_y * 2)

# 움직이는 방향키에서 반대키 누르면 멈추고 다시 때면 다시 가게 함
# 차징하면서 조금씩 이동 방향으로 움직이게 해볼까
# 움직이면서 공격 기능은 나중에 추가하기


class StateMachine:
    def __init__(self, kirby):
        self.player = kirby
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run,
                   F_down: Normal_Attack, E_down: Speed_Attack, Q_down: Charge_Attack, S_down: Defense, },

            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle,
                  F_down: Normal_Attack, E_down: Speed_Attack, Q_down: Charge_Attack, S_down: Defense, STOP: Idle },
            Normal_Attack: {STOP: Run, },
            Speed_Attack: {STOP: Run, },
            Charge_Attack: {Q_up: Charge_Attack, STOP: Run, },
            Defense: { STOP: Idle, }


        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)


class Kirby:

    def __init__(self):
        self.x, self.y = 400, 150
        self.do_call_count = 0
        self.frame = 0
        self.dir = 0
        self.charging = False
        self.Attacking = False
        self.Left_Move = False
        self.Right_Move = False
        self.face_dir = 1 # 오른쪽 방향으로 얼굴 향하게
        self.image = load_image('resource/Master_Kirby.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

