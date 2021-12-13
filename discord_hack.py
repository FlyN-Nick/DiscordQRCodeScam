#from multiprocessing import Pool      
from threading import Thread
                                          
import discord_hack_automation
import discord_hack_server

#pool = Pool(processes=2)

#pool.apply_async(discord_hack_automation.main)
#pool.apply_async(discord_hack_server.main)

if __name__ == "__main__":
    t1 = Thread(target = discord_hack_automation.main)
    t2 = Thread(target = discord_hack_server.main)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    while True:
        pass