import time,sys,json

from SharedData.Logger import Logger
from SharedData.SharedData import SharedData
shdata = SharedData('SharedData/Routines/Server',user='master')
from SharedData.RealTime import RealTime

if len(sys.argv)>=2:
    _argv = sys.argv[1:]
else:
    Logger.log.error('command not provided!')
    raise Exception('command not provided!')

args = _argv[0].split(',')
host = args[0]
port = int(args[1])
RealTime.runserver(shdata,host,port)

while True:
    n=0
    sendheartbeat=True
    for client in RealTime.clients:
        c = RealTime.clients[client]
        table = c['table'].table
        n=n+1
        Logger.log.debug('Client %i: %s, %s,%s,%s,%s' % \
            (n,client.getpeername(),table.database,table.period,table.source,table.tablename) )
        sendheartbeat=False
    if sendheartbeat:
        Logger.log.debug('#heartbeat#,host:%s,port:%i' % (host,port))
    time.sleep(15)