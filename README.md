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
from flask import Flask

app=Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

config_object={
    'name':'my_web_app',
    'type':'mesh',
    'protocol':'tcp',
    'address':'192.168.1.1'
    'port':8000,
    'server_name':'mywebapp.p2p'
}

if __name__=='__main__':
    ZeroconfRegisterService.register_service(config_object)
    app.run(debug=True,use_reloader=False)
`````

---------------------
LICENSE

GNU GPL V3. Refer to the LICENSE files for details
