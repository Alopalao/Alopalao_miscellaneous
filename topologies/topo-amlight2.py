# cat /data/acanets-miami/home/italo/mydata/topo-amlight2.py
from mininet.topo import Topo

class AmlightTopo(Topo):
    """Amlight Topology."""
    def build(self):
        # Add switches
        Ampath1 = self.addSwitch('Ampath1', listenPort=6601, dpid='0000000000000011')
        Ampath2 = self.addSwitch('Ampath2', listenPort=6602, dpid='0000000000000012')
        SouthernLight2 = self.addSwitch('SoL2', listenPort=6603, dpid='0000000000000013')
        SanJuan = self.addSwitch('SanJuan', listenPort=6604, dpid='0000000000000014')
        AndesLight2 = self.addSwitch('AL2', listenPort=6605, dpid='0000000000000015')
        AndesLight3 = self.addSwitch('AL3', listenPort=6606, dpid='0000000000000016')
        Ampath3 = self.addSwitch('Ampath3', listenPort=6608, dpid='0000000000000017')
        Ampath4 = self.addSwitch('Ampath4', listenPort=6609, dpid='0000000000000018')
        Ampath5 = self.addSwitch('Ampath5', listenPort=6610, dpid='0000000000000019')
        Ampath7 = self.addSwitch('Ampath7', listenPort=6611, dpid='0000000000000020')
        JAX1 = self.addSwitch('JAX1', listenPort=6612, dpid='0000000000000021')
        JAX2 = self.addSwitch('JAX2', listenPort=6613, dpid='0000000000000022')
        Ampath8 = self.addSwitch('Ampath8', listenPort=6614, dpid='0000000000000008')
        # add hosts
        h1 = self.addHost('h1', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', mac='00:00:00:00:00:04')
        h5 = self.addHost('h5', mac='00:00:00:00:00:05')
        h6 = self.addHost('h6', mac='00:00:00:00:00:06')
        h7 = self.addHost('h7', mac='00:00:00:00:00:07')
        h8 = self.addHost('h8', mac='00:00:00:00:00:08')
        h9 = self.addHost('h9', mac='00:00:00:00:00:09')
        h10 = self.addHost('h10', mac='00:00:00:00:00:0A')
        h11 = self.addHost('h11', mac='00:00:00:00:00:0B')
        h12 = self.addHost('h12', mac='00:00:00:00:00:0C')
        h13 = self.addHost('h13', mac='00:00:00:00:00:0D')
        # Add links
        self.addLink(Ampath1, Ampath2, port1=1, port2=1)
        self.addLink(Ampath1, SouthernLight2, port1=2, port2=2)
        self.addLink(Ampath1, SouthernLight2, port1=3, port2=3)
        self.addLink(Ampath2, AndesLight2, port1=4, port2=4)
        self.addLink(SouthernLight2, AndesLight3, port1=5, port2=5)
        self.addLink(AndesLight3, AndesLight2, port1=6, port2=6)
        self.addLink(AndesLight2, SanJuan, port1=7, port2=7)
        self.addLink(SanJuan, Ampath2, port1=8, port2=8)
        self.addLink(Ampath1, Ampath3, port1=9, port2=9)
        self.addLink(Ampath2, Ampath3, port1=10, port2=10)
        self.addLink(Ampath1, Ampath4, port1=11, port2=11)
        self.addLink(Ampath2, Ampath5, port1=12, port2=12)
        self.addLink(Ampath4, Ampath5, port1=13, port2=13)
        self.addLink(Ampath4, JAX1, port1=14, port2=14)
        self.addLink(Ampath5, JAX2, port1=15, port2=15)
        self.addLink(Ampath4, Ampath7, port1=16, port2=16)
        self.addLink(Ampath7, SouthernLight2, port1=17, port2=17)
        self.addLink(JAX1, JAX2, port1=18, port2=18)
        self.addLink(Ampath1, Ampath8, port1=19, port2=19)
        self.addLink(h1, Ampath1, port1=1, port2=50)
        self.addLink(h2, Ampath2, port1=1, port2=51)
        self.addLink(h3, SouthernLight2, port1=1, port2=52)
        self.addLink(h4, SanJuan, port1=1, port2=53)
        self.addLink(h5, AndesLight2, port1=1, port2=54)
        self.addLink(h6, AndesLight3, port1=1, port2=55)
        self.addLink(h7, Ampath3, port1=1, port2=56)
        self.addLink(h8, Ampath4, port1=1, port2=57)
        self.addLink(h9, Ampath5, port1=1, port2=58)
        self.addLink(h10, Ampath7, port1=1, port2=59)
        self.addLink(h11, JAX1, port1=1, port2=60)
        self.addLink(h12, JAX2, port1=1, port2=61)
        self.addLink(h13, Ampath8, port1=1, port2=62)


# You can run any of the topologies above by doing:
# mn --custom tests/helpers.py --topo ring --controller=remote,ip=127.0.0.1
topos = {
    'amlight2': (lambda: AmlightTopo()),
}