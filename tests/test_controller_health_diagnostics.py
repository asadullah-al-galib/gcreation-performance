"""Stage-1 journal regressions: mocked predicates only, no runtime or host actions."""
import ast
from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import unittest
from unittest import mock
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('diagnostic_controller', str(ROOT / 'ops/dev/deploy_controller.py'))
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)
PREFIX = 'GCREATION_HEALTH_DIAG '
SECRET = 'SENTINEL_SECRET_DO_NOT_EMIT'
IDENTITY = {'service': 'gcreation-performance', 'environment': 'development'}
REASONS = {'OK', 'HTTP_ERROR', 'TIMEOUT', 'URL_ERROR', 'INVALID_JSON',
           'IDENTITY_MISMATCH', 'NON_200_STATUS', 'NETWORK_OR_OS_ERROR', 'UNEXPECTED_EXCEPTION'}


class Response(io.BytesIO):
    def __init__(self, status=200, body=None):
        super().__init__(json.dumps(IDENTITY if body is None else body).encode())
        self.status = status


class HealthDiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.assertNotEqual(os.geteuid(), 0, 'Ordinary-user unit tests only')
        # A missed mock must fail before any socket or trusted subprocess can run.
        sockets = mock.patch.object(socket, 'socket', side_effect=AssertionError('Network forbidden'))
        processes = mock.patch.object(controller.subprocess, 'run', side_effect=AssertionError('Host execution forbidden'))
        sockets.start(); processes.start()
        self.addCleanup(sockets.stop); self.addCleanup(processes.stop)

    def events(self, output):
        rows = []
        for line in output.getvalue().splitlines():
            self.assertTrue(line.startswith(PREFIX))
            self.assertLessEqual(len((line + '\n').encode()), 512)
            row = json.loads(line[len(PREFIX):])
            self.assertEqual(set(row), {'event', 'timestamp_utc', 'phase', 'attempt', 'predicate',
                                       'result', 'http_status', 'exception_class', 'reason'})
            self.assertEqual(row['event'], 'gcreation_health_diagnostic')
            self.assertRegex(row['timestamp_utc'], r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
            self.assertIn(row['reason'], REASONS)
            if row['exception_class'] is not None:
                self.assertLessEqual(len(row['exception_class']), 64)
            status = row['http_status']
            self.assertTrue(status is None or (type(status) is int and 100 <= status <= 599))
            rows.append(row)
        self.assertNotIn(SECRET, output.getvalue())
        return rows

    def check(self, replies, expected_error=None, **context):
        output = io.StringIO()
        opener = mock.Mock()
        opener.open.side_effect = replies
        with redirect_stdout(output), mock.patch.object(controller.urllib.request, 'build_opener', return_value=opener) as build:
            if expected_error is None:
                self.assertIsNone(controller.health(**context))
            else:
                with self.assertRaises(type(expected_error)) as caught:
                    controller.health(**context)
                # Transport/context errors must be the same object, not a replacement.
                self.assertIs(caught.exception, expected_error)
        self.assertIsInstance(build.call_args[0][0], controller.NoRedirect)
        calls = opener.open.call_args_list
        self.assertEqual(calls[0], mock.call('http://127.0.0.1:3101/health', timeout=10))
        if len(calls) > 1:
            self.assertEqual(calls[1], mock.call('https://dev.gcreation.agency/', timeout=15))
        return self.events(output), opener, output.getvalue()

    def test_localhost_connection_failure_never_reaches_homepage(self):
        error = ConnectionRefusedError(111, SECRET)
        rows, opener, _ = self.check([error], error, phase='readiness', attempt=1)
        self.assertEqual(opener.open.call_count, 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual((rows[0]['predicate'], rows[0]['result'], rows[0]['reason']),
                         ('LOCALHOST_ENGINE_HEALTH', 'FAIL', 'NETWORK_OR_OS_ERROR'))

    def test_identity_service_and_environment_failures_preserve_runtime_error(self):
        for body in ({'service': SECRET, 'environment': 'development'},
                     {'service': 'gcreation-performance', 'environment': SECRET}, {}):
            with self.subTest(body=body):
                output = io.StringIO(); opener = mock.Mock()
                opener.open.return_value = Response(body=body)
                with redirect_stdout(output), mock.patch.object(controller.urllib.request, 'build_opener', return_value=opener):
                    with self.assertRaisesRegex(RuntimeError, '^Internal health failed$'):
                        controller.health(phase='readiness', attempt=2)
                row, = self.events(output)
                self.assertEqual((row['result'], row['http_status'], row['reason'], row['exception_class']),
                                 ('FAIL', 200, 'IDENTITY_MISMATCH', 'RuntimeError'))
                self.assertEqual(opener.open.call_count, 1)

    def test_localhost_non_200_preserves_runtime_error(self):
        output = io.StringIO(); opener = mock.Mock()
        opener.open.return_value = Response(status=503)
        with redirect_stdout(output), mock.patch.object(controller.urllib.request, 'build_opener', return_value=opener):
            with self.assertRaisesRegex(RuntimeError, '^Internal health failed$'):
                controller.health()
        row, = self.events(output)
        self.assertEqual((row['predicate'], row['http_status'], row['reason']),
                         ('LOCALHOST_ENGINE_HEALTH', 503, 'NON_200_STATUS'))
        self.assertEqual(opener.open.call_count, 1)

    def test_localhost_pass_then_homepage_non_200(self):
        output = io.StringIO(); opener = mock.Mock()
        opener.open.side_effect = [Response(), Response(status=503)]
        with redirect_stdout(output), mock.patch.object(controller.urllib.request, 'build_opener', return_value=opener):
            with self.assertRaisesRegex(RuntimeError, '^DEV website health failed$'):
                controller.health()
        rows = self.events(output)
        self.assertEqual([(r['predicate'], r['result'], r['http_status'], r['reason']) for r in rows],
                         [('LOCALHOST_ENGINE_HEALTH', 'PASS', 200, 'OK'),
                          ('DEV_HOMEPAGE_HEALTH', 'FAIL', 503, 'NON_200_STATUS')])

    def test_both_pass_retains_order_timeouts_and_returns_normally(self):
        rows, opener, _ = self.check([Response(), Response(body=SECRET)], phase='readiness', attempt=3)
        self.assertEqual(opener.open.call_count, 2)
        self.assertEqual([r['predicate'] for r in rows], ['LOCALHOST_ENGINE_HEALTH', 'DEV_HOMEPAGE_HEALTH'])
        self.assertEqual([r['result'] for r in rows], ['PASS', 'PASS'])
        self.assertEqual([r['http_status'] for r in rows], [200, 200])
        self.assertTrue(all(r['phase'] == 'readiness' and r['attempt'] == 3 for r in rows))

    def test_redirect_handlers_still_raise_without_following(self):
        # Exercise urllib's real redirect dispatch with DATA; no socket is opened.
        for code in (301, 302, 303, 307, 308):
            with self.subTest(code=code):
                opener = urllib.request.build_opener(controller.NoRedirect())
                request = urllib.request.Request('https://dev.gcreation.agency/')
                headers = {'Location': 'https://example.invalid/?token=' + SECRET, 'Cookie': SECRET}
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    opener.error('http', request, io.BytesIO(SECRET.encode()), code, SECRET, headers)
                error = caught.exception
                rows, _, _ = self.check([Response(), error], error)
                self.assertEqual((rows[-1]['predicate'], rows[-1]['result'], rows[-1]['http_status'], rows[-1]['reason']),
                                 ('DEV_HOMEPAGE_HEALTH', 'FAIL', code, 'HTTP_ERROR'))

    def test_timeout_and_url_errors_use_fixed_reasons_and_original_exceptions(self):
        for error, reason in ((TimeoutError(SECRET), 'TIMEOUT'), (socket.timeout(SECRET), 'TIMEOUT'),
                              (urllib.error.URLError(SECRET), 'URL_ERROR'),
                              (urllib.error.URLError(socket.timeout(SECRET)), 'TIMEOUT')):
            for local in (True, False):
                with self.subTest(error_type=type(error).__name__, local=local):
                    rows, _, _ = self.check([error] if local else [Response(), error], error)
                    self.assertEqual(rows[-1]['reason'], reason)
                    self.assertEqual(rows[-1]['result'], 'FAIL')
                    self.assertEqual(len(rows), 1 if local else 2)

    def test_invalid_json_preserves_parser_exception_without_body(self):
        response = Response(); response.seek(0); response.truncate(); response.write(SECRET.encode()); response.seek(0)
        output = io.StringIO(); opener = mock.Mock(); opener.open.return_value = response
        with redirect_stdout(output), mock.patch.object(controller.urllib.request, 'build_opener', return_value=opener):
            with self.assertRaises(json.JSONDecodeError):
                controller.health()
        row, = self.events(output)
        self.assertEqual((row['result'], row['reason'], row['exception_class']), ('FAIL', 'INVALID_JSON', 'JSONDecodeError'))
        self.assertEqual(opener.open.call_count, 1)

    def test_non_mapping_json_preserves_attribute_error(self):
        output = io.StringIO(); opener = mock.Mock(); opener.open.return_value = Response(body=[SECRET])
        with redirect_stdout(output), mock.patch.object(controller.urllib.request, 'build_opener', return_value=opener):
            with self.assertRaises(AttributeError):
                controller.health()
        row, = self.events(output)
        self.assertEqual((row['http_status'], row['reason'], row['exception_class']),
                         (200, 'UNEXPECTED_EXCEPTION', 'AttributeError'))

    def test_context_exit_failure_is_not_logged_as_pass(self):
        error = OSError(SECRET)
        response = mock.Mock(status=200)
        response.__enter__ = mock.Mock(return_value=Response())
        response.__exit__ = mock.Mock(side_effect=error)
        rows, opener, _ = self.check([response], error)
        self.assertEqual((rows[0]['result'], rows[0]['reason']), ('FAIL', 'NETWORK_OR_OS_ERROR'))
        self.assertEqual(opener.open.call_count, 1)

    def test_diagnostic_output_failure_does_not_break_health_success(self):
        opener = mock.Mock(); opener.open.side_effect = [Response(), Response()]
        with mock.patch.object(controller.urllib.request, 'build_opener', return_value=opener), \
                mock.patch('builtins.print', side_effect=OSError(SECRET)):
            self.assertIsNone(controller.health())
        self.assertEqual(opener.open.call_count, 2)

    def test_diagnostic_output_failure_does_not_replace_health_failure(self):
        error = urllib.error.URLError(SECRET)
        opener = mock.Mock(); opener.open.side_effect = error
        with mock.patch.object(controller.urllib.request, 'build_opener', return_value=opener), \
                mock.patch('builtins.print', side_effect=OSError(SECRET)):
            with self.assertRaises(urllib.error.URLError) as caught:
                controller.health()
        self.assertIs(caught.exception, error)

    def test_diagnostic_serialization_or_clock_failure_cannot_break_health(self):
        for target in ('json.dumps', 'time.gmtime'):
            for failure in (False, True):
                with self.subTest(target=target, failure=failure):
                    opener = mock.Mock()
                    error = OSError(SECRET)
                    opener.open.side_effect = [error] if failure else [Response(), Response()]
                    module_name, name = target.split('.')
                    with mock.patch.object(controller.urllib.request, 'build_opener', return_value=opener), \
                            mock.patch.object(getattr(controller, module_name), name, side_effect=ValueError(SECRET)):
                        if failure:
                            with self.assertRaises(OSError) as caught:
                                controller.health()
                            self.assertIs(caught.exception, error)
                        else:
                            self.assertIsNone(controller.health())

    def run_readiness(self, replies):
        # Only health() and the retry loop are real. Every Docker/network/image operation is mocked.
        output = io.StringIO(); opener = mock.Mock(); opener.open.side_effect = replies
        with redirect_stdout(output), mock.patch.object(controller.urllib.request, 'build_opener', return_value=opener), \
                mock.patch.object(controller, 'command'), \
                mock.patch.object(controller, 'ensure_internal_network'), \
                mock.patch.object(controller, 'ensure_egress_network'), \
                mock.patch.object(controller, 'runtime_image', return_value='sha256:' + 'e' * 64), \
                mock.patch.object(controller.time, 'sleep') as sleep:
            try:
                controller.start_runtime(Path('/fixture/release'))
                error = None
            except RuntimeError as observed:
                error = observed
        return self.events(output), opener, sleep, error

    def test_readiness_30_attempts_2_second_sleeps_and_deadline_unchanged(self):
        error = ConnectionRefusedError(111, SECRET)
        rows, opener, sleep, terminal = self.run_readiness([error] * 30)
        self.assertIsInstance(terminal, RuntimeError)
        self.assertEqual(str(terminal), 'Runtime readiness deadline exceeded')
        self.assertEqual(opener.open.call_count, 30)
        self.assertEqual(sleep.call_args_list, [mock.call(2)] * 30)
        self.assertEqual([r['attempt'] for r in rows], list(range(1, 31)))
        self.assertTrue(all(r['phase'] == 'readiness' and r['predicate'] == 'LOCALHOST_ENGINE_HEALTH' and r['result'] == 'FAIL' for r in rows))

    def test_readiness_event_maximum_is_60(self):
        error = urllib.error.HTTPError('https://dev.gcreation.agency/?token=' + SECRET, 503, SECRET, {'Cookie': SECRET}, io.BytesIO(SECRET.encode()))
        replies = [item for _ in range(30) for item in (Response(), error)]
        rows, _, sleep, terminal = self.run_readiness(replies)
        self.assertIsInstance(terminal, RuntimeError)
        self.assertEqual(len(rows), 60)
        self.assertEqual([r['attempt'] for r in rows], [number for number in range(1, 31) for _ in range(2)])
        self.assertEqual(sleep.call_args_list, [mock.call(2)] * 30)

    def test_readiness_success_stops_without_extra_sleep_or_retry(self):
        rows, opener, sleep, terminal = self.run_readiness([OSError(SECRET), Response(), Response()])
        self.assertIsNone(terminal)
        self.assertEqual([r['attempt'] for r in rows], [1, 2, 2])
        self.assertEqual(opener.open.call_count, 3)
        self.assertEqual(sleep.call_args_list, [mock.call(2)])

    def test_final_health_has_null_attempt_and_same_predicates(self):
        rows, _, _ = self.check([Response(), Response()])
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r['phase'] == 'final-health' and r['attempt'] is None for r in rows))
        tree = ast.parse((ROOT / 'ops/dev/deploy_controller.py').read_text())
        deploy = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'deploy')
        calls = [n for n in ast.walk(deploy) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'health']
        self.assertEqual(len(calls), 1)
        self.assertFalse(calls[0].args or calls[0].keywords)

    def test_information_disclosure_sentinels_never_escape(self):
        error_type = type(SECRET + '_Exception', (Exception,), {})
        errors = [urllib.error.HTTPError('https://example.invalid/?token=' + SECRET, 503, SECRET,
                                        {'Authorization': SECRET, 'Cookie': SECRET}, io.BytesIO(SECRET.encode())),
                  urllib.error.URLError(SECRET), error_type(SECRET)]
        with mock.patch.dict(os.environ, {'ENGINE_SECRET': SECRET, 'AUTHORIZATION': SECRET, 'COOKIE': SECRET}):
            for error in errors:
                with self.subTest(error_type=type(error).__name__):
                    rows, _, text = self.check([Response(body=dict(IDENTITY, extra=SECRET)), error], error)
                    for forbidden in (SECRET, 'Authorization', 'Cookie', 'headers', '?token=', 'ENGINE_SECRET', 'Traceback'):
                        self.assertNotIn(forbidden, text)
                    self.assertIn(rows[-1]['exception_class'], ('HTTPError', 'URLError', 'Exception'))
                    self.assertNotIn('service', rows[0])
                    self.assertNotIn('environment', rows[0])

    def test_status_must_be_plain_integer_100_to_599(self):
        for status in (True, False, 99, 600, '200', SECRET, None, 200.0, 200, 599):
            with self.subTest(status=status):
                output = io.StringIO()
                with redirect_stdout(output):
                    controller.emit_health_diagnostic('readiness', 1, 'LOCALHOST_ENGINE_HEALTH', 'FAIL', status,
                                                      RuntimeError(SECRET), 'NON_200_STATUS')
                row, = self.events(output)
                self.assertEqual(row['http_status'], status if type(status) is int and 100 <= status <= 599 else None)

    def test_unknown_reason_or_invalid_phase_attempt_predicate_is_not_emitted(self):
        for kwargs in ({'reason': SECRET}, {'phase': SECRET}, {'phase': 'readiness', 'attempt': True},
                       {'phase': 'readiness', 'attempt': 0}, {'phase': 'readiness', 'attempt': 31},
                       {'phase': 'final-health', 'attempt': 1}, {'predicate': SECRET}, {'result': SECRET}):
            args = dict(phase='final-health', attempt=None, predicate='DEV_HOMEPAGE_HEALTH', result='PASS')
            args.update(kwargs)
            output = io.StringIO()
            with redirect_stdout(output):
                controller.emit_health_diagnostic(**args)
            self.assertEqual(output.getvalue(), '')

    def test_exception_formatters_are_never_used(self):
        class OpaqueError(Exception):
            def __str__(self):
                raise AssertionError('Exception stringification forbidden')
            def __repr__(self):
                raise AssertionError('Exception repr forbidden')
        error = OpaqueError()
        rows, _, _ = self.check([error], error)
        self.assertEqual((rows[0]['exception_class'], rows[0]['reason']), ('Exception', 'UNEXPECTED_EXCEPTION'))

    def test_emitter_performs_only_fixed_serialization_timestamp_and_stdout(self):
        tree = ast.parse((ROOT / 'ops/dev/deploy_controller.py').read_text())
        helper = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'emit_health_diagnostic')
        names = set()
        for node in ast.walk(helper):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    names.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    self.assertIsInstance(node.func.value, ast.Name)
                    names.add(node.func.value.id + '.' + node.func.attr)
        self.assertEqual(names, {'type', 'isinstance', 'time.strftime', 'time.gmtime', 'json.dumps', 'len', 'print'})
        self.assertNotIn('fromisoformat', (ROOT / 'ops/dev/deploy_controller.py').read_text())


if __name__ == '__main__':
    unittest.main()
