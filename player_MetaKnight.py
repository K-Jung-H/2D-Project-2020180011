from pico2d import get_time, load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_f, SDLK_e, SDLK_q, SDLK_s
import World
import game_framework

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

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






walking_focus = [[3, 58], [3, 66], [10, 66], [15, 50], [6, 50], [3, 66], [5, 66]]
Normal_Attack_focus = [[110, 50],[220,60],[325, 75],[425,110], [425,110]]
Speed_Attack_focus = [[2, 50, 485], [2, 50, 485], [755, 110, 480], [2, 100, 405],[110,100,400]]
Charge_Attack_focus = [[2, 50],[110, 50],[220,60],[325, 75],[425,110], [425,110],[540, 100],[540, 100],[540, 100],[645,110]]
Defense_focus = [[445, 30, 340],[498, 35, 340], [540, 35, 340], [592, 42, 330], [636, 42, 340], [0, 50, 210], [50, 50, 210], [113, 50, 210], [163, 50, 210]]



class Idle:

    @staticmethod
    def enter(p1, e):
        p1.dir = 0
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
        p_size_x = walking_focus[frame][1]
        p_size_y = 60
        p1.image.clip_draw(62 * frame + walking_focus[frame][0], 655, walking_focus[frame][1], 60, p1.x,
                                   p1.y, p_size_x * 2, p_size_y * 2)


class Run:

    @staticmethod
    def enter(p1, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            p1.dir, p1.face_dir = 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            p1.dir, p1.face_dir = -1, -1

        p1.frame = 0


    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        p1.x += p1.dir * RUN_SPEED_PPS * game_framework.frame_time
        p1.x = clamp(25, p1.x, 1000 - 25)
        pass

    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = walking_focus[frame][1]
        p_size_y = 60
        p1.image.clip_draw(62 * frame + walking_focus[frame][0], 655, walking_focus[frame][1], 60, p1.x, p1.y, p_size_x * 2, p_size_y * 2)




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
        #p1.x += p1.dir * RUN_SPEED_PPS * game_framework.frame_time
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if int(p1.frame) == 4:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Normal_Attack_focus[frame][1]
        p_size_y = 60
        p1.image.clip_draw(Normal_Attack_focus[frame][0], 480, Normal_Attack_focus[frame][1], 60, p1.x + 30, p1.y, p_size_x * 2, p_size_y * 2)




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
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if int(p1.frame) == 4:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Speed_Attack_focus[frame][1]
        p_size_y = 60
        p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][2], Speed_Attack_focus[frame][1], 60, p1.x + 30, p1.y, p_size_x * 2, p_size_y * 2)



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
            p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        elif  p1.charging == False:
            p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        if int(p1.frame) == 9:
            p1.Attacking = False
            p1.state_machine.handle_event(('STOP', 0))



    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Charge_Attack_focus[frame][1]
        p_size_y = 60
        p1.image.clip_draw(Charge_Attack_focus[frame][0], 480, Charge_Attack_focus[frame][1], 60, p1.x + 30, p1.y, p_size_x * 2, p_size_y * 2)



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
    def __init__(self, meta_knight):
        self.player = meta_knight
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run,
                   F_down: Normal_Attack, E_down: Speed_Attack, Q_down: Charge_Attack, S_down: Defense, },

            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle,
                  F_down: Normal_Attack, E_down: Speed_Attack, Q_down: Charge_Attack, S_down: Defense, },
            Normal_Attack: {STOP: Run, },
            Speed_Attack: {STOP: Run, },
            Charge_Attack: {Q_up: Charge_Attack, STOP: Run, },
            Defense: { STOP: Idle,}


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


class MetaKnight:

    def __init__(self):
        self.x, self.y = 400, 90
        self.do_call_count = 0
        self.frame = 0
        self.dir = 0
        self.charging = False
        self.Attacking = False
        self.face_dir = 1 # 오른쪽 방향으로 얼굴 향하게
        self.image = load_image('resource/Meta_Knight_3.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

