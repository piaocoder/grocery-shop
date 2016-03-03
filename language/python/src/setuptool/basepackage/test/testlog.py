#!/usr/bin/python
# coding:utf-8

## 
# @file testlog.py
# @brief    test signal log
# @author unlessbamboo
# @version 0.1
# @date 2016-01-23


from basepackage.baselog import SignalLogHandle


def testDebug(sobj):
    """testDebug:test debug log.
    
    :sobj:  SignalLogHandle objects
    """
    # write debug(level-ERROR)
    sobj.sendDebug(sobj.ERROR, "Signal Test with Debug(error)")

    # write debug(level-INFO)
    sobj.sendDebug(sobj.INFO, "Signal Test with Debug(INFO)")
    
    # write debug(level-DEBUG)
    sobj.sendDebug(sobj.DEBUG, "Signal Test with Debug(DEBUG)")


def testError(sobj):
    """testError:test debug log.
    
    :sobj:  SignalLogHandle objects
    """
    # write debug(level-ERROR)
    sobj.sendError(sobj.ERROR, "Signal Test with Error(ERROR)")

    # write debug(level-INFO)
    sobj.sendError(sobj.INFO, "Signal Test with Error(INFO)")
    
    # write debug(level-DEBUG)
    sobj.sendError(sobj.DEBUG, "Signal Test with Error(DEBUG)")


if __name__ == '__main__':
    """main"""
    sobj = SignalLogHandle("/data/logs/job")
    testDebug(sobj)
    testError(sobj)
