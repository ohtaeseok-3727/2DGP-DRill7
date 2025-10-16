from pico2d import load_image

from Idle import Idle
from State_machine import State_machine


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.idle = Idle(self)
        self.state_machine= State_machine(self.idle)
    def update(self):
        self.state_machine.update()
    def draw(self):
        self.state_machine.draw()
