# implements a decentralized routines worker 
# connects to worker pool
# broadcast heartbeat
# listen to commands
# environment variables:
# SOURCE_FOLDER
# WORKERPOOL_STREAM
# GIT_SERVER
# GIT_USER
# GIT_ACRONYM
# GIT_TOKEN

import os,time,sys
from importlib.metadata import version
import numpy as np
from threading import Thread

from SharedData.SharedData import SharedData
shdata = SharedData('SharedData/Routines/Worker',user='worker')
from SharedData.Logger import Logger
from SharedData.AWSKinesis import *
from SharedData.Routines.WorkerLib import *


routines = []
consumer = KinesisStreamConsumer(os.environ['WORKERPOOL_STREAM'])
producer = KinesisStreamProducer(os.environ['WORKERPOOL_STREAM'])
SLEEP_TIME = int(os.environ['SLEEP_TIME'])

Logger.log.info('SharedData Worker version %s STARTED!' % (version('shareddata')))
lastheartbeat = time.time()
while True:
    try:
        sendheartbeat=True    
        for routine in routines:
            if ('process' in routine):
                if (not routine['process'] is None):
                    if routine['process'].poll() is not None:
                        routines.remove(routine)
            elif (not routine['thread'].is_alive()):
                routines.remove(routine)

        if not consumer.consume():
            consumer.get_stream()
            Logger.log.error('Cannot consume workerpool messages!')
            time.sleep(5)

        for record in consumer.stream_buffer:
            print('Received:'+str(record))
            
            command = record
            if ('job' in command) & ('target' in command):
                if ((command['target'].lower()==os.environ['USER_COMPUTER'].lower())\
                     | (command['target']=='ALL')):
                    sendheartbeat = False
                    if command['job'] == 'command':
                        send_command(command['command'])

                    elif command['job'] == 'routine': 
                        start_time = time.time()
                        routine = {
                            'command':command,
                            'thread':None,
                            'process':None,
                            'start_time':start_time,
                        }                     
                        thread = Thread(target=run_routine,args=(command,routine))
                        routine['thread'] = thread
                        routines.append(routine)
                        thread.start()
                        
                    elif command['job'] == 'install':
                        start_time = time.time()
                        routine = {
                            'command':command,
                            'thread':None,
                            'start_time':start_time,
                        }                     
                        thread = Thread(target=install_repo,args=(command,routine))
                        routine['thread'] = thread
                        routines.append(routine)
                        thread.start()

                    elif command['job'] == 'logger':
                        isrunning = False
                        for routine in routines:
                            if (routine['command']['repo']=='logger'):
                                isrunning=True
                                break                                
                        if not isrunning:
                            routine = run_logger(command)
                            routines.append(routine)
                            
                        else:
                            Logger.log.info('Logger already running!')
                            
                    elif command['job'] == 'scheduler':
                        isrunning = False
                        for routine in routines:
                            if (routine['command']['repo']=='scheduler'):
                                if 'args' in routine['command']:
                                    if (routine['command']['args']==command['args']):
                                        isrunning=True
                                        break                                
                        if not isrunning:
                            routine = run_scheduler(command)
                            routines.append(routine)
                            
                        else:
                            Logger.log.info('Scheduler %s already running!' % (command['args']))

                    elif command['job'] == 'server':
                        isrunning = False
                        for routine in routines:
                            if (routine['command']['repo']=='server'):
                                if 'args' in routine['command']:
                                    if (routine['command']['args']==command['args']):
                                        isrunning=True
                                        break                                
                        if not isrunning:
                            routine = run_server(command)
                            routines.append(routine)
                            
                        else:
                            Logger.log.info('Server %s already running!' % (command['args']))

                    elif command['job'] == 'status': 

                        Logger.log.info('Status: %i process' % (len(routines)))
                        n=0
                        for routine in routines:                            
                            n+=1
                            statusstr = 'Status %i: running %s' % (n,routine['command']['repo'])
                            if 'routine' in routine['command']:
                                statusstr = '%s/%s' % (statusstr,routine['command']['routine'])
                            if 'args' in routine['command']:
                                statusstr = '%s/%s' % (statusstr,routine['command']['args'])
                            if 'start_time' in routine:
                                statusstr = '%s %.2fs' % (statusstr,time.time()-routine['start_time'])
                            Logger.log.info(statusstr)
                            
                    elif command['job'] == 'kill':
                        if command['repo']=='ALL':
                            Logger.log.info('Kill: ALL...')
                            for routine in routines:                            
                                try:
                                    routine['process'].kill()
                                except:
                                    pass
                            Logger.log.info('Kill: ALL DONE!')
                        else:
                            for routine in routines:
                                kill=False
                                if (routine['command']['repo']==command['repo']):
                                    if 'routine' in command:
                                        if (routine['command']['routine']==command['routine']):
                                            kill=True
                                    else:
                                        kill=True
                                
                                if (kill) & ('process' in routine):
                                    try:                                                                                
                                        routine['process'].kill()
                                        if 'routine' in command:
                                            Logger.log.info('Kill: %s/%s %.2fs DONE!' % \
                                                (routine['command']['repo'],routine['command']['routine'],\
                                                time.time()-routine['start_time']))
                                        else:
                                            Logger.log.info('Kill: %s %.2fs DONE!' % \
                                                (routine['command']['repo'],time.time()-routine['start_time']))
                                    except:
                                        pass

                    elif command['job'] == 'restart':                    
                        restart_program()

                    elif command['job'] == 'ping':
                        Logger.log.info('pong')

                    elif command['job'] == 'pong':
                        Logger.log.info('ping')

        if (sendheartbeat) & (time.time()-lastheartbeat>15):
            lastheartbeat = time.time()
            Logger.log.debug('#heartbeat#')

        consumer.stream_buffer = []
        time.sleep(SLEEP_TIME + SLEEP_TIME*np.random.rand() - SLEEP_TIME/2)

    except Exception as e:
        Logger.log.error('Worker ERROR\n%s' % (str(e)))
        consumer.stream_buffer = []
        time.sleep(SLEEP_TIME + SLEEP_TIME*np.random.rand() - SLEEP_TIME/2)
        
    