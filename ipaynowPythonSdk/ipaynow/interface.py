#!/usr/bin/env python
# -*- coding: utf-8; mode: python; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- vim:fenc=utf-8:ft=python:et:sw=4:ts=4:sts=4
from ipaynow.packMsg import PackMsgSend
from ipaynow.paramlist import WP001_PostList, WP001_RespList
from ipaynow.paramlist import MQ001_PostList, MQ001_RespList
from ipaynow.paramlist import N001_QueryList, N001_RespList
from ipaynow.paramlist import N002_NotifyList
from ipaynow.unpackMsg import UnpackMsgRecv
#from ipaynow.utils import trans2unicode
def trade(payparam = {}):
    '''
    trade interface.
    输入发起交易的字典参数.
    详细信息见文档:WP001-无插件聚合支付
    '''
    pms = PackMsgSend(payparam,WP001_PostList)
    return pms.getResultString()

def query(queryparam = {}):
    '''
    query interface.
    输入查询的字典参数.
    详细信息见文档:MQ001-商户支付订单查询
    '''
    pms = PackMsgSend(queryparam,MQ001_PostList)
    return pms.getResultString()

# def notify(notifyparam = {}):
#     pms = PackMsgSend(notifyparam,N001_Resplist)
#     return pms.getResultString()

def notify(frontNotifyParam = 'Y'):
    stringRtn = "{'success':'%s'}" %frontNotifyParam
    return stringRtn

def parseTrade(instr = ""):
    upm = UnpackMsgRecv(instr,WP001_RespList)
    recvDict = upm.getResultDict()
    isVerified = upm.verifyResponse()
    return (recvDict,isVerified)

def parseQuery(instr = ""):
 #   instrunicode = trans2unicode(instr)
    upm = UnpackMsgRecv(instr,MQ001_RespList)
    recvDict = upm.getResultDict()
    isVerified = upm.verifyResponse()
    return (recvDict,isVerified)

def parseNotify(instr = ""):
    upm = UnpackMsgRecv(instr,N001_QueryList)
    recvDict = upm.getResultDict()
    isVerified = upm.verifyResponse()
    return (recvDict,isVerified)

def parseFrontNotify(instr = ""):
    upm = UnpackMsgRecv(instr,N002_NotifyList)
    recvDict = upm.getResultDict()
    isVerified = upm.verifyResponse()
    return (recvDict,isVerified)
