"""Source-only host-access regressions. Ordinary UID, fixture files and strict mocks."""
import ast
import copy
import hashlib
import importlib.util
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
BASE = 'ccd31c20a8ec918454aa5aa455972860be17e3bf'
spec = importlib.util.spec_from_file_location('host_access_controller', str(ROOT / 'ops/dev/deploy_controller.py'))
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)


class HostAccessNetworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Read committed Git DATA before installing the no-subprocess guard.
        cls.frozen = {file: subprocess.check_output([str(ROOT / 'scripts/repo-git.sh'), 'show', BASE + ':' + file])
            for file in ('package.json', 'package-lock.json', 'ops/dev/runtime.Dockerfile', 'ops/dev/trusted/gateway.mjs',
                         'ops/dev/prepare_image.py', 'ops/dev/install-root.sh', 'ops/dev/install_preflight.py')}

    def setUp(self):
        self.assertNotEqual(os.geteuid(), 0, 'Ordinary-user fixtures only')
        base = ROOT / '.ops/test-artifacts'; base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=str(base)); self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.ids = {controller.NETWORK: 'a' * 64, controller.EGRESS: 'b' * 64, controller.HOST_ACCESS_NETWORK: 'c' * 64}
        self.names = {controller.APP: '1' * 64, controller.PROXY: '2' * 64, controller.GATEWAY: '3' * 64}
        for file, name in [('network-id', controller.NETWORK), ('egress-network-id', controller.EGRESS),
                           ('host-access-network-id', controller.HOST_ACCESS_NETWORK)]:
            (self.root / file).write_text(self.ids[name])
        self.containers = {}
        for name, identifier in self.names.items():
            networks = {controller.NETWORK: {'NetworkID': self.ids[controller.NETWORK]}}
            if name == controller.PROXY:
                networks[controller.EGRESS] = {'NetworkID': self.ids[controller.EGRESS]}
            elif name == controller.GATEWAY:
                networks[controller.HOST_ACCESS_NETWORK] = {'NetworkID': self.ids[controller.HOST_ACCESS_NETWORK],
                    'IPAddress': '172.31.255.2', 'IPPrefixLen': 29, 'GlobalIPv6Address': ''}
            self.containers[identifier] = {'Id': identifier, 'Name': '/' + name, 'Image': 'sha256:' + 'e' * 64,
                'Config': {'Labels': {'gcreation.role': {controller.APP: 'app', controller.PROXY: 'proxy', controller.GATEWAY: 'gateway'}[name]}},
                'NetworkSettings': {'Networks': networks, 'Ports': {}}, 'HostConfig': {'PortBindings': {}, 'PublishAllPorts': False}}
        self.networks = {}
        for name, allowed, internal, role in [(controller.NETWORK, set(self.names), True, 'dev-audit'),
                (controller.EGRESS, {controller.PROXY}, False, 'dev-audit-egress'),
                (controller.HOST_ACCESS_NETWORK, {controller.GATEWAY}, True, 'dev-host-access')]:
            members = {self.names[n]: {'Name': n} for n in allowed}
            if name == controller.HOST_ACCESS_NETWORK:
                members[self.names[controller.GATEWAY]]['IPv4Address'] = '172.31.255.2/29'
            self.networks[name] = {'Name': name, 'Id': self.ids[name], 'Internal': internal, 'Driver': 'bridge',
                'Scope': 'local', 'Labels': {'gcreation.role': role}, 'Containers': members}
        self.networks[controller.HOST_ACCESS_NETWORK]['IPAM'] = {'Driver': 'default', 'Options': None,
            'Config': [{'Subnet': '172.31.255.0/29', 'Gateway': '172.31.255.1'}]}
        for target in [mock.patch.object(controller, 'STATE', self.root),
                mock.patch.object(controller, 'runtime_image', return_value='sha256:' + 'e' * 64),
                mock.patch.object(controller, 'command'),
                mock.patch.object(controller, 'docker_json', side_effect=self.inspect),
                mock.patch.object(socket, 'socket', side_effect=AssertionError('Network forbidden')),
                mock.patch.object(controller.subprocess, 'run', side_effect=AssertionError('Host subprocess forbidden'))]:
            value = target.start(); self.addCleanup(target.stop)
            if getattr(target, 'attribute', '') == 'command':
                self.commands = value

    def inspect(self, args):
        if args[:2] == ['network', 'ls']:
            return {'Name': 'fixture-existing'}
        if args[:2] == ['network', 'inspect']:
            return copy.deepcopy(self.networks[args[-1]])
        if args[:2] == ['container', 'inspect']:
            return copy.deepcopy(self.containers[args[-1]])
        raise AssertionError('Unexpected inspection')

    def host(self):
        return self.networks[controller.HOST_ACCESS_NETWORK]

    def gateway(self):
        return self.containers[self.names[controller.GATEWAY]]

    def assert_host_rejected(self):
        with self.assertRaises(ValueError):
            controller.ensure_host_access_network()
        self.commands.assert_not_called()

    def test_fixed_constants_cannot_be_overridden_by_environment(self):
        expected = {'HOST_ACCESS_NETWORK': 'gcreation-perf-dev-host-access', 'HOST_ACCESS_ROLE': 'dev-host-access',
            'HOST_ACCESS_SUBNET': '172.31.255.0/29', 'HOST_ACCESS_BRIDGE_GATEWAY': '172.31.255.1',
            'GATEWAY_HOST_ACCESS_IP': '172.31.255.2', 'HOST_ACCESS_NETWORK_ID_FILE': 'host-access-network-id',
            'ENGINE_HOST_URL': 'http://172.31.255.2:3101'}
        with mock.patch.dict(os.environ, {k: 'attacker' for k in expected}):
            self.assertEqual({k: getattr(controller, k) for k in expected}, expected)

    def test_creation_exact_flags_and_private_persisted_identity(self):
        (self.root / 'host-access-network-id').unlink()
        self.host()['Containers'] = {}
        with mock.patch.object(controller, 'docker_json', side_effect=[None, self.host()]):
            controller.ensure_host_access_network()
        self.commands.assert_called_once_with(['docker', 'network', 'create', '--driver=bridge', '--internal',
            '--subnet=172.31.255.0/29', '--gateway=172.31.255.1', '--label=gcreation.role=dev-host-access',
            'gcreation-perf-dev-host-access'])
        identity = self.root / 'host-access-network-id'
        self.assertEqual(identity.read_text(), 'c' * 64)
        self.assertEqual(identity.stat().st_mode & 0o777, 0o600)

    def test_persisted_identity_change_fails_closed(self):
        self.host()['Id'] = 'd' * 64
        self.assert_host_rejected()
        self.assertEqual((self.root / 'host-access-network-id').read_text(), 'c' * 64)

    def test_wrong_subnet_fails_before_container_start(self):
        self.host()['IPAM']['Config'][0]['Subnet'] = '172.30.0.0/29'
        with self.assertRaises(ValueError):
            controller.start_runtime(self.root)
        self.commands.assert_not_called()

    def test_wrong_bridge_gateway_fails_closed(self):
        self.host()['IPAM']['Config'][0]['Gateway'] = '172.31.255.3'
        self.assert_host_rejected()

    def test_wrong_role_labels_and_extra_labels_fail_closed(self):
        for labels in ({}, {'gcreation.role': 'dev-audit'}, {'gcreation.role': 'dev-host-access', 'extra': 'bad'}):
            self.host()['Labels'] = labels
            self.assert_host_rejected()

    def test_name_internal_driver_scope_and_invalid_identity_fail_closed(self):
        original = copy.deepcopy(self.host())
        for update in ({'Name': 'bridge'}, {'Internal': False}, {'Driver': 'overlay'}, {'Scope': 'swarm'}, {'Id': 'invalid'}):
            self.networks[controller.HOST_ACCESS_NETWORK] = dict(original, **update)
            self.assert_host_rejected()

    def test_extra_ipam_ranges_routes_options_or_ipv6_fail_closed(self):
        original = copy.deepcopy(self.host())
        for update in ({'Config': []}, {'Config': original['IPAM']['Config'] + [{'Subnet': '10.0.0.0/8'}]},
                       {'Config': [{'Subnet': '172.31.255.0/29', 'Gateway': '172.31.255.1', 'IPRange': '172.31.255.0/30'}]},
                       {'Config': [{'Subnet': '172.31.255.0/29', 'Gateway': '172.31.255.1', 'AuxiliaryAddresses': {'extra': '172.31.255.3'}}]},
                       {'Driver': 'custom'}, {'Options': {'extra': 'bad'}}, {'extra': 'bad'}):
            self.host()['IPAM'] = dict(original['IPAM'], **update)
            self.assert_host_rejected()
        self.networks[controller.HOST_ACCESS_NETWORK] = dict(original, EnableIPv6=True)
        self.assert_host_rejected()

    def test_unexpected_host_member_including_app_and_proxy_rejected(self):
        for name in ('unrelated', controller.APP, controller.PROXY):
            self.host()['Containers'] = {'f' * 64: {'Name': name}}
            self.assert_host_rejected()

    def test_gateway_exact_address_accepted_on_both_inspections(self):
        controller.ensure_host_access_network(require_members=True)
        controller.ensure_internal_network(require_members=True)
        self.commands.assert_not_called()

    def test_gateway_wrong_ip_prefix_or_ipv6_rejected(self):
        original = copy.deepcopy(self.gateway()['NetworkSettings']['Networks'][controller.HOST_ACCESS_NETWORK])
        for update in ({'IPAddress': '172.31.255.3'}, {'IPAddress': ''}, {'IPPrefixLen': 24}, {'GlobalIPv6Address': 'fd00::2'}):
            self.gateway()['NetworkSettings']['Networks'][controller.HOST_ACCESS_NETWORK] = dict(original, **update)
            self.assert_host_rejected()

    def test_gateway_network_endpoint_id_or_member_address_rejected(self):
        self.gateway()['NetworkSettings']['Networks'][controller.HOST_ACCESS_NETWORK]['NetworkID'] = 'd' * 64
        self.assert_host_rejected()
        self.gateway()['NetworkSettings']['Networks'][controller.HOST_ACCESS_NETWORK]['NetworkID'] = 'c' * 64
        self.host()['Containers'][self.names[controller.GATEWAY]]['IPv4Address'] = '172.31.255.3/29'
        self.assert_host_rejected()

    def test_gateway_egress_default_bridge_host_or_other_network_rejected(self):
        for extra in (controller.EGRESS, 'bridge', 'host', 'unrelated'):
            self.gateway()['NetworkSettings']['Networks'][extra] = {'NetworkID': 'f' * 64}
            self.assert_host_rejected()
            del self.gateway()['NetworkSettings']['Networks'][extra]

    def test_gateway_missing_host_access_is_not_accepted_as_transition(self):
        del self.gateway()['NetworkSettings']['Networks'][controller.HOST_ACCESS_NETWORK]
        with self.assertRaises(ValueError):
            controller.ensure_internal_network()
        self.commands.assert_not_called()

    def test_app_internal_only_no_host_access_or_egress(self):
        controller.ensure_internal_network(require_members=True)
        app = self.containers[self.names[controller.APP]]
        for extra in (controller.HOST_ACCESS_NETWORK, controller.EGRESS, 'bridge', 'host'):
            app['NetworkSettings']['Networks'][extra] = {'NetworkID': 'f' * 64}
            with self.assertRaises(ValueError):
                controller.ensure_internal_network()
            del app['NetworkSettings']['Networks'][extra]

    def test_proxy_internal_plus_egress_only_no_host_access_or_bridge(self):
        controller.ensure_egress_network(require_members=True)
        proxy = self.containers[self.names[controller.PROXY]]
        for extra in (controller.HOST_ACCESS_NETWORK, 'bridge', 'host'):
            proxy['NetworkSettings']['Networks'][extra] = {'NetworkID': 'f' * 64}
            with self.assertRaises(ValueError):
                controller.ensure_egress_network()
            del proxy['NetworkSettings']['Networks'][extra]
        del proxy['NetworkSettings']['Networks'][controller.EGRESS]
        with self.assertRaises(ValueError):
            controller.ensure_internal_network()

    def test_gateway_no_requested_or_effective_published_port(self):
        for host, ports in [({'PortBindings': {'3101/tcp': [{'HostIp': '127.0.0.1', 'HostPort': '3101'}]}}, {}),
                           ({'PublishAllPorts': True}, {}), ({}, {'3101/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '3101'}]}),
                           ({}, {'3101/tcp': False})]:
            self.gateway()['HostConfig'] = host
            self.gateway()['NetworkSettings']['Ports'] = ports
            self.assert_host_rejected()

    def test_strict_post_attachment_requires_all_expected_members(self):
        self.host()['Containers'] = {}
        with self.assertRaises(ValueError):
            controller.ensure_host_access_network(require_members=True)
        self.networks[controller.NETWORK]['Containers'].pop(self.names[controller.APP])
        with self.assertRaises(ValueError):
            controller.ensure_internal_network(require_members=True)
        self.networks[controller.EGRESS]['Containers'] = {}
        with self.assertRaises(ValueError):
            controller.ensure_egress_network(require_members=True)

    def test_runtime_launch_has_no_publish_static_connect_and_strict_order(self):
        order = []
        with mock.patch.object(controller, 'ensure_internal_network', side_effect=lambda **kw: order.append(('internal', kw))), \
                mock.patch.object(controller, 'ensure_egress_network', side_effect=lambda **kw: order.append(('egress', kw))), \
                mock.patch.object(controller, 'ensure_host_access_network', side_effect=lambda **kw: order.append(('host', kw))), \
                mock.patch.object(controller, 'health', side_effect=lambda **kw: order.append(('health', kw))):
            controller.start_runtime(self.root)
        calls = [call[0][0] for call in self.commands.call_args_list]
        gateway = next(args for args in calls if args[:3] == ['docker', 'run', '-d'] and args[args.index('--name') + 1] == controller.GATEWAY)
        self.assertFalse(any(arg == '-p' or arg.startswith(('--publish', '-p=')) for arg in gateway))
        self.assertEqual(gateway[gateway.index('--network') + 1], controller.NETWORK)
        self.assertEqual(gateway[-2:], ['node', '/opt/gcreation-trusted/ops/dev/trusted/gateway.mjs'])
        connect = ['docker', 'network', 'connect', '--ip', '172.31.255.2', controller.HOST_ACCESS_NETWORK, controller.GATEWAY]
        self.assertGreater(calls.index(connect), calls.index(gateway))
        self.assertEqual(order, [('internal', {}), ('egress', {}), ('host', {}),
            ('internal', {'require_members': True}), ('egress', {'require_members': True}),
            ('host', {'require_members': True}), ('health', {'phase': 'readiness', 'attempt': 1})])

    def test_creation_collision_aborts_before_runtime_launch_no_fallback(self):
        with mock.patch.object(controller, 'ensure_internal_network'), mock.patch.object(controller, 'ensure_egress_network'), \
                mock.patch.object(controller, 'docker_json', return_value=None), \
                mock.patch.object(controller, 'command', side_effect=RuntimeError('fixture subnet collision')) as command:
            with self.assertRaisesRegex(RuntimeError, 'subnet collision'):
                controller.start_runtime(self.root)
        self.assertEqual(command.call_count, 1)
        self.assertEqual(command.call_args[0][0][1:3], ['network', 'create'])
        self.assertIn('--subnet=172.31.255.0/29', command.call_args[0][0])
        self.assertNotIn('allow_failure', command.call_args[1])

    def test_gateway_member_trusted_image_label_and_name_fail_closed(self):
        original = copy.deepcopy(self.gateway())
        for update in ({'Image': 'mutable-tag'}, {'Name': '/unrelated'}, {'Config': {'Labels': {'gcreation.role': 'app'}}}):
            self.containers[self.names[controller.GATEWAY]] = dict(original, **update)
            self.assert_host_rejected()

    def test_builder_remains_offline_no_extra_network_or_secret(self):
        args = controller.build_command(self.root / 'source', self.root / 'output')
        self.assertIn('--network=none', args)
        self.assertNotIn(controller.HOST_ACCESS_NETWORK, args)
        self.assertNotIn('--env-file', ' '.join(args))
        self.assertIn('--user', args); self.assertIn('10001:10001', args)

    def test_rollback_reuses_same_start_runtime_function(self):
        tree = ast.parse((ROOT / 'ops/dev/deploy_controller.py').read_text())
        deploy = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'deploy')
        calls = [n for n in ast.walk(deploy) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'start_runtime']
        self.assertEqual(len(calls), 2)
        self.assertIsInstance(calls[0].args[0], ast.Name)
        self.assertIsInstance(calls[1].args[0], ast.Call)

    def test_no_dependencies_image_gateway_or_extra_environment_change(self):
        for file, expected in self.frozen.items():
            self.assertEqual(hashlib.sha256((ROOT / file).read_bytes()).digest(), hashlib.sha256(expected).digest(), file)
        source = (ROOT / 'ops/dev/deploy_controller.py').read_text()
        self.assertNotIn('http://127.0.0.1:3101', source)
        self.assertNotIn('HOST_ACCESS_NETWORK=', source)
        self.assertNotIn('os.environ', source)


if __name__ == '__main__':
    unittest.main()
