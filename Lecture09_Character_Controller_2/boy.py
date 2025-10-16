from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a
from state_machine import StateMachine

def space_down(e):
   return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def A_clicked(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

class Run:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.on = False
        if right_down(e) or left_up(e):
            self.boy.dir = 1
            self.boy.face_dir = 1
        if left_down(e) or right_up(e):
            self.boy.dir = -1
            self.boy.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        if (self.boy.x > 770): self.boy.x = 770
        if (self.boy.x < 30): self.boy.x = 30
        if(self.boy.x>0 and self.boy.x<800):
            self.boy.x+=self.boy.dir*5
    def draw(self):
        if self.boy.face_dir == 1:  # right
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else:  # face_dir == -1: left
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y)

class Perfect_mode:

    def __init__(self, boy):
        self.boy = boy
        self.boy.wait_start_time = get_time()

    def enter(self, e):
        if A_clicked(e):
            self.boy.on = True
            self.boy.dir = 1
            self.boy.face_dir = 1

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        if (self.boy.x > 770):
            self.boy.x = 770
            self.boy.dir = -1
            self.boy.face_dir = -1
        if (self.boy.x < 30):
            self.boy.x = 30
            self.boy.dir = 1
            self.boy.face_dir = 1
        if(self.boy.x>0 and self.boy.x<800and self.boy.on == True):
            self.boy.x+=self.boy.dir*8
        if(get_time() - self.boy.wait_start_time > 5):
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))
    def draw(self):
        if self.boy.face_dir == 1:  # right
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y+30, 200, 200)
        else:  # face_dir == -1: left
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y+30, 200, 200)


class Sleep:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

    def draw(self):
        if self.boy.face_dir == 1:  # right
            self.boy.image.clip_composite_draw(
                self.boy.frame * 100, 300, 100, 100,  # 소스 영역
                3.141592 / 2,  # 회전 각도
                '',  # 플립 옵션
                self.boy.x, self.boy.y,  # 위치
                100, 100  # 크기
            )
        else:  # face_dir == -1: left
            self.boy.image.clip_composite_draw(
                self.boy.frame * 100, 200, 100, 100,  # 소스 영역
                -3.141592 / 2,  # 회전 각도
                '',  # 플립 옵션
                self.boy.x, self.boy.y,  # 위치
                100, 100  # 크기
            )
class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.on = False
        self.boy.dir = 0
        self.boy.wait_start_time = get_time()

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        if get_time() - self.boy.wait_start_time > 2:
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.boy.face_dir == 1:  # right
            self.boy.image.clip_draw(self.boy.frame * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else:  # face_dir == -1: left
            self.boy.image.clip_draw(self.boy.frame * 100, 200, 100, 100, self.boy.x, self.boy.y)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.on = False
        self.image = load_image('animation_sheet.png')
        # 나머지 초기화 코드

        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)
        self.Run = Run(self)
        self.Perfect_mode = Perfect_mode(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.SLEEP : {space_down : self.IDLE, right_down : self.Run, left_down : self.Run, right_up : self.Run, left_up : self.Run, A_clicked : self.Perfect_mode},
                self.IDLE : {right_down : self.Run, left_down : self.Run, right_up : self.Run, left_up : self.Run, time_out : self.SLEEP, A_clicked : self.Perfect_mode},
                self.Run : {right_up : self.IDLE, left_up : self.IDLE, right_down : self.IDLE, left_down : self.IDLE, A_clicked : self.Perfect_mode},
                self.Perfect_mode : {right_down : self.Run, left_down : self.Run, right_up : self.Run, left_up : self.Run, time_out : self.IDLE}
            }


        )

    def update(self):
        self.state_machine.update()


    def draw(self):
        self.state_machine.draw()
    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
