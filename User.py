
class User:
    def __init__(self, pos_x, pos_y):
        #self.ID = ID
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.snr = 0.
        self.master = None              # put the reference of master
      