import unittest
import mock
import os

from pyhpecw7.features.config import Config
from .base_feature_test import BaseFeatureCase

FILENAME = '/path/to/file.cfg'
BASENAME = os.path.basename(FILENAME)

class ConfigTestCase(BaseFeatureCase):

    @mock.patch('pyhpecw7.comware.HPCOM7')
    def setUp(self, mock_device):
        self.device = mock_device
        self.config = Config(self.device, FILENAME)

    def test_init(self):
        self.assertEqual(self.config.filename, FILENAME)
        self.assertEqual(self.config.basename, BASENAME)

    def test_get_diffs(self):
        result = self.config._get__diffs_from_switch()
        self.device.cli_display.assert_called_with('display diff current-configuration configfile file.cfg')

    def test_compare_config(self):
        self.config._diff_response = self.read_cli_display('display_diff')

        result = self.config.compare_config()
        expected = (['+port group interface FortyGigE1/0/1', '+port group interface FortyGigE1/0/2', '+irf domain 1', '+flash:/safety_file.cfg', '+name VLAN_77', '+description instant vlan', '+name web_vlan', '+irf-port 1/2', '+irf-port 1/1', '-name VLAN100_VRRP_TEST', '-description vlan 3 for testing', '-destination 10.1.1.2', '-mad exclude interface FortyGigE1/0/10', '-interface LoopBack29', '-interface Tunnel22 mode vxlan', '-vrrp vrid 100 authentication-mode md5 cipher $c$3$sBCWj6+b6pWNZe7D6EQSfsG4j4ca1SASow==', '-interface Vlan-interface100', '-lacp mode passive', '-vrrp vrid 100 priority 10', '-name hello', '-name VLAN5_TEST', '-vlan 100', '-Current configuration', '-interface Bridge-Aggregation3', '-port link-mode route', '-mad exclude interface FortyGigE1/0/9', '-vlan 3', '-ip address 100.100.100.2 255.255.255.0', '-vrrp vrid 100 virtual-ip 100.100.100.1', '-source 10.1.1.1', '-interface Tunnel20 mode vxlan', '-interface Tunnel24 mode vxlan', '-irf domain 2', '-tunnel global source-address 10.10.10.10', '-vlan 2', '-description goodbye', '-description vlan 5 for testing', '-interface Tunnel21 mode vxlan', '-name VLAN3_TEST', '-interface Tunnel23 mode vxlan', '-l2vpn enable'], ['<HP1>display diff current-configuration configfile safety_file.cfg', '--- Current configuration', '+++ flash:/safety_file.cfg', '@@ -5,7 +5,7 @@', ' #', '  clock protocol none', ' #', '- irf domain 2', '+ irf domain 1', '  irf mac-address persistent timer', '  irf auto-update enable', '  undo irf link-delay', '@@ -13,8 +13,6 @@', '  irf member 1 description They used to call me HP1', '  irf mode normal', ' #', '- tunnel global source-address 10.10.10.10', '-#', '  lldp global enable', ' #', '  system-working-mode standard', '@@ -23,72 +21,31 @@', ' #', ' vlan 1', ' #', '-vlan 2', '-#', '-vlan 3', '- name VLAN3_TEST', '- description vlan 3 for testing', '-#', ' vlan 5', '- name VLAN5_TEST', '- description vlan 5 for testing', '+ name web_vlan', ' #', ' vlan 20', '  name VLAN20', ' #', ' vlan 77', '- name hello', '- description goodbye', '+ name VLAN_77', '+ description instant vlan', ' #', '-vlan 100', '- name VLAN100_VRRP_TEST', '+irf-port 1/1', '+ port group interface FortyGigE1/0/1', ' #', '+irf-port 1/2', '+ port group interface FortyGigE1/0/2', '+#', '  stp global enable', ' #', '- l2vpn enable', '-#', '-interface Bridge-Aggregation3', '-#', ' interface NULL0', ' #', '-interface LoopBack29', '-#', '-interface Vlan-interface100', '- ip address 100.100.100.2 255.255.255.0', '- vrrp vrid 100 virtual-ip 100.100.100.1', '- vrrp vrid 100 authentication-mode md5 cipher $c$3$sBCWj6+b6pWNZe7D6EQSfsG4j4ca1SASow==', '- vrrp vrid 100 priority 10', '-#', '-interface FortyGigE1/0/9', '- port link-mode route', '-#', '-interface FortyGigE1/0/27', '- port link-mode route', '-#', '-interface FortyGigE1/0/28', '- port link-mode route', '-#', '-interface FortyGigE1/0/29', '- port link-mode route', '-#', '-interface FortyGigE1/0/30', '- port link-mode route', '-#', '-interface FortyGigE1/0/1', '- port link-mode bridge', '- shutdown', '-#', '-interface FortyGigE1/0/2', '- port link-mode bridge', '- shutdown', '-#', ' interface FortyGigE1/0/3', '  port link-mode bridge', '- shutdown', ' #', ' interface FortyGigE1/0/4', '  port link-mode bridge', '- shutdown', ' #', ' interface FortyGigE1/0/5', '  port link-mode bridge', '@@ -102,12 +59,14 @@', ' interface FortyGigE1/0/8', '  port link-mode bridge', ' #', '+interface FortyGigE1/0/9', '+ port link-mode bridge', '+#', ' interface FortyGigE1/0/10', '  port link-mode bridge', ' #', ' interface FortyGigE1/0/11', '  port link-mode bridge', '- lacp mode passive', ' #', ' interface FortyGigE1/0/12', '  port link-mode bridge', '@@ -154,35 +113,32 @@', ' interface FortyGigE1/0/26', '  port link-mode bridge', ' #', '-interface FortyGigE1/0/31', '+interface FortyGigE1/0/27', '  port link-mode bridge', ' #', '-interface FortyGigE1/0/32', '+interface FortyGigE1/0/28', '  port link-mode bridge', ' #', '-interface M-GigabitEthernet0/0/0', '- ip address 10.1.100.40 255.255.255.0', '+interface FortyGigE1/0/29', '+ port link-mode bridge', ' #', '-interface Tunnel20 mode vxlan', '- source 10.1.1.1', '- destination 10.1.1.2', '+interface FortyGigE1/0/30', '+ port link-mode bridge', ' #', '-interface Tunnel21 mode vxlan', '- source 10.1.1.1', '- destination 10.1.1.2', '+interface FortyGigE1/0/31', '+ port link-mode bridge', ' #', '-interface Tunnel22 mode vxlan', '- source 10.1.1.1', '- destination 10.1.1.2', '+interface FortyGigE1/0/32', '+ port link-mode bridge', ' #', '-interface Tunnel23 mode vxlan', '- source 10.1.1.1', '- destination 10.1.1.2', '+interface FortyGigE1/0/1', '+ shutdown', ' #', '-interface Tunnel24 mode vxlan', '- source 10.1.1.1', '- destination 10.1.1.2', '+interface FortyGigE1/0/2', ' #', '+interface M-GigabitEthernet0/0/0', '+ ip address 10.1.100.40 255.255.255.0', '+#', '  scheduler logfile size 16', ' #', ' line class aux', '@@ -205,9 +161,6 @@', '  user-role network-operator', ' #', '  ip route-static 0.0.0.0 0 10.1.100.1', '-#', '- mad exclude interface FortyGigE1/0/9', '- mad exclude interface FortyGigE1/0/10', ' #', '  ssh server enable', '  ssh user hp service-type all authentication-type password'])

        self.assertEqual(set(result[0]), set(expected[0]))
        self.assertEqual(set(result[1]), set(expected[1]))

    def test_build(self):
        self.config.build()
        self.device.save.assert_any_call('safety_file.cfg')
        self.device.rollback.assert_called_with(self.config.basename)
        self.device.save.assert_any_call('startup.cfg')

        self.config.build(stage=True)
        self.assert_stage_requests_multiple([['safety_file.cfg', 'save'], [self.config.basename, 'rollback'], ['startup.cfg', 'save']])




if __name__ == "__main__":
    unittest.main()