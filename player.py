from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_f, SDLK_e
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

def F_out(e):
    return e[0] == 'STOP'

def E_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e

def E_out(e):
    return e[0] == 'STOP'


walking_focus = [[3, 58], [3, 66], [10, 66], [15, 50], [6, 50], [3, 66], [5, 66]]
Normal_Attack_focus = [[110, 50],[220,60],[325, 75],[425,110], [425,110]]
Speed_Attack_focus = [[2, 50, 485], [2, 50, 485], [755, 110, 480], [2, 100, 405],[110,100,400]]



class Idle:

    @staticmethod
    def enter(p1, e):
        if p1.face_dir == -1:
            p1.action = 2
        elif p1.face_dir == 1:
            p1.action = 3
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
            p1.dir, p1.face_dir, p1.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            p1.dir, p1.face_dir, p1.action = -1, -1, 0
        p1.frame = 0

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        p1.x += p1.dir * 5
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
        p1.do_call_count = 0

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if int(p1.frame) == 4:
            p1.state_machine.handle_event(('STOP', 0))
        p1.do_call_count = p1.do_call_count % 3

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
        p1.frame = (p1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if int(p1.frame) == 4:
            p1.state_machine.handle_event(('STOP', 0))
        p1.do_call_count = p1.do_call_count % 3


    @staticmethod
    def draw(p1):
        frame = int(p1.frame)
        p_size_x = Speed_Attack_focus[frame][1]
        p_size_y = 60
        p1.image.clip_draw(Speed_Attack_focus[frame][0], Speed_Attack_focus[frame][2], Speed_Attack_focus[frame][1], 60, p1.x + 30, p1.y, p_size_x * 2, p_size_y * 2)


class StateMachine:
    def __init__(self, meta_knight):
        self.player = meta_knight
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Idle, right_up: Idle, F_down: Normal_Attack, E_down: Speed_Attack, E_out: Idle},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, F_down: Normal_Attack, F_out: Idle, E_down: Speed_Attack, E_out: Idle},
            Normal_Attack: {F_out: Idle},
            Speed_Attack: {F_out: Idle},

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
        self.action = 3 # 오른쪽 idle
        self.dir = 0
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

