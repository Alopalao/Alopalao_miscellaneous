from mininet.topo import Topo

class Ring4Topo(Topo):
    """Create a network from semi-scratch with multiple controllers."""

    def build(self):
        # ("*** Creating switches\n")
        s1 = self.addSwitch('s1', listenPort=6601, dpid="1")
        s2 = self.addSwitch('s2', listenPort=6602, dpid="2")
        s3 = self.addSwitch('s3', listenPort=6603, dpid="3")
        s4 = self.addSwitch('s4', listenPort=6604, dpid="4")

        # ("*** Creating hosts\n")
        hosts1 = [self.addHost('h%d' % n) for n in (1, 2)]
        hosts2 = [self.addHost('h%d' % n) for n in (3, 4)]
        hosts3 = [self.addHost('h%d' % n) for n in (5, 6)]
        hosts4 = [self.addHost('h%d' % n) for n in (7, 8)]

        # ("*** Creating links\n")
        for h in hosts1:
            self.addLink(s1, h)
        for h in hosts2:
            self.addLink(s2, h)

        self.addLink(s1, s2)
        self.addLink(s2, s3)

        for h in hosts3:
            self.addLink(s3, h)
        for h in hosts4:
            self.addLink(s4, h)

        self.addLink(s3, s4)
        self.addLink(s4, s1)


topos = {
    'ring4': (lambda: Ring4Topo()),
}