import numpy as np
import Parameter as pr
import random as rd
import SmallCell as sc
import User as ur
import Utility as ut
from math import sqrt, pi, degrees, atan2, log, pow, inf



    
def init_cell():
    mylist = []
    fix_pos = ut.load_pos_cell()
    for i in range(pr.cell_no):
        pos_x = rd.uniform(0, pr.map_size[0])
        pos_y = rd.uniform(0, pr.map_size[1])
        if pr.fix_cell_pos:
            mylist.append( sc.Cell(fix_pos[i][0], fix_pos[i][1]) )
        else: 
            mylist.append( sc.Cell(pos_x, pos_y) )
    return mylist
    
    
def init_user():
    mylist = []
    fix_pos = ut.load_pos_user()
    for i in range(pr.user_no):
        pos_x = rd.uniform(0, pr.map_size[0])
        pos_y = rd.uniform(0, pr.map_size[1])
        if pr.fix_user_pos:
            mylist.append( ur.User(fix_pos[i][0], fix_pos[i][1]) )
        else: 
            mylist.append( ur.User(pos_x, pos_y) )
    return mylist   
    
    
def cco(cm, um):
    alg1(cm, um)
    alg2_v1(cm, um)
    
def alg1(cm, um):
    def find_max_user(cm, mark):
        mylist = []
        for i in range(len(cm)):
            for j in range(pr.sector_no):
                if mark[i][j] == 1:
                    mylist.append(-9999)
                else:
                    mylist.append(len(cm[i].client[j]))
        idx = mylist.index(max(mylist))
        (m, n) = (int(idx/pr.sector_no), idx%pr.sector_no)
        return (m, n)
        
    mark = [[0]*pr.sector_no  for _ in range(pr.cell_no)]    # indicate which cell's sector has already been allocated user completely.  If allocate=1,  unallocate=0
    for u in um:            # 一開始power全開，當cell的某個region有涵蓋到user，就把該user加入此region
        #print (ut.get_snr(cm[0], u, cm, pr.isInterfere, False))
        for c in cm:        # in this time, users can receive many cells' signal, but they haven't yet been allocated to any cell.
            snr = ut.get_snr(c, u, cm, pr.isInterfere, False)
            dist = ut.get_dist(c.pos_x, c.pos_y, u.pos_x, u.pos_y)
            clien_no = c.get_client_no()
            if snr >= pr.snr_threshold and dist <= c.radius and clien_no < c.max_client_no:  
                reg_no = ut.get_region_no(c, u)
                c.add_client(reg_no, u)    
   
    for _ in range( pr.cell_no * pr.sector_no):     # from now on, system begin to use greedy method to allocate user to some cell. If there is a cell's sector have most client under its coverage, then these client will be assign to this cell first.
        (m, n) = find_max_user(cm, mark)        # means cell-m's sector-n covers most users
        for u in cm[m].client[n]:               
            u.master = cm[m]
            for c in cm:
                for sec in c.client:
                    i = cm.index(c)
                    j = c.client.index(sec)
                    if m == i and n == j:
                        continue
                    if u in sec:
                        sec.remove(u)
        mark[m][n] = 1  
        

        

def alg2_v2(cm, um):    
    for c in cm:
        if c.get_client_no() == 0:
            c.power = pr.Pmin
            continue
        optimal_p = pr.Pmin
        max_f = -inf
        for p in range(int(pr.Pmax), int(pr.Pmin-1), -1):
            c.power = p
            snr_later = [ut.get_snr(c, u, cm, pr.isInterfere, True) for sec in c.client for u in sec]
            if min(snr_later) < pr.snr_threshold:
                optimal_p = p + 1 if p != pr.Pmax else p
                f = objective_func(c, cm, um)
                break
        c.power = optimal_p
            
    
        
def alg2_v1(cm, um):
    for c in cm:                            # keep decreasing every cells' power until its clients' SNR just reach threshold 
        if c.get_client_no() == 0:
            c.power = pr.Pmin
            continue
        while not c.is_power_min():
            c.power_down(1)
            snr_later = [ut.get_snr(c, u, cm, pr.isInterfere, True) for sec in c.client for u in sec]
            if min(snr_later) < pr.snr_threshold:
                c.power_up(1)
                break    
                
    
def objective_func(cell, cm, um):
    nb_client = cell.get_client_no()
    if nb_client == 0:
        return 0
    delta = pr.delta
    Bk = pr.bandwidth / nb_client 
    normalize_factor = pr.capacity4G
    cover_rate = ut.get_cover_nb(um) / pr.user_no    # covered rate value from 0 to 1
        
    f = (delta * cover_rate) + ((1-delta) * sum([Bk * log(1+ut.get_snr(cell, user, cm, pr.isInterfere, True), 2) for sec in cell.client for user in sec])) / normalize_factor
    return f
                

def capacity_func(cm, um):
    capacity = 0.
    for c in cm:
        nb_client = c.get_client_no()
        if nb_client == 0:
            continue
        Bk = pr.bandwidth / nb_client 
        capacity += sum([Bk * log(1 + ut.get_snr(c, u, cm, pr.isInterfere, True), 2) for sec in c.client for u in sec])
    return capacity / pr.cell_no
    
    
def begin():
    cm = init_cell()                # cell manager : gether all the cell's reference in one list
    um = init_user()                # user mamanger : gather all the user's reference in one list
    
    cco(cm, um)
    ut.draw_system(cm, um)    
    ut.print_cover_rate(um)
    ut.print_cm_power(cm)
    ut.print_cm_client(cm)
    ut.print_power_reduce(cm)
    ut.print_interfere_reduce(cm, um)
    print ('[Capacity]:', capacity_func(cm, um))
    
    
if __name__ == '__main__':          # main function
    begin()
        