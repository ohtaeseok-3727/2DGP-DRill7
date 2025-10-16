from Idle import Idle


class State_machine:
    def __init__(self, start_state):
        self.cur_state = start_state # 시작상태 설정
        self.cur_state.enter() # 시작상태 진입
    def update(self):
        self.cur_state.do()
    def draw(self):
        self.cur_state.draw()