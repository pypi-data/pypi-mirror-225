import numpy as np
import time
from multiprocessing import shared_memory

import SharedData.TableIndexJit as TableIndexJit
from SharedData.TableIndexJit import *


class TableIndex:

    # TODO: create a symbol backward linked list index
    # TODO: change portfolio index to backward linked list index
    
    def __init__(self,table):
        self.table = table
        self.shareddata = self.table.shareddata
        
        self.initialized = False

        # primary key hash table        
        self.pkeycolumns = TableIndex.get_pkeycolumns(self.table.database)
        self.pkeystr = '_'.join(self.pkeycolumns)
        self.pkey = np.ndarray([])
        # date index
        self.dateiniidx = np.ndarray([])
        self.dateendidx = np.ndarray([])
        # date,portfolio index
        self.portiniidx = np.ndarray([]) # hash table
        self.portlist = np.ndarray([]) # linked list
        self.portlistcount = 0

    def initialize(self):
        
        self.get_functions()
        
        self.malloc()

        self.initialized = True

    def get_functions(self):
        # primary key & index functions
        self.create_index_func = None
        self.upsert_func = None
        self.get_loc_func = None
        

        create_pkey_fname = 'create_pkey_'+ self.pkeystr + '_jit'
        if hasattr(TableIndexJit,create_pkey_fname):
            self.create_index_func = getattr(TableIndexJit,create_pkey_fname)
        else:
            raise Exception('create_pkey function not found for database %s!' \
                % (self.table.database))

        upsert_fname = 'upsert_'+ self.pkeystr + '_jit'
        if hasattr(TableIndexJit,upsert_fname):
            self.upsert_func = getattr(TableIndexJit,upsert_fname)
        else:
            raise Exception('upsert function not found for database %s!' \
                % (self.table.database))

        get_loc_fname = 'get_loc_'+ self.pkeystr + '_jit'
        if hasattr(TableIndexJit,get_loc_fname):
            self.get_loc_func = getattr(TableIndexJit,get_loc_fname)
        else:
            raise Exception('get_loc function not found for database %s!' \
                % (self.table.database))
        
        if 'date_portfolio_' in self.pkeystr:
            self.get_index_date_portfolio_func = \
                getattr(TableIndexJit,'get_index_date_portfolio_jit')
    
    def malloc(self):
        shm_name = self.table.shm_name
        self.malloc_pkey(shm_name)
        if 'date' in self.pkeystr:
            self.malloc_dateidx(shm_name)
        if 'date_portfolio_' in self.pkeystr:
            self.malloc_portfolioidx(shm_name)
        if np.all(self.pkey==-1):
            self.create_index()

    def malloc_pkey(self,shm_name):        
        keysize = int(self.table.records.size*5)
        keysize_bytes = int(keysize * 4)

        iscreate = False
        [self.pkeyshm, ismalloc] = self.shareddata.malloc(shm_name+'#pkey')
        if not ismalloc:
            [self.pkeyshm, ismalloc] = self.shareddata.malloc(shm_name+'#pkey',\
                create=True,size=keysize_bytes)
            iscreate = True

        self.pkey = np.ndarray((keysize,),dtype=np.int32,buffer=self.pkeyshm.buf)
        if iscreate:
            self.pkey[:] = -1
                        
    def malloc_dateidx(self,shm_name):
        #date index
        dtunit = str(self.table.records.dtype[0]).split('[')[-1].split(']')[0]
        if dtunit=='ns':
            self.dateunit = 24*60*60*1000*1000*1000
        else:
            raise Exception('Only dates with ns precision are supported!')
        maxdate = np.datetime64('2070-01-01','D')
        dateidxsize = maxdate.astype(int)
        dateidxsize_bytes = int(dateidxsize * 4)
        
        iscreate = False        
        [self.dateidxshm, ismalloc] = self.shareddata.malloc(shm_name+'#dateidx')
        if not ismalloc:
            [self.dateidxshm, ismalloc] = self.shareddata.malloc(shm_name+'#dateidx',\
                create=True,size=int(dateidxsize_bytes*2))
            iscreate = True
            
        self.dateiniidx = np.ndarray((dateidxsize,),dtype=np.int32,buffer=self.dateidxshm.buf)        
        self.dateendidx = np.ndarray((dateidxsize,),dtype=np.int32,buffer=self.dateidxshm.buf,\
            offset=dateidxsize_bytes)
        
        if iscreate:
            self.dateiniidx[:]=-1        
            self.dateendidx[:]=-1
            
    def malloc_portfolioidx(self,shm_name):
        portlistsize = int(self.table.records.size*2)
        keysize = int(self.table.records.size*5)
        keysize_bytes = int(keysize * 4)
        portidxsize_bytes = 4 +  int(keysize_bytes*2) + int(portlistsize*4)
        
        iscreate = False
        [self.portidxshm, ismalloc] = self.shareddata.malloc(shm_name+'#portidx')
        if not ismalloc:        
            [self.portidxshm, ismalloc] = self.shareddata.malloc(shm_name+'#portidx',create=True,size=portidxsize_bytes)
            iscreate = True
            
        self.portlistcount = np.ndarray((1,),dtype=np.int32,buffer=self.portidxshm.buf)[0]
        self.portiniidx = np.ndarray((keysize,),dtype=np.int32,\
            buffer=self.portidxshm.buf,offset=4)
        self.portendidx = np.ndarray((keysize,),dtype=np.int32,\
            buffer=self.portidxshm.buf,offset=int(4+keysize_bytes))
        self.portlist = np.ndarray((portlistsize,),dtype=np.int32,\
            buffer=self.portidxshm.buf,offset=int(4+keysize_bytes*2))

        if iscreate:
            self.portlistcount=0
            self.portiniidx[:]=-1
            self.portendidx[:]=-1
            self.portlist[:]=-1
                
    def create_index(self):
        ti = time.time()
        if self.table.records.count>0:
            print('Creating index %s/%s/%s/%s %i lines...' % \
                (self.table.database,self.table.period,self.table.source,\
                self.table.tablename,self.table.records.count))
            time.sleep(0.001)
            arr = self.table.records
            if 'date_portfolio_' in self.pkeystr:
                self.create_index_func(arr,self.table.records.count,\
                    self.pkey,self.dateiniidx,self.dateendidx,self.dateunit,\
                    self.portiniidx,self.portendidx,self.portlist,self.portlistcount,0)
                self.portlistcount=self.table.records.count
            else:
                self.create_index_func(arr,self.table.records.count,self.pkey,\
                    self.dateiniidx,self.dateendidx,self.dateunit,0)
            print('Creating index %s/%s/%s/%s %i lines/s DONE!' % \
                (self.table.database,self.table.period,self.table.source,\
                self.table.tablename,self.table.records.count/(time.time()-ti)))

    def update_index(self,start):
        self.pkey[:] = -1
        self.dateiniidx[:]=-1        
        self.dateendidx[:]=-1
        arr = self.table.records[0:self.table.records.size]        
        if 'date_portfolio_' in self.pkeystr:            
            self.portlistcount=0
            self.portiniidx[:]=-1
            self.portendidx[:]=-1
            self.portlist[:]=-1
            self.create_index_func(arr,self.table.records.count,\
                    self.pkey,self.dateiniidx,self.dateendidx,self.dateunit,\
                    self.portiniidx,self.portendidx,self.portlist,self.portlistcount,0)
            self.portlistcount=self.table.records.count
        else:            
            self.create_index_func(arr,self.table.records.count,self.pkey,\
                self.dateiniidx,self.dateendidx,self.dateunit,0)    
        
    @staticmethod
    def get_pkeycolumns(database):
        if database == 'MarketData':
            return ['date','symbol']
        
        elif database == 'Relationships':
            return ['date','symbol1','symbol2']
        
        elif database == 'Portfolios':
            return ['date','portfolio']
                                
        elif database == 'Signals':
            return ['date','portfolio','symbol']

        elif database == 'Risk':
            return ['date','portfolio','symbol']
                
        elif database == 'Positions':
            return ['date','portfolio','symbol']
        
        elif database == 'Orders':
            return ['date','portfolio','symbol','clordid']
                
        elif database == 'Trades':
            return ['date','portfolio','symbol','tradeid']
                
        else:
            raise Exception('Database not implemented!')
        