import json
import mock
import unittest

from charmhelpers.contrib.openstack import utils


class UtilsTests(unittest.TestCase):
    def setUp(self):
        super(UtilsTests, self).setUp()

    @mock.patch.object(utils, 'config')
    @mock.patch('charmhelpers.contrib.openstack.utils.relation_set')
    @mock.patch('charmhelpers.contrib.openstack.utils.relation_ids')
    @mock.patch('charmhelpers.contrib.openstack.utils.get_ipv6_addr')
    def test_sync_db_with_multi_ipv6_addresses(self, mock_get_ipv6_addr,
                                               mock_relation_ids,
                                               mock_relation_set,
                                               mock_config):
        mock_config.return_value = None
        addr1 = '2001:db8:1:0:f816:3eff:fe45:7c/64'
        addr2 = '2001:db8:1:0:d0cf:528c:23eb:5000/64'
        mock_get_ipv6_addr.return_value = [addr1, addr2]
        mock_relation_ids.return_value = ['shared-db']

        utils.sync_db_with_multi_ipv6_addresses('testdb', 'testdbuser')
        hosts = json.dumps([addr1, addr2])
        mock_relation_set.assert_called_with(relation_id='shared-db',
                                             database='testdb',
                                             username='testdbuser',
                                             hostname=hosts)

    @mock.patch.object(utils, 'config')
    @mock.patch('charmhelpers.contrib.openstack.utils.relation_set')
    @mock.patch('charmhelpers.contrib.openstack.utils.relation_ids')
    @mock.patch('charmhelpers.contrib.openstack.utils.get_ipv6_addr')
    def test_sync_db_with_multi_ipv6_addresses_single(self, mock_get_ipv6_addr,
                                                      mock_relation_ids,
                                                      mock_relation_set,
                                                      mock_config):
        mock_config.return_value = None
        addr1 = '2001:db8:1:0:f816:3eff:fe45:7c/64'
        mock_get_ipv6_addr.return_value = [addr1]
        mock_relation_ids.return_value = ['shared-db']

        utils.sync_db_with_multi_ipv6_addresses('testdb', 'testdbuser')
        hosts = json.dumps([addr1])
        mock_relation_set.assert_called_with(relation_id='shared-db',
                                             database='testdb',
                                             username='testdbuser',
                                             hostname=hosts)

    @mock.patch.object(utils, 'config')
    @mock.patch('charmhelpers.contrib.openstack.utils.relation_set')
    @mock.patch('charmhelpers.contrib.openstack.utils.relation_ids')
    @mock.patch('charmhelpers.contrib.openstack.utils.get_ipv6_addr')
    def test_sync_db_with_multi_ipv6_addresses_w_prefix(self,
                                                        mock_get_ipv6_addr,
                                                        mock_relation_ids,
                                                        mock_relation_set,
                                                        mock_config):
        mock_config.return_value = None
        addr1 = '2001:db8:1:0:f816:3eff:fe45:7c/64'
        mock_get_ipv6_addr.return_value = [addr1]
        mock_relation_ids.return_value = ['shared-db']

        utils.sync_db_with_multi_ipv6_addresses('testdb', 'testdbuser',
                                                relation_prefix='bungabunga')
        hosts = json.dumps([addr1])
        mock_relation_set.assert_called_with(relation_id='shared-db',
                                             bungabunga_database='testdb',
                                             bungabunga_username='testdbuser',
                                             bungabunga_hostname=hosts)

    @mock.patch.object(utils, 'config')
    @mock.patch('charmhelpers.contrib.openstack.utils.relation_set')
    @mock.patch('charmhelpers.contrib.openstack.utils.relation_ids')
    @mock.patch('charmhelpers.contrib.openstack.utils.get_ipv6_addr')
    def test_sync_db_with_multi_ipv6_addresses_vips(self, mock_get_ipv6_addr,
                                                    mock_relation_ids,
                                                    mock_relation_set,
                                                    mock_config):
        addr1 = '2001:db8:1:0:f816:3eff:fe45:7c/64'
        addr2 = '2001:db8:1:0:d0cf:528c:23eb:5000/64'
        vip1 = '2001:db8:1:0:f816:3eff:32b3:7c'
        vip2 = '2001:db8:1:0:f816:3eff:32b3:7d'
        mock_config.return_value = '%s 10.0.0.1 %s' % (vip1, vip2)

        mock_get_ipv6_addr.return_value = [addr1, addr2]
        mock_relation_ids.return_value = ['shared-db']

        utils.sync_db_with_multi_ipv6_addresses('testdb', 'testdbuser')
        hosts = json.dumps([addr1, addr2, vip1, vip2])
        mock_relation_set.assert_called_with(relation_id='shared-db',
                                             database='testdb',
                                             username='testdbuser',
                                             hostname=hosts)

    @mock.patch('uuid.uuid4')
    @mock.patch('charmhelpers.contrib.openstack.utils.related_units')
    @mock.patch('charmhelpers.contrib.openstack.utils.relation_set')
    @mock.patch('charmhelpers.contrib.openstack.utils.relation_ids')
    def test_remote_restart(self, mock_relation_ids, mock_relation_set,
                            mock_related_units, mock_uuid4):
        mock_relation_ids.return_value = ['neutron-plugin-api-subordinate:8']
        mock_related_units.return_value = ['neutron-api/0']
        mock_uuid4.return_value = 'uuid4'
        utils.remote_restart('neutron-plugin-api-subordinate')
        mock_relation_set.assert_called_with(
            relation_id='neutron-plugin-api-subordinate:8',
            relation_settings={'restart-trigger': 'uuid4'}
        )

    @mock.patch.object(utils, 'config')
    @mock.patch('charmhelpers.contrib.openstack.utils.'
                'git_os_codename_install_source')
    @mock.patch('charmhelpers.contrib.openstack.utils.get_os_codename_package')
    @mock.patch('charmhelpers.contrib.openstack.utils.'
                'get_os_codename_install_source')
    def test_os_release(self, mock_get_os_codename_install_source,
                        mock_get_os_codename_package,
                        mock_git_os_codename_install_source,
                        mock_config):
        # Wipe the modules cached os_rel
        utils.os_rel = None
        mock_get_os_codename_install_source.return_value = None
        mock_get_os_codename_package.return_value = None
        mock_git_os_codename_install_source.return_value = None
        mock_config.return_value = 'cloud-pocket'
        self.assertEqual(utils.os_release('my-pkg'), 'essex')
        mock_get_os_codename_install_source.assert_called_once_with(
            'cloud-pocket')
        mock_get_os_codename_package.assert_called_once_with(
            'my-pkg', fatal=False)
        mock_git_os_codename_install_source.assert_called_once_with(
            'cloud-pocket')
        # Next call to os_release should pickup cached version
        mock_get_os_codename_install_source.reset_mock()
        mock_get_os_codename_package.reset_mock()
        mock_git_os_codename_install_source.reset_mock()
        self.assertEqual(utils.os_release('my-pkg'), 'essex')
        self.assertFalse(mock_get_os_codename_install_source.called)
        self.assertFalse(mock_get_os_codename_package.called)
        self.assertFalse(mock_git_os_codename_install_source.called)
        # Call os_release and bypass cache
        mock_get_os_codename_install_source.reset_mock()
        mock_get_os_codename_package.reset_mock()
        mock_git_os_codename_install_source.reset_mock()
        self.assertEqual(utils.os_release('my-pkg', reset_cache=True),
                         'essex')
        mock_get_os_codename_install_source.assert_called_once_with(
            'cloud-pocket')
        mock_get_os_codename_package.assert_called_once_with(
            'my-pkg', fatal=False)
        mock_git_os_codename_install_source.assert_called_once_with(
            'cloud-pocket')
