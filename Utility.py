import Parameter as pr
import random as rd
from math import sqrt, pi, degrees, atan2, log, pow
import SmallCell as sc
import User as ur
import matplotlib.pyplot as plt
import read_pattern as rp


def load_pos_cell():
    pos = []
    with open(pr.fn_pos_bs, 'r') as f:
        for line in f:
            parts = line.split()
            pos.append([float(e) for e in parts])
    return pos

def load_pos_user():
    pos = []
    with open(pr.fn_pos_ue, 'r') as f:
        for line in f:
            parts = line.split(',')
            pos.append([float(e) for e in parts])
    return pos

def get_snr(cell, user, cm, isInterfere, isAddGain):        # return power ratio not db
    def dbm2mwatt(dbm):
        return pow(10, dbm/10.)         
    def ratio2db(ratio):        # SNR in db
        return 10 * log(ratio, 10)            
    def get_pathloss(dist):     # db
        dist = pr.ref_dist if dist < pr.ref_dist else dist
        return pr.gamma * 10 * log((dist/pr.ref_dist), 10) + pr.Pref
    
    dist = get_dist(cell.pos_x, cell.pos_y, user.pos_x, user.pos_y)
    gain = rp.beam_gain(cell.get_beam_pattern(), get_angle(cell, user)) if isAddGain else 0
    
    signal_power = dbm2mwatt(cell.power - get_pathloss(dist) + gain)    # in watt
    interfere_power = 0. if len(cm)!=1 else 0.01                        # in watt
    for e in cm:
        if e is cell:
            continue
        dist = get_dist(e.pos_x, e.pos_y, user.pos_x, user.pos_y)
        interfere_power += dbm2mwatt(e.power - get_pathloss(dist))
    #interfere_power += dbm2mwatt(pr.gaussian_noise)    
    interfere_power = interfere_power if isInterfere else 1.    
    return  (signal_power / interfere_power) * pr.interfereReduction   
    

def get_angle(cell, user):      # get angle between one cell and one user. 假想cell在中心，求user在cell的甚麼方向，若user在cell的頭頂則為0度、若再cell的右方則90度、若左方則270度
    x1 = cell.pos_x  
    y1 = cell.pos_y 
    x2 = user.pos_x
    y2 = user.pos_y
    
    dx = x2 - x1
    dy = y2 - y1
    rads = atan2(dx,dy)
    rads %= 2*pi
    degs = degrees(rads)
    return degs
    
    
def get_region_no(cell, user):
    angle = get_angle(cell, user)
    if 36 <= angle < 108:
        return 1        #sector A2
    elif 108 <= angle < 180:
        return 2
    elif 180 <= angle < 252:
        return 3
    elif 252 <= angle < 324:
        return 4
    else:
        return 0
    

def get_dist(x1, y1, x2, y2):
    return sqrt((x1-x2)**2 + (y1-y2)**2)
    
    
def draw_system(cm, um):
    color = ['b', 'g', 'r', 'c', 'k', 'y', 'm' ,'w', '#8172B2', '#56B4E9', '#D0BBFF', '#D65F5F', '#017517', '#e5ae38', '#001C7F', '#6ACC65', '#8EBA42', '#EAEAF2', '#7600A1', '#E8000B']
    for c in cm:
        idx_c = cm.index(c)
        color_no = idx_c % len(color)
        plt.text(c.pos_x, c.pos_y, str(idx_c))
        plt.plot(c.pos_x, c.pos_y, color = color[color_no], marker='^')
        for sec in c.client:
            for u in sec:
                plt.plot(u.pos_x, u.pos_y, color = color[color_no], marker='o')                
        
    plt.axis([0, pr.map_size[0], 0, pr.map_size[1]])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('System Overview')
    plt.savefig('overview.jpg')
    plt.show()
    
    
def get_cover_nb(um):
    covered = 0.
    for u in um:
        if u.master != None:
            covered += 1.
    return covered   
    
    
def print_cover_rate(um):
    covered = get_cover_nb(um)
    print ('[Cover rate] :%.3f%%  (%d/%d)' % (covered/pr.user_no*100, covered, pr.user_no))


def print_cm_power(cm):
    print('[Cell power] :' , [e.power for e in cm])
        
def print_cm_client(cm):
    print('[Cell client]:')
    for c in cm:
        print(' ', c.get_client_no(), '/', pr.max_client_no, [len(e) for e in c.client])

        
def print_power_reduce(cm):
    nb_sector = pr.cell_no * pr.sector_no
    opened = sum([int(len(sec) > 0) for c in cm for sec in c.client ])
    print ('[Power saving] : from %d sectors opened to %d sectors' % (nb_sector, opened))
    #print ('[Power saving] :%f  (%d/%d)' % (opened/nb_sector*100, opened, nb_sector))
    
def print_interfere_reduce(cm, um):
    covered = 0.;
    intersect = 0.
    
    tmp_p = [c.power for c in cm]
    for c in cm:
        c.power = pr.Pmax
    for u in um:
        counter = 0.
        for c in cm:
            snr = get_snr(c, u, cm, pr.isInterfere, False)
            dist = get_dist(c.pos_x, c.pos_y, u.pos_x, u.pos_y)
            if snr >= pr.snr_threshold and dist <= c.radius:  
                counter += 1            # if counter >= 2, means this user is in the intersection of two cell's coverage
        if counter >= 2:
            intersect += 1        
            if u.master != None:
                covered += 1
    for c in cm:
        c.power = tmp_p[cm.index(c)]
    rate = covered/intersect if intersect != 0 else 0
    print ('[Interference reduction] :%.3f%%  (%d/%d)' % (rate * 100, covered, intersect))
    

def scenario1():
    cm = [sc.Cell(500, 500), sc.Cell(480, 500), sc.Cell(450, 500)]
    um = [ur.User(i*5, 500) for i in range(80, 101)]
    
    cell = cm[0]
    """
    for e in um:
        print (get_snr(cell, e, cm))      
          
    """      
    import Simulate as si
    um[0].master = cell
    cell.client[0].append(um[0])
    print (si.objective_func(cell, cm, um))
    for i in range(-31, 20):
        cell.power = i
        print (si.objective_func(cell, cm, um))         
        
        
if __name__ is '__main__':  
    cm = [sc.Cell(50, 50), sc.Cell(0, 20), sc.Cell(10, 10)]
    um = [ur.User(0, 50), ur.User(50, 0), ur.User(100, 50)]    
    cell = cm[0]
    for i  in range(3):
        um[i].master = cell
        cell.client[0].append(um[i])
    print (get_snr(cell, um[0], cm, False, True)) 
    print (get_snr(cell, um[1], cm, False, True))        
    print (get_snr(cell, um[2], cm, False, True))               
        
    
    
    
    
    
    
    
    
    
    
    
    