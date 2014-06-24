#!/usr/bin/env python

# Copyright 2014 ValeriyR
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pox.core import core                                           # Main POX object
import pox.openflow.libopenflow_01 as of                            # OpenFlow library
#import pox.lib.packet as pkt                                        # Network unit 
from pox.lib.revent import *                                        # Event library
#from pox.lib.util import dpidToStr                                  # Util dpidToStr
#from pox.samples.pretty_log import log.color                        # Module log
from pox.forwarding.l2_learning import LearningSwitch               # Module switch
from pox.lib.addresses import IPAddr                                # Address types
from collections import namedtuple                                  #
import os                                                           # OS component library
import csv                                                          # File configuration

#log = core.getLogger()                                              #Create a logger for this component
policyFile = "%s/pox/ext/nfw_rul.csv" % os.environ[ 'HOME' ]  

#Read the configuration file
entry = []
with open(policyFile) as f:
    next(f)
    csv_entry =  csv.reader(f, delimiter=',')
    for row in csv_entry:
        entry.append(row[1:])

class NanoFirewall (EventMixin):
    def __init__ (self):
        self.listenTo(core.openflow)
#        log.debug("Start NanoFirewall Module")
    
    def _handle_ConnectionUp (self, event):    
        #print "Switch %s has come up." %event.connection  # View dpid switch
        #core.getLogger().info("Connection %s" % (event.connection,)) # Conected MAC switch
        LearningSwitch(event.connection, False)     # Start module switch
#Logic
        for pair in entry:
            m = of.ofp_match()
            m.dl_type = 0x800
            m.nw_src = IPAddr(pair[0])
            m.nw_dst = IPAddr(pair[1])
            msg = of.ofp_flow_mod()
            msg.match = m
            event.connection.send(msg)

#        log.debug("NanoFirewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    print "INFO:Starting the NanoFirewall"
    core.registerNew(NanoFirewall)
