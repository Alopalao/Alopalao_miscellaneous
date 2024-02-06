from mininet.topo import Topo

class RingTopo(Topo):
    """Ring topology with three switches
    and one host connected to each switch"""

    def build(self):
        # Create two hosts
        h1 = self.addHost('h1', ip='0.0.0.0')
        h2 = self.addHost('h2', ip='0.0.0.0')
        h3 = self.addHost('h3', ip='0.0.0.0')
        h4 = self.addHost('h4', ip='0.0.0.0')
        h5 = self.addHost('h5', ip='0.0.0.0')
        h6 = self.addHost('h6', ip='0.0.0.0')

        # Create the switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')

        # Add links between the switch and each host
        self.addLink(s1, h1)
        self.addLink(s2, h2)
        self.addLink(s3, h3)
        self.addLink(s4, h4)
        self.addLink(s5, h5)
        self.addLink(s6, h6)

        # Add links between the switchesz
        self.addLink(s1, s2)
        self.addLink(s1, s4)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
        self.addLink(s1, s5)
        self.addLink(s2, s5)
        self.addLink(s2, s6)
        self.addLink(s3, s6)

topos = {"min3": (lambda: RingTopo())}
