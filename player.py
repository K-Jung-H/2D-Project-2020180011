# 이것은 각 상태들을 객체로 구현한 것임.


from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_f
import World

# state event check
# ( state event type, event value )

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


walking_focus = [[3, 58], [3, 66], [10, 66], [15, 50], [6, 50], [3, 66], [5, 66]]
Normal_Attack_focus = [[110, 50],[220,60],[325, 75],[425,110], [425,110]]

class Idle:

    @staticmethod
    def enter(metaknight, e):
        if metaknight.face_dir == -1:
            metaknight.action = 2
        elif metaknight.face_dir == 1:
            metaknight.action = 3
        metaknight.dir = 0
        metaknight.frame = 0
        metaknight.wait_time = get_time() # pico2d import 필요
        pass

    @staticmethod
    def exit(metaknight, e):
        pass

    @staticmethod
    def do(metaknight):
        metaknight.do_call_count += 1

        if metaknight.do_call_count == 3:
            metaknight.frame = (metaknight.frame + 1) % 4
        metaknight.do_call_count %= 3


    @staticmethod
    def draw(metaknight):
        frame = metaknight.frame
        metaknight.image.clip_draw(62 * frame + walking_focus[frame][0], 655, walking_focus[frame][1], 60, metaknight.x,
                                   metaknight.y, 100, 100)


class Run:

    @staticmethod
    def enter(metaknight, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            metaknight.dir, metaknight.face_dir, metaknight.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            metaknight.dir, metaknight.face_dir, metaknight.action = -1, -1, 0
        metaknight.frame = 0

    @staticmethod
    def exit(metaknight, e):
        pass

    @staticmethod
    def do(metaknight):
        metaknight.do_call_count += 1


        if metaknight.do_call_count == 3:
            metaknight.frame = (metaknight.frame + 1) % 7
        metaknight.do_call_count = metaknight.do_call_count % 3
        metaknight.x += metaknight.dir * 5
        pass

    @staticmethod
    def draw(metaknight):
        frame = metaknight.frame
        metaknight.image.clip_draw(62 * frame + walking_focus[frame][0], 655, walking_focus[frame][1], 60, metaknight.x, metaknight.y, 100, 100)




class Normal_Attack:

    @staticmethod
    def enter(metaknight, e):
        metaknight.frame = 0
        metaknight.do_call_count = 0

    @staticmethod
    def exit(metaknight, e):
        pass

    @staticmethod
    def do(metaknight):
        metaknight.do_call_count += 1

        if metaknight.do_call_count == 3:
            metaknight.frame = (metaknight.frame + 1) % 5
            if metaknight.frame == 4:
                metaknight.state_machine.handle_event(('STOP', 0))
        metaknight.do_call_count = metaknight.do_call_count % 3


    @staticmethod
    def draw(metaknight):
        frame = metaknight.frame
        metaknight.image.clip_draw(Normal_Attack_focus[frame][0], 480, Normal_Attack_focus[frame][1], 60, metaknight.x, metaknight.y, 100, 100)



class StateMachine:
    def __init__(self, metaknight):
        self.metaknight = metaknight
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Idle, right_up: Idle, F_down: Normal_Attack, },
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, F_down: Normal_Attack, F_out: Idle },
            Normal_Attack: {F_out: Idle}

        }

    def start(self):
        self.cur_state.enter(self.metaknight, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.metaknight)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.metaknight, e)
                self.cur_state = next_state
                self.cur_state.enter(self.metaknight, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.metaknight)


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

