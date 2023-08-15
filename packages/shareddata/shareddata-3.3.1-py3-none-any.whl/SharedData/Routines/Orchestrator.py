# PROPRIETARY LIBS
import os,sys,time
from datetime import datetime

from SharedData.SharedData import SharedData
shdata = SharedData('SharedData/Routines/Orchestrator',user='master')
from SharedData.Logger import Logger
from SharedData.Routines.Scheduler import RoutineScheduler
from SharedData.AWSKinesis import KinesisStreamProducer

# TODO: add routine type realtime

if len(sys.argv)>=2:
    SCHEDULE_NAME = str(sys.argv[1])
else:
    Logger.log.error('SCHEDULE_NAME not provided, please specify!')
    raise Exception('SCHEDULE_NAME not provided, please specify!')

Logger.log.info('SharedData Routines orchestrator starting for %s...' % (SCHEDULE_NAME))

stream_name=os.environ['WORKERPOOL_STREAM']
producer = KinesisStreamProducer(stream_name)

sched = RoutineScheduler(stream_name)
sched.LoadSchedule(SCHEDULE_NAME)
sched.UpdateRoutinesStatus()

lastheartbeat = time.time()
while(True):
    if (time.time()-lastheartbeat>=15):
        lastheartbeat = time.time()
        Logger.log.debug('#heartbeat#,schedule:%s' % (SCHEDULE_NAME))

    if sched.schedule['Run Times'][0].date()<datetime.now().date():
        print('')
        print('Reloading Schedule %s' % (str(datetime.now())))
        print('')
        sched.LoadSchedule(SCHEDULE_NAME)
        sched.UpdateRoutinesStatus()

    sched.UpdateRoutinesStatus()
    sched.RunPendingRoutines()    
    time.sleep(5)