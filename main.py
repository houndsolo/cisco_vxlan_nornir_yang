#!/usr/bin/env python3
import time
from inventory.vars import *
from inventory.vyos_leafs import *

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netconf.plugins.tasks import netconf_edit_config, netconf_lock, netconf_commit, netconf_validate
from nornir_utils.plugins.functions import print_result

from tasks.netconf_locks        import  global_lock, global_unlock
from tasks.set_system_settings  import  system_config_payload
from tasks.set_p2p_links        import  set_p2p_links
from tasks.set_bgp              import  set_bgp
from tasks.set_vlans            import  configure_vlans, configure_evpn_vlans, delete_evpn_vlans


def configure_vxlan(task,num_leafs,num_spines):

    ## delete vlans first, EVI instance needs to be configured when there are no evpn vlans
    #task.run(task=global_lock)
    #task.run(task=delete_evpn_vlans)
    #task.run(netconf_validate)
    #task.run(netconf_commit, manager=task.host["manager"])
    #task.run(task=global_unlock)

    # rest of evpn vxlan config
    task.run(task=global_lock)

    task.run(
        task=system_config_payload,
    )
    task.run(
        task=set_p2p_links,
        num_spines=num_spines,
        num_leafs=num_leafs
    )
    task.run(
        task=set_bgp,
        num_spines=num_spines,
        num_leafs=num_leafs
    )

    task.run(netconf_validate)
    task.run(netconf_commit, manager=task.host["manager"])

    task.run(task=global_unlock)


    # set vlans last, EVI instance needs to be configured first
    task.run(task=global_lock)
    task.run(task=configure_evpn_vlans)
    task.run(netconf_validate)
    task.run(netconf_commit, manager=task.host["manager"])
    task.run(task=global_unlock)

    #task.run(task=global_lock)
    #task.run(task=configure_vlans)
    #task.run(netconf_validate)
    #task.run(netconf_commit, manager=task.host["manager"])
    #task.run(task=global_unlock)

def main():
    nr = InitNornir(config_file="config.yml")
    nr_spines = nr.filter(F(groups__contains="spine"))
    nr_leafs = nr.filter(F(groups__contains="leaf"))
    nr_s7 = nr.filter(hostname="10.20.0.7")
    nr_s9 = nr.filter(hostname="10.20.0.9")
    nr_s8 = nr.filter(hostname="10.20.0.8")
    nr_s10 = nr.filter(hostname="10.20.0.10")

    results = nr.run(task=configure_vxlan, num_spines=num_spines, num_leafs=num_leafs)
    print_result(results)

if __name__ == "__main__":
    main()
