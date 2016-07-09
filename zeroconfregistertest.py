#!/usr/bin/env python
import ZeroconfRegisterService
import time

def register():
    ZeroconfRegisterService.register_service({
        'type':'mesh',
        'port':9000
    })

    while True:
        time.sleep(0.1)

if __name__=='__main__':
    register()
