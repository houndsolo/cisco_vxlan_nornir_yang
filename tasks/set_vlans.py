#!/usr/bin/env python3
from inventory.vars import *

from nornir import InitNornir
from nornir_netconf.plugins.tasks import netconf_edit_config, netconf_lock, netconf_commit, netconf_validate
from nornir_utils.plugins.functions import print_result


def configure_evpn_vlans(task):
    if task.host["vxlan_device_type"] == "leaf":

        vlan_evpn_config = []

        for evpn_vlan in evpn_vlans:
            evpn_vlan_snippet = f"""
              <configuration-entry xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vlan">
                <vlan-id>{evpn_vlan}</vlan-id>
                <member>
                  <evi-member>
                    <evpn-instance/>
                  </evi-member>
                </member>
              </configuration-entry>
            """
            vlan_evpn_config.append(evpn_vlan_snippet)


        config_payload = f"""
          <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <vlan>
          {''.join(vlan_evpn_config)}
            </vlan>
            </native>
          </config>
        """

        result = task.run(netconf_edit_config, config=config_payload, target="candidate")

def delete_evpn_vlans(task):
    if task.host["vxlan_device_type"] == "leaf":

        vlan_evpn_config = []

        for evpn_vlan in evpn_vlans:
            evpn_vlan_snippet = f"""
            <configuration-entry xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vlan" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">
              <vlan-id>{evpn_vlan}</vlan-id>
            </configuration-entry>
            """
            vlan_evpn_config.append(evpn_vlan_snippet)

        config_payload = f"""
          <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <vlan>
          {''.join(vlan_evpn_config)}
            </vlan>
            </native>
          </config>
        """

        result = task.run(netconf_edit_config, config=config_payload, target="candidate")

def configure_vlans(task):
    config_payload = f"""
      <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
          {vlan_configuration}
        </native>
      </config>
    """
    result = task.run(netconf_edit_config, config=config_payload, target="candidate")
