from progressbar import progressbar
from time import sleep

for i in progressbar(range(0,10),"Loading ",40):
    sleep(1)
    
