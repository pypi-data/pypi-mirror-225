#! /usr/bin/env python
# -*-coding:utf-8-*-
'''
- Description: `https://stat.ripe.net/data/*`的接口集合，实现对prefix, peer, AS, IP等相关历史数据的查找
- version: 1.0
- Author: JamesRay
- Date: 2023-03-18 05:30:31
- LastEditTime: 2023-06-17 10:01:10
'''
import requests
import jsonpath, json
from typing import Union

class tools():
    '''- common tools for the script'''
    
    @staticmethod
    def fill_url(*args, **kwargs):
        '''
        - description: 生成url
        - args-> args {array}: array_0: str like `/data/*/data.json`
        - args-> kwargs {object}: 
        - return {*}
        '''
        domain= 'https://stat.ripe.net'
        url= domain+ args[0]
        if 'resource' in kwargs.keys():
            for k, v in kwargs.items():
                if k=='resource':
                    url+= f"?{k}={v}"
                else:
                    if v!= '':
                        url+= f"&{k}={v}"
        else:
            for cnt, (k, v) in enumerate(kwargs.items()):
                if cnt==0:
                    url+= f"?{k}={v}"
                else:
                    if v!= '':
                        url+= f"&{k}={v}"
        return url

class ripeAPI():

    @staticmethod
    def pfx2AS(pfxes: Union[str, list], query_time= ''):
        '''- 给定一个/一组prefix, 输出所属的AS(列表)
        - args-> query_time {`'2017-04-26T16:00'`}：查找过去某一时刻该pfx所属的AS
            - 注意：查询时间只能是00:00, 08:00, 16:00'''
        if isinstance(pfxes, str):
            pfxes= [pfxes]
        res= []
        for resource in pfxes:
            url= tools.fill_url('/data/prefix-overview/data.json', resource= resource, query_time= query_time)                           
            try:
                data= requests.get(url).json()['data']
                cur_res= {}
                cur_res['is_less_specific']= data['is_less_specific']
                cur_res['asns']= []
                cur_res['holders']= []
                for dic in data['asns']:
                    cur_res['asns'].append( dic['asn'])
                    cur_res['holders'].append( dic['holder'])
                res.append(cur_res)
            except:
                pass
        return res

    @staticmethod
    def AS2pfx(ASn:str, starttime='', endtime= ''):
        '''- 获取一个AS拥有的前缀列表
        - args-> starttime/endtime {`'2017-04-30T00:00'`}
        '''
        url= tools.fill_url('/data/announced-prefixes/data.json', resource= ASn, starttime= starttime, endtime= endtime)  
        try:
            data= requests.get(url).json()
            data= jsonpath.jsonpath(data['data']['prefixes'], '$..prefix')
            return data
        except:
            print('wrong with `starttime` or `endtime`')

    @staticmethod
    def pfx2all_upds(pfx= '170.247.0.0/24', starttime='', endtime='', rrcs=''):
        '''- 给定一个起止时间和前缀，输出一个list，其元素为关于该前缀的所有updates消息
        - args-> starttime/endtime {`'2023-01-31T00:00'`}
        - args-> rrcs {str}: 指定rrc, 形如`'14',或 '14,01'`
        '''
        url= tools.fill_url('/data/bgp-updates/data.json', resource= pfx, starttime= starttime, endtime= endtime, rrcs= rrcs)  
        data= requests.get(url).json()['data']['updates']
        return data

    @staticmethod
    def rrc2peer(query_time= ''):
        ''' - 获取指定时间(`'2023-01-31T00:00'`)的rrc列表及其peer子列表'''
        url= tools.fill_url('/data/ris-peers/data.json', query_time= query_time)
        data= requests.get(url).json()['data']['peers']
        return data

    @staticmethod
    def ip2pfx_and_AS(ips: Union[str, list]):
        '''- 查找ip所在的prefix和AS。可能返回空值。'''
        if isinstance(ips, str):
            ips= [ips]
        res= {}
        for ip in ips:
            url= tools.fill_url('/data/network-info/data.json', resource= ip)
            data= requests.get(url).json()['data']
            res[ip]= data
        return res
        
    @staticmethod
    def full_table_peer_list(query_time= ''):
        '''- 获取rrc中属于`full-table`的peers，即高视野peer。
        - 参数格式：`"2021-02-01T09:00"`
        - 返回2个set：`full-table`和非`full-table`, 其元素为`(asn, ip, pfx_version)` '''
        url_for_thd= tools.fill_url('/data/ris-full-table-threshold/data.json', query_time= query_time)
        data1= requests.get(url_for_thd).json()['data']
        v4_thd= data1['v4']
        v6_thd= data1['v6']

        whole_peer_list= ripeAPI.rrc2peer(query_time)
        p_full= set()
        p_nfull=set()
        for rrc, lis in whole_peer_list.items():
            for dic in lis:
                if dic['v4_prefix_count']>= v4_thd or dic['v6_prefix_count']>= v6_thd:
                    p_full.add( (dic['asn'], dic['ip'], dic['v4_prefix_count']+dic['v6_prefix_count']) )
                else:
                    p_nfull.add( (dic['asn'], dic['ip']) )
        return (p_full, p_nfull)

    @staticmethod
    def reserved_prefixes():
        '''- 获取保留IP地址块列表'''
        lis= [
            '0.0.0.0/8', 
            '10.0.0.0/8', 
            '100.64.0.0/10', 
            '127.0.0.0/8', 
            '169.254.0.0/16', 
            '172.16.0.0/12', 
            '192.0.0.0/24', 
            '192.0.2.0/24', 
            '192.88.99.0/24', 
            '192.168.0.0/16', 
            '198.18.0.0/15', 
            '198.51.100.0/24', 
            '203.0.113.0/24', 
            '224.0.0.0/4', 
            '233.252.0.0/24',
            '240.0.0.0/4', 
            '255.255.255.255/32'
        ]
        return lis


if __name__== "__main__":
    res= ripeAPI.full_table_peer_list("2021-02-01T09:00")
    '''with open('/home/huanglei/work/z_test/1_analysis_routing_flap/tt.json', 'w') as f:
        json.dump(res, f)'''
    print(res)
    print(len(res[0]), len(res[1]))
