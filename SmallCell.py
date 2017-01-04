import Parameter as pr

class Cell:
    def __init__(self, pos_x, pos_y):
        #self.ID = ID
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sector_no = pr.sector_no
        self.power = pr.Pmax                          # open transmission power to maximum     
        self.max_client_no = pr.max_client_no
        self.radius = pr.radius
        self.X = [0] * self.sector_no               # indicate which sector is opened
        self.client = [[] for _ in range(self.sector_no)]         # record client's "reference" who is under sector i.  i = 0~sector_no  
        

    def power_up(self, n):
        self.power = self.power + n
        
    def power_down(self, n):
        self.power = self.power - n
        
    def is_power_min(self):
        return self.power == pr.Pmin
        
    def add_client(self, sector_no, user):
        self.client[sector_no].append(user)
        
    def get_client_no(self):
        nb = 0
        for sec in self.client:
            nb += len(sec)
        return nb
        
    def get_beam_pattern(self):
        pattern = ''.join([str(int(len(sec) is not 0)) for sec in self.client])[::-1]
        return int(pattern, 2)
        
if __name__ == '__main__':    
    import User as u
    c = Cell(10, 10)
    #c.add_client(0, u.User(10, 10))
    #c.add_client(1, u.User(10, 10))
    #c.add_client(2, u.User(10, 10))
    #c.add_client(3, u.User(10, 10))
    #c.add_client(4, u.User(10, 10))
    
    import read_pattern as rp
    print (c.get_beam_pattern())
    print (rp.beam_gain(c.get_beam_pattern(), 230))
    
    
    
    