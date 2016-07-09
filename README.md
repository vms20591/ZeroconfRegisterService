# ZeroconfRegisterService

A small module for service to register themselves with Zeroconf for easy advertisement

# Why ZeroconfRegisterService?

ZeroconfRegisterService is module written with the following usecase in
mind,

    1) Various sevices running in the system can register them
    as a service with this module

    2) A server can listen for the services and send them to
    a client who can browse these service

    3) In this way, there will be no hardcoding required to
    maintain a list of currently running services

#### Installation

You can install ZeroconfRegisterService by running the following command...

`sudo pip install git+https://github.com/vms20591/ZeroconfRegisterService.git`

Or by downloading the repository and running `sudo python setup.py install`.  
Installation via pip is suggested.

#### Service Registration Example
`````python
import ZeroconfRegisterService
import time

def register_service():
    config_object={
        'name':'my_service'
        'type':'mesh',
        'protocol':'tcp',
        'address':'192.168.1.1'
        'port':8000,
        'server_name':'myservice.p2p'
    }

    ZeroconfRegisterService.register_service(config_object)

    """
        This is added just not to kill the Zeroconf module
        which automatically invokes destroy callback within 
        the modules to unregister services and close Zeroconf.
        
        This is not required for a normal application like a
        web application, which would have a shutdown mechanism
        and at that time the destroy callback is called within
        the ZeroconfRegisterService module for cleanup activities.
    """
    while True:
        time.sleep(0.1)

if __name__=='__main__':
    register_service()
`````

---------------------
GNU GPL V3 LICENSE
