# 게임 월드 모듈

# 게임 월드 표현

world = [ [], [], [], [], []]

# 게임 월드에 객체 담기
def add_object(o, depth = 0):
    world[depth].append(o) # 지정된 깊이의 레이어에 객체 추가


# 게임 월드 객체들을 전부 업데이트
def update():
    for layer in world:
        for o in layer:
           o.update()


# 게임 월드의 객체들을 전부 그리기
def render():
    for layer in world:
        for o in layer:
            o.draw()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


collision_pairs = {}


def add_collision_pair(group, a, b):

    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)



def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError("왜 존재하지도 않는 걸 지우려 하나요?")

def clear():
    for layer in world:
        layer.clear()
    collision_pairs.clear()