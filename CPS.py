from twisted.internet import reactor, protocol

PORT = 9000

class CPS(protocol.Protocol):
    pass

class CPSFactory(protocol.Factory):
    protocol = CPS

print("Running Server")
factory = CPSFactory()
reactor.listenTCP(PORT, factory)
reactor.run()
