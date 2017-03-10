from twisted.internet import reactor, protocol

HOST = 'localhost'
PORT = 9000

class EC(protocol.Protocol):
    def connectionMade(self):
        print("connected!")

class ECFactory(protocol.ClientFactory):
    protocol = EC

print("Running EC")
factory = ECFactory()
reactor.connectTCP(HOST, PORT, factory)

reactor.run()
