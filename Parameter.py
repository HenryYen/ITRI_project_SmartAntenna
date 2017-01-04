# for global system
user_no = 39
cell_no = 31                 # if cell_no == 1, Utility.get_snr() will have porblem 
map_size = [250, 200]        # Logical coordinate system : bottom left is (0, 0),  and top rigth is(1000, 1000)
alpha = 1.                  
gamma = 4.                  
bandwidth = 20.              
snr_threshold = 31.      #thredshold in db = 14.914 ; threadshold in ratio = 31   
gaussian_noise = 8.      # db
delta = 0.               # delta=1 means objective function only consider coverage factor; delta=0 means objective function only consider capacity factor
capacity4G = 100.        # standard 4G : 100Mbps
isInterfere = True       # decide whether serving cell is interfered by other cells
interfereReduction = 80.


# for cell
fix_cell_pos = True 
fix_user_pos = True  
Pmax = 19.       
Pmin = -31.      
sector_no = 5     
max_client_no = 32
radius = 32.
ref_dist = 1.
Pref = 30.                # PL(d1) = 30


#external data
path = './data'
fn_pos_bs = path + '/161130-BS.txt'
fn_pos_ue = path + '/161130-UE.txt'


if __name__ == '__main__':
    import Simulate as sm
    sm.begin()