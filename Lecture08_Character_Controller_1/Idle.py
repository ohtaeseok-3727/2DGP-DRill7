class Idle:
    def __init__(self, boy):
        self.boy = boy
    def enter(self):
        pass
    def exit(self):
        pass
    def do(self):
        self.boy.frame = (self.boy.frame+1)&8
        pass
    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_draw(self.boy.frame*100, 300, 100, 100, self.boy.x, self.boy.y)
        else:
            self.boy.image.clip_draw(self.boy.frame*100, 200, 100, 100, self.boy.x, self.boy.y)