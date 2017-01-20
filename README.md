
snr數值不穩 一部分是因為gaussian noise 且要除interfere才有辦法消掉watt單位 

ALG1 一開始算SNR 過threashold 不要考慮interfere
path loss太大



 ----DONE-----
 ALG-V2  objective一定只會帶入 Pthreshold
 capacity 要加gain?   要除cell_nb? 
objective 必然最大  沒有把powerUp的反效果加進去   
init全開snr要加gain?   不要加  (ALG1慢慢加user後  pattern會開始變  所以算snr就不是全關的狀態)
 object-coverUk是指被cell而已?   
 gaussian db??     
 objective-Bk?   
 objective-SNR (負值db/ratio)?   
 object-normal.   
 ITRI_bean_pattern?   