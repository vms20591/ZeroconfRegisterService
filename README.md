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
