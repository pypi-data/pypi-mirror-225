from tqdm import tqdm
import time

#Manually set p_bar
p_bar = tqdm(total=100)
p_bar.update(0-p_bar.n)
time.sleep(2)
p_bar.update(20-p_bar.n)
time.sleep(2)
p_bar.update(40-p_bar.n)
time.sleep(2)
p_bar.update(60-p_bar.n)
time.sleep(2)
p_bar.update(80-p_bar.n)
time.sleep(2)
p_bar.update(100-p_bar.n)
time.sleep(2)