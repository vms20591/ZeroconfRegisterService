# -*- coding: utf-8 -*-
"""
    ZeroconfRegisterService is module written with the following usecase in
    mind,

        1) Various sevices running in the system can register them
        as a service with this module

        2) A server can listen for the services and send them to
        a client who can browse these service

        3) In this way, there will be no hardcoding required to
        maintain a list of currently running services

    This module is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public V3 License for more details.

"""

#Import Section
import socket
import time
import netifaces
import threading
import atexit
import logging
import hashlib
import os
from zeroconf import Zeroconf,ServiceInfo

__author__ = 'Meenakshi Sundaram V'
__maintainer__ = 'Meenakshi Sundaram <vms20591@gmail.com>'
__version__ = '0.1'
__license__ = 'GPL V3'

#Only register_service is required by clients to register their service
__all__ = ['register_service']

#Setup logger
level=os.environ.get('ZEROCONFREGISTER_LOG_LEVEL',logging.DEBUG)
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=level)
logger=logging.getLogger(__name__)

#Some global constants
ADDRESS='127.0.0.1'
PORT=3000
HOSTNAME=socket.gethostname()
USERNAME=os.environ.get('USER','default')
PEERNAME=USERNAME+"@"+HOSTNAME

#Initialise zeroconf
zeroconf=Zeroconf()

def initialise_host():
    """
        Find out the default interface on this machine (for ex: eth)
        and derive the IP address allocated
    """

    global ADDRESS

    interface=netifaces.gateways()['default'][netifaces.AF_INET][1]
    logger.debug("Inteface for default gateway is: "+interface)

    ADDRESS=netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    logger.debug("IP address of %s is %s"%(socket.gethostname(),ADDRESS))

def close_zeroconf():
    """
        Callback function that is called when the program exits in order to
        do the following,
            1) Unregister all services with zeroconf instance
            2) Close zeroconf
    """

    if zeroconf:
        logger.info("Unregistering all services from current Zeroconf object")
        zeroconf.unregister_all_services()
        logger.info("Services unregistered")

        logger.info("Closing Zerconf")
        zeroconf.close()
        logger.info("Zeroconf successfully closed")

def register_service(config_object={}):
    """
        API called by clients to register themselves as service.

        :type config_object: :dict: Configuration items for Zeroconf

        Example: If a service like mediagoblin wants to announce its
        presence it will have a config object something like below and
        register with it.

            config_object={
                'name':'mediagoblin',
                'type':'mesh',
                'protocol':'tcp',
                'address':'192.168.1.1'
                'port':80,
                'server_name':'mediagoblin.p2p'
            }

            register_service(config_object)
    """

    #Initialise host to find the IP address of the current default interface
    initialise_host()

    logger.debug("Creating a new thread to register the service and start it")
    ZeroconfService(config_object,zeroconf).start()

class ZeroconfService(threading.Thread):
    """
        ZeroconfService is the heart of the module which runs as a daemon thread
        and registers the client as a service.

        This is subclassed as a daemon thread because, once the client calls this API
        from their function and once it terminates we don't want the zeroconf object
        to be garbage collected.
    """

    def __init__(self,config_object={},zeroconf=None):
        """
            __init__() called from the register_service function, which passes the
            config object and the Zeroconf instance.

            :type config_object:    :dict: Configuration items for Zeroconf
            :type zeroconf:         :class: Zeroconf instance
        """

        #call the parent constructor
        threading.Thread.__init__(self)

        #Mark this thread as daemon
        self.daemon=True

        #store in the config object in the instance
        self.config_object=config_object

        #store the zeroconf instance if present or 
        #initialize a new one
        if not zeroconf:
            self.zeroconf=Zeroconf()
        else:
            self.zeroconf=zeroconf

    def run(self):
        """
            call register_service instance method to kick off
            the registration activity
        """

        self.register_service()

    def form_zeroconf_qualified_name(self):
        """
            Helper method that creates fully qualified Zeroconf names from
            the client input.

            Ex: If a service like mediagoblin wants to announce its
            presence it will have a config object something like below and
            register with it.

            config_object={
                'name':'mediagoblin'
                'type':'mesh',
                'protocol':'tcp',
                'address':'192.168.1.1'
                'port':80,
                'domain':'local',
                'server_name':'mediagoblin.p2p'
            }

            The name and type would be transformed to,
            
            name (fqdn) => mediagoblin._mesh._tcp.local.
            type => _mesh._tcp.local.
        """

        peername=PEERNAME

        #retrieve all the params from the config object
        name=self.config_object.get('name',None)
        typ=self.config_object.get('type','http')
        protocol=self.config_object.get('protocol','tcp')
        domain=self.config_object.get('domain','local')

        #This is used just in case there is no name from the client
        if not name:
            name=peername+"_"+hashlib.sha512(peername+os.urandom(10)).hexdigest()[:6]

        #form the fully qualified names as expected by Zeroconf
        basename='_'+typ+'.'+'_'+protocol+'.'+domain+'.'
        fqdn=name+'.'+basename
        server_name=HOSTNAME+'.'+domain

        #store the fully qualified names in the config object
        self.config_object['fqdn']=fqdn
        self.config_object['basename']=basename
        self.config_object['server_name']=self.config_object.get('server_name',server_name)

    def register_service(self):
        """
            Register the service with Zeroconf with the client provided config object
        """

        #form fully qualified domain names
        logger.debug("Converting application input to fully qualified Zerconf names")
        self.form_zeroconf_qualified_name()

        #create ServiceInfo instance from the config object
        logger.debug("Creating ServiceInfo object for service")
        info=ServiceInfo(self.config_object.get('basename'),
            self.config_object.get('fqdn'),
            socket.inet_aton(ADDRESS),
            self.config_object.get('port',PORT),
            0,
            0,
            self.config_object.get('desc',{}),
            self.config_object.get('server_name'))

        #Register the service with Zeroconf
        logger.debug("Registering service with the ServiceInfo object")
        self.zeroconf.register_service(info)
        logger.debug("Service registered")

"""
    This hook is added when the module is terminated in order to,
        1) Unregister all the services with the current instance
        2) Close Zeroconf
"""
atexit.register(close_zeroconf)
