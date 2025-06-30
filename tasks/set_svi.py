#!/usr/bin/env python3
from inventory.vars import *

from nornir import InitNornir
from nornir_netconf.plugins.tasks import netconf_edit_config, netconf_lock, netconf_commit, netconf_validate
from nornir_utils.plugins.functions import print_result


def configure_evpn_svi(task):
    if "leaf" in task.host.groups:

        svi_config = []

        for evpn_svi in evpn_vlans:
            evpn_svi_snippet = f"""
          <interface>
            <Vlan>
              <name>{evpn_svi}</name>
              <ip>
                <address>
                  <primary>
                    <address>10.{evpn_svi}.0.5</address>
                    <mask>255.255.0.0</mask>
                  </primary>
                </address>
              </ip>
            </Vlan>
          </interface>
            """
            svi_config.append(evpn_svi_snippet)


        config_payload = f"""
          <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
          {''.join(svi_config)}
            </native>
          </config>
        """

        result = task.run(netconf_edit_config, config=config_payload, target="candidate")

