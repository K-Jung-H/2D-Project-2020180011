from pico2d import *
import game_framework

import World
import one_player_character_select_mode
import Title_mode
from Background import BackGround
from player_MetaKnight import MetaKnight
from player_Kirby import Kirby


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
    global Check_Victory

    picked_side = 'p1'
    computer_side = 'p2'

    picked_character = one_player_character_select_mode.Player
    computer_character = 1


    if one_player_character_select_mode.Player_side == 'Left':
        picked_side, computer_side = 'p1', 'p2'
    elif one_player_character_select_mode.Player_side == 'Right':
        picked_side, computer_side = 'p2', 'p1'

    print(picked_side, picked_character)

    if picked_character == 0:
        Player = Kirby(picked_side)
    elif picked_character == 1:
        Player = MetaKnight(picked_side)

    # ai 추가할 부분

    if computer_character == 0:
        Com = Kirby(computer_side)
    elif computer_character == 1:
        Com = MetaKnight(computer_side)

    World.add_object(Player, 1)
    World.add_object(Com, 1)

    World.add_collision_pair('p1 : p2_attack_range', Player, Com.attack_area)
    World.add_collision_pair('p1 : p2_Sword_Skill', Player, None)

    World.add_collision_pair('p2 : p1_attack_range', Com, Player.attack_area)
    World.add_collision_pair('p2 : p1_Sword_Skill', Com, None)

    World.add_collision_pair('p1_Sword_Skill : p2_Sword_Skill', None, None)


    background = BackGround()
    World.add_object(background, 0)

    Check_Victory = KO()


def finish():
    World.clear()
    pass


def update():
    World.update()
    World.handle_collisions()
    Check_Victory.update()
    if Check_Victory.KO_time is not None:
        pass
        #delay(0.1)


def draw():
    clear_canvas()
    World.render()
    Check_Victory.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass


class KO:
    KO_image = None
    def __init__(self):
        if KO.KO_image == None:
            KO.KO_image = load_image('resource/KO.png')
        self.KO_time = None
        self.drawing = False
        self.pos_x = 0
        self.spotlight = 0

    def update(self):
        if Player.Life <= 0 or Com.Life <= 0:
            print("KO")
            self.drawing = True
            if self.pos_x < 500:
                self.pos_x += 10
            else:
                max(self.pos_x, 500)
                if self.KO_time is None:
                    self.KO_time = get_time()

            if self.KO_time is not None:
                self.spotlight += 1
                if get_time() - self.KO_time >= 3:
                    self.KO_time = None
                    self.spotlight = 0
                    game_framework.change_mode(Title_mode)


    def draw(self):
        if self.drawing:
            if self.spotlight % 2 == 0 or self.spotlight > 100:
                self.KO_image.clip_draw(0, 0, 473, 228, self.pos_x, 300, 300, 150)



