class PlayButton:
    def __init__(self, son):
        self.son = son
        self.paused = True

    def rect(self, rect):
        self.rect = rect
        
    def play(self):
        self.son.play()
        self.Paused = False
