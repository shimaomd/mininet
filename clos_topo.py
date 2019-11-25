#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController

import argparse
import sys
import time


class ClosTopo(Topo):

    def __init__(self, fanout, cores, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
       
        "Set up Core and Aggregate level, Connection Core - Aggregation level"
        #WRITE YOUR CODE HERE!
        core_switches = {}
        total_core_switches = cores
        s = 0
        for x in range(1, total_core_switches + 1):
            s += 1
            core_switches[x] = self.addSwitch('s%i' % s)
        print("Core switches")
        pp(core_switches)

        agg_switches = {}
        total_agg_switches = total_core_switches * fanout
        for x in range(1, total_agg_switches + 1):
            s += 1
            agg_switches[x] = self.addSwitch('s%i' % s)
        print("Aggregate switches:")
        pp(agg_switches)

        for x in core_switches:
            for y in agg_switches:
                self.addLink(core_switches[x], agg_switches[y])
        pass

        "Set up Edge level, Connection Aggregation - Edge level "
        #WRITE YOUR CODE HERE!

        edge_switches = {}
        total_edge_switches = total_agg_switches*fanout
        for x in xrange(total_edge_switches):
            s += 1
            edge_switches[x] = self.addSwitch('s%i' %s)
        print("Edge switches:")
        pp(edge_switches)

        for x in agg_switches:
            for y in edge_switches:
                self.addLink(agg_switches[x], edge_switches[y])
        pass
        hosts = {}
        total_hosts = total_edge_switches*fanout
        # for x in xrange(total_hosts):
        #     hosts[x] = self.addHost('h%i' %x)
        #
        for x in xrange(total_edge_switches):
            # add fanout number of hosts to each edge switch
            for y in xrange(fanout):
                n = x*fanout + y
                hosts[n] = self.addHost('h%i' %n)
                self.addLink(hosts[n], edge_switches[x])
        "Set up Host level, Connection Edge - Host level "
        #WRITE YOUR CODE HERE!
        pass
	

def setup_clos_topo(fanout=2, cores=1):
    "Create and test a simple clos network"
    assert(fanout>0)
    assert(cores>0)
    topo = ClosTopo(fanout, cores)
    net = Mininet(topo=topo, controller=lambda name: RemoteController('c0', "127.0.0.1"), autoSetMacs=True, link=TCLink)
    net.start()
    time.sleep(20) #wait 20 sec for routing to converge
    net.pingAll()  #test all to all ping and learn the ARP info over this process
    CLI(net)       #invoke the mininet CLI to test your own commands
    net.stop()     #stop the emulation (in practice Ctrl-C from the CLI 
                   #and then sudo mn -c will be performed by programmer)

    
def main(argv):
    parser = argparse.ArgumentParser(description="Parse input information for mininet Clos network")
    parser.add_argument('--num_of_core_switches', '-c', dest='cores', type=int, help='number of core switches')
    parser.add_argument('--fanout', '-f', dest='fanout', type=int, help='network fanout')
    args = parser.parse_args(argv)
    setLogLevel('info')
    setup_clos_topo(args.fanout, args.cores)


if __name__ == '__main__':
    main(sys.argv[1:])