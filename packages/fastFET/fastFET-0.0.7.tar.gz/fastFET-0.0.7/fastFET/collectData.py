import math
import os, sys, csv, re
import datetime as dt
from datetime import datetime
from copy import deepcopy
import glob
import time
import requests

import multiprocessing, subprocess

#sys.path.append( os.path.dirname(os.path.dirname(__file__)))
from fastFET.BGPMAGNET.dataGetter import downloadByParams
from fastFET.BGPMAGNET.base import base_params, bgpGetter
from fastFET.BGPMAGNET.params import BGP_DATATYPE
from fastFET.utils import logger
from fastFET import utils, bgpToolKit


processList= []


class GetRawData(object):
    
    def __init__(self, 
        event_list_path=os.path.dirname(__file__)+ '/event_list.csv',
        parent_folder= "Dataset/",
        increment= 4,  
        duration= 2,
        updates= True,
        ribs= False    ):
        '''
        - description: `event_list.csv` -> download `.gz`files -> `bgpdump` to `.txt` -> `.txt`files
        - args-> event_list_path {*}: 事件列表路径
        - args-> parent_folder {*}: 下载和解析数据存放路径
        - args-> increment {*}: 定义事件起止时间的增量(h)
        - args-> duration {*}: 当事件缺省结束时间时，将其指定为 start_time + duration (h)
        - args-> updates {*}: 是否需要收集updates数据。
        - args-> ribs {*}: 是否需要收集ribs数据
        - return {*}
        '''        
        self.path= event_list_path
        self.collection_data_lib= parent_folder+ 'raw_cmpres/'
        self.collection_data_lib_parsed= parent_folder+ "raw_parsed/"

        self.increment= increment
        self.duration= duration
        self.ribTag= ribs
        self.updTag= updates

        logger.info('')
        s= '# download & decode to ASCII #'
        logger.info('#'* len(s))
        logger.info(s)
        logger.info('#'* len(s))
  
    def getEventsDict(self):
        '''
        - description: read events from `self.path`.  
        - 主要目的：把用户自定义事件起止时间规范化为符合raw文件名的、并考虑到了increment和rib表更新等参数的  起止时间
            - 若FET类不采图特征，则只收集updates文件：`新起止时间= (原起止± increment)*标准化`
            - 若FET类要采图特征，则还需收集ribs文件： 在上式基础上，添加一个datetime_atRIB。图特征的采集需要从datetime_atRIB到datetime_end的全部updates消息。``
        - return {'eventName':{'collector': [datetime_start, datetime_end, datetime_atRIB]}} arg3可能为None。'''
        # read 'events_list.csv'
        with open(self.path) as f:
            event_list= []
            csv_file= csv.reader(f)
            for line in csv_file:
                event_list.append(list(line))
        # get time slot of each event which to be collected. 
        res= utils.d_d_list()
        for event in event_list:
            if len(event):
                start= dt.datetime.strptime(event[1].strip(), "%Y/%m/%d %H:%M:%S")- dt.timedelta(hours= self.increment )
                if event[2].strip():
                    end = dt.datetime.strptime(event[2].strip(), "%Y/%m/%d %H:%M:%S")+ dt.timedelta(hours= self.increment )
                else:
                    end = dt.datetime.strptime(event[1].strip(), "%Y/%m/%d %H:%M:%S")+ dt.timedelta(hours= self.increment+ self.duration)

                for monitor in event[3:]:
                    monitor= monitor.strip()
                    interval_upd= utils.intervalMin('updates', monitor)
                    satTime, endTime= utils.normSatEndTime(interval_upd, start, end)
                    satTime_atRIB= None
                    if self.ribTag:
                        interval_rib= utils.intervalMin('ribs', monitor)
                        satTime_atRIB, _= utils.normSatEndTime(interval_rib, satTime, endTime)
                    res[event[0]][monitor]= [satTime, endTime, satTime_atRIB]

        return res

    def isDwlad(self, type, monitor, satTime: datetime, endTime: datetime):
        ''''''
        try:
            ppath, _, files = os.walk(self.collection_data_lib+ monitor).__next__()
            assert len(files) != 0
            try:
                files= sorted( [ f for f in files if type in f])
                files_cuted= utils.cut_files_list(files, satTime, endTime)
                res= [ppath+ os.sep+ file for file in files_cuted]
                return res
            except:
                return []
        except:
            return []

    def download(self, type:str, monitor:str, satTime: datetime, endTime: datetime, only_rib= None):
        '''- download files in whole day, then cut files to sat and end. 
        - arg(type): only in 'updates', 'ribs', 'all'
        - arg(satTime, endTime): datetime type or str (e.g. `'2023-02-06-00:00'`)
        - return: cuted  raw_files, or maybe empty list'''

        str_map= {'updates': 'updates', 'rib.': 'ribs', 'bview.': 'ribs'}
        if not isinstance(satTime, str):
            sat= satTime.strftime('%Y-%m-%d')+ "-00:00"
            end= endTime.strftime('%Y-%m-%d')+ "-23:59"
        else:
            sat= satTime
            end= endTime
        if type!= 'updates' and only_rib== False:
            target_time= satTime.strftime('%Y%m%d.%H%M')
            a_rib_url= bgpToolKit.MRTfileHandler.get_download_url(type, monitor, target_time)
            a_rib_filename= a_rib_url.split('/')[-1]
            
            response = requests.head(a_rib_url).status_code
            if response==200:
                target_path= f'{self.collection_data_lib}{monitor}/'
                cmd= f"cd {target_path}; wget {a_rib_url}; mv {a_rib_filename} {monitor}_{a_rib_filename}"
                p= subprocess.Popen(cmd, shell=True)
                logger.info(f'    - {p.pid=}, downloading a `{monitor}` rib table...')
                processList.append(p)
                return [ f"{target_path}{monitor}_{a_rib_filename}"]
            else:
                logger.warning(f'    - in {monitor}, url WRONG:`{a_rib_url}`')
                return []

        bgpdbp=downloadByParams( 
            urlgetter=bgpGetter(base_params(
                start_time= sat,
                end_time  = end,
                bgpcollectors=[monitor],
                data_type=BGP_DATATYPE[str_map[type].upper()]
            )),
            destination= self.collection_data_lib,
            save_by_collector=1
        )
        bgpdbp.start_on()
        # check_error_list(sys.path[0]+ "/errorInfo.txt")
        whole_files= glob.glob(self.collection_data_lib+ monitor+ os.sep+ monitor+ '_'+ type+ '*')
        
        try:
            dest_files= utils.cut_files_list(whole_files, satTime, endTime)
        except:
            return []
        return dest_files

    def trans_multiproc(self, tup):
            os.system('bgpdump -m '+ tup[1] + ' > '+ tup[0] +  os.path.basename(tup[1])+ '.txt')

    def raw2txt(self, dest_dir, raw_files, type, monitor= None):       
        '''- description: transform BGP update raw data to .txt by command `bgpdump`
        - return `.txt list`
        '''
        if len(raw_files)==1:
            target_path= f"{dest_dir}{os.path.basename(raw_files[0])}.txt"
            cmd= f"bgpdump -m {raw_files[0]} > {target_path}"
            p= subprocess.Popen(cmd, shell=True)
            logger.info(f"    - {p.pid=}, parsing a rib of `{monitor if monitor!=None else ' '}`...")
            processList.append(p)
            return [target_path]

        dest_dirs= [ dest_dir ]* len(raw_files)
        
        pool= multiprocessing.Pool(multiprocessing.cpu_count()//2)
        pool.map(self.trans_multiproc, zip(dest_dirs, raw_files))
        pool.close()
        pool.join()

        parsed_files= sorted(glob.glob(f'{dest_dir}/*{type}*'))
        return parsed_files

    def oneMonitor(self, type, txt_dir, monitor, fact_satTime: datetime, endTime: datetime):
        '''
        - description: 单个monitor的多文件的下载和解析
        - args-> type {*}: `'updates'`or`'rib.'`or`'bview.'`
        '''
        curDir= utils.makePath( txt_dir+ monitor+ '/' )        
        os.system(f'rm {curDir}*_{type}*')
        raw_files= self.isDwlad(type, monitor, fact_satTime, endTime)
        if not len(raw_files): 
            st1= time.time()
            raw_files= self.download(type, monitor, fact_satTime, endTime, only_rib= not self.updTag )
            logger.info(' '*4+ '- %s dwladed: %.3f sec, %d files.' %( monitor, time.time()- st1, len(raw_files)))

        if not len(raw_files):
            logger.warning(' '*4+ '- %s has missed files on website.' % monitor)
            return []

        st2= time.time()
        txtfiles= self.raw2txt( curDir, raw_files, type, monitor )
        #logger.info(' '*4+ '- %s parsed: %.3f sec, %d files.' %( monitor, time.time()- st2, len(raw_files)))

        return txtfiles

    def getUpdTxts(self, events_dict):
        '''解析updates文件
        - return:  `{'evtNm': {'monitor': ( [ .txt, ...]|None, str|None ) } } `'''
        res= deepcopy( events_dict )
        ppath, dirs, _= os.walk( self.collection_data_lib_parsed ).__next__()
        for evtNm, moniDict in events_dict.items():
            logger.info(' '*2+ '- %s:' % evtNm )
            if evtNm in dirs:
                p2, moni_dirs, _ = os.walk( ppath+ evtNm+ os.sep ).__next__()
                for monitor,[ satTime_tradiFeat, endTime, satTime_graphFeat ] in moniDict.items():
                    
                    txtfiles= sorted(glob.glob(p2+ monitor+ os.sep+ monitor+ '_updates*'))
                    if not satTime_graphFeat :
                        fact_satTime= satTime_tradiFeat
                        watershed_= None
                    else:
                        fact_satTime= satTime_graphFeat
                        watershed_= satTime_tradiFeat.strftime('%Y%m%d.%H%M')

                    interval= utils.intervalMin('updates', monitor[:3])
                    allin= utils.allIn(interval, txtfiles, fact_satTime, endTime)

                    if monitor in moni_dirs and allin :
                        target_files= utils.cut_files_list(txtfiles, fact_satTime, endTime)
                        res[evtNm][monitor]= ( target_files, watershed_ )
                        logger.info(' '*4+ '- %s: upds has existed, don\'t need to parse.' % monitor)
                    else:
                        res[evtNm][monitor]= ( self.oneMonitor('updates', p2, monitor, fact_satTime, endTime), watershed_ )
                        
            else:
                for monitor,[ satTime_tradiFeat, endTime, satTime_graphFeat ] in moniDict.items():
                    if not satTime_graphFeat :
                        fact_satTime= satTime_tradiFeat
                        watershed_= None
                    else:
                        fact_satTime= satTime_graphFeat
                        watershed_= satTime_tradiFeat.strftime('%Y%m%d.%H%M')

                    res[evtNm][monitor]= ( self.oneMonitor('updates', ppath+ evtNm+ '/', monitor, fact_satTime, endTime), watershed_ )
        return res

    def getRibTxts(self, events_dict):
        '''
        - description: 解析rib文件
        - return {*}: `{'evtNm': {'monitor': [.txt]|[] } } `
        '''
        list_parsing=[]
        list_downloading=[]

        strmap= {'rrc': 'bview.', 'rou': 'rib.'}
        res= deepcopy( events_dict )
        ppath, dirs, _= os.walk( self.collection_data_lib_parsed ).__next__()
        for evtNm, moniDict in events_dict.items():
            logger.info(' '*2+ '- %s:' % evtNm )

            for monitor,[ _, endRIBtime, satRIBtime ] in moniDict.items():
                txtFolder= ppath+ evtNm+ '/' + monitor+ '/'     
                utils.makePath(txtFolder)
                
                txtfiles= sorted(glob.glob( txtFolder+ monitor+ '_'+ strmap[monitor[:3]]+ '*' ))
                interval= utils.intervalMin('ribs', monitor[:3])
                if self.updTag:
                    if len(txtfiles) != 1:
                        target_time= satRIBtime.strftime('%Y%m%d.%H%M')
                        a_rib_url= bgpToolKit.MRTfileHandler.get_download_url(type, monitor, target_time)
                        basename = a_rib_url.split('/')[-1]
                        download_file= f"{self.collection_data_lib}{monitor}/{monitor}_{basename}"
                        pathTXT= f"{self.collection_data_lib_parsed}{evtNm}/{monitor}/{monitor}_{basename}.txt"
                        
                        if not os.path.exists(download_file):
                            response = requests.head(a_rib_url).status_code
                            if response==404:
                                logger.warning(f'    - in {monitor}, url WRONG:`{a_rib_url}`')
                                res[evtNm][monitor]= []
                            else:
                                list_downloading.append({'url': a_rib_url, 'path': download_file})
                                list_parsing.append({'pathMRT': download_file, 'pathTXT': pathTXT})
                                res[evtNm][monitor]= [pathTXT]
                        else:
                            list_parsing.append({'pathMRT': download_file, 'pathTXT': pathTXT})
                            res[evtNm][monitor]= [pathTXT]
                    else:   
                        logger.info(' '*4+ '- %s: ribs has existed, don\'t need to parse.' % monitor)    
                        res[evtNm][monitor]= txtfiles 

                else:
                    allin= utils.allIn(interval, txtfiles, satRIBtime, endRIBtime)
                    if allin:
                        logger.info(' '*4+ '- %s: ribs has existed, don\'t need to parse.' % monitor) 
                    else:
                        txtfiles= self.oneMonitor(strmap[monitor[:3]], ppath+ evtNm+ '/', monitor, satRIBtime, endRIBtime)
                    res[evtNm][monitor]= txtfiles 
                    
        if list_downloading:
            plist=[]
            for dic in list_downloading:
                cmd= f"wget -q -O {dic['path']} {dic['url']}"
                p= subprocess.Popen(cmd, shell=True)
                logger.info(f'    - {p.pid=}, downloading: `{cmd}`...')
                plist.append(p)
            for p in plist:
                p.wait()
                
        if list_parsing:
            p2list=[]
            for dic in list_parsing:
                cmd= f"bgpdump -m {dic['pathMRT']} > {dic['pathTXT']}"
                p= subprocess.Popen(cmd, shell=True)
                logger.info(f'    - {p.pid=}, parsing: `{cmd}`...')
                p2list.append(p)
            for p in p2list:
                p.wait()

        return res

    def getRawTxts(self, events_dict: dict):
        '''- including download and parse
        - return `{ 'updates': {'evtNm': {'monitor': ([ '.txt', ...], str|None) } } |{}, 
                    'ribs'    : {'evtNm': {'monitor': [ '.txt', ...]|[]         } } |{}
                  }`
        '''
        if not os.path.exists( self.collection_data_lib_parsed ):
            utils.makePath( self.collection_data_lib_parsed )
        resUpd, resRib= {},{}
        
        if self.updTag:
            logger.info('Start: parse `updates` data:')
            resUpd= self.getUpdTxts(events_dict)
            logger.info('End: `updates` data.')
        else:
            logger.info('ONLY analysis ribs with graph-features, no need to get any updates files.')
        if self.ribTag:
            t1= time.time()
            logger.info('Start: parse `ribs` data:')
            resRib= self.getRibTxts(events_dict)
            logger.info(f'End({(time.time()-t1):.1f}sec): `ribs` data.')
        return {'updates': resUpd, 'ribs': resRib} 
    

    def run(self):
        '''
        - description: main func
        - return {*}: 
            `{ 'updates': {'evtNm': {'monitor': ( [ .txt, ...]|None, str|None ) } },
                'ribs'  : {'evtNm': {'monitor': [.txt]|None                       } } | {}   } `
        '''
        evtDic= self.getEventsDict()
        txtDic= self.getRawTxts(evtDic)

        # ending all of subprocess
        for p in processList:
            p.wait()
        return txtDic
        
        
if __name__=='__main__':
    
    obj= GetRawData(increment=0, collection_data_lib='Dataset/')