import time
import numpy as np


from SharedData.SharedData import SharedData
shdata = SharedData('SharedData/Routines/ReadLogs',user='worker')
from SharedData.Logger import Logger
from SharedData.AWSKinesis import KinesisLogStreamConsumer

SLEEP_TIME = 2

def run():
    consumer = KinesisLogStreamConsumer(user='worker')
    lastheartbeat = time.time()
    try:
        consumer.readLogs()
        if consumer.connect():
            Logger.log.info('Logger reader process STARTED!')
    except:
        pass

    while True:
        success = False
        try:
            success = consumer.consume()            
            if (success) & (time.time()-lastheartbeat>=15):
                lastheartbeat = time.time()
                Logger.log.debug('#heartbeat#')                
        except:
            pass

        if not success:
            Logger.log.info('Logger reader process error! Restarting...')
            try:
                consumer.readLogs()
                success = consumer.connect()
            except:
                pass
            if success:
                Logger.log.info('Logger reader process RESTARTED!')
            else:
                Logger.log.info('Logger reader failed RESTARTING!')
                time.sleep(SLEEP_TIME*5)
        else:
            time.sleep(SLEEP_TIME + SLEEP_TIME*np.random.rand() - SLEEP_TIME/2)

if __name__ == "__main__":
    run()