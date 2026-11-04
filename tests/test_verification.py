import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/verify_pipeline.py'


class VerificationTest(unittest.TestCase):
    def setUp(self):
        '''Create isolated configuration and report paths.

        Args:
            self: VerificationTest instance.
        Returns:
            None. Registers temporary-directory cleanup.
        '''
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / 'reports'
        self.config_path = self.root / 'verification.json'

    def check(self, code='pass', **fields):
        '''Build an independently asserted test declaration.

        Args:
            self: VerificationTest instance.
            code: Python assertion snippet.
            fields: Additional check fields.
        Returns:
            Check configuration mapping.
        '''
        return dict(id='expected-output', name='Independent expected values', category='unit',
                    oracle='Assert expected fixture values and return the test exit code.',
                    command=['{python}', '-c', code], timeout=5, **fields)

    def config(self, checks):
        '''Map a fixture requirement to its check.

        Args:
            self: VerificationTest instance.
            checks: Nonempty list of fixture checks.
        Returns:
            Suite configuration for the isolated fixture.
        '''
        return {'scope':'temporary fixture only', 'required_categories':[],
                'requirements':[{'id':'fixture requirement','checks':[checks[0]['id']]}], 'checks':checks}

    def run_suite(self, config):
        '''Execute a verification fixture through the CLI.

        Args:
            self: VerificationTest instance.
            config: Suite configuration to serialize and execute.
        Returns:
            Tuple of CLI result and latest report, or None for rejected configurations.
        '''
        self.config_path.write_text(json.dumps(config))
        proc = subprocess.run([sys.executable, str(SCRIPT), '--config', str(self.config_path),
                               '--root', str(self.root), '--output-dir', str(self.output)],
                              capture_output=True, text=True, timeout=20)
        reports = sorted(self.output.glob('*/report.json'), key=lambda x:x.stat().st_mtime_ns)
        return proc, json.loads(reports[-1].read_text()) if reports else None

    def test_pass_report_has_evidence_and_frozen_config(self):
        '''Pass report has evidence and frozen config.

        Args:
            self: Isolated test fixture instance.
        Returns:
            None. Assertions check the observed behavior.
        '''
        config = self.config([self.check("print('fixture checked');assert 2+2==4")])
        proc, report = self.run_suite(config)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(report['status'], 'passed')
        self.assertIn('fixture checked', Path(report['checks'][0]['stdout']).read_text())
        folder = next(self.output.iterdir())
        self.assertEqual(json.loads((folder/'config.json').read_text()), config)
        self.assertTrue((folder/'report.md').is_file())
        self.assertIn('git', report)

    def test_actual_test_failure_fails_gate(self):
        '''Actual test failure fails gate.

        Args:
            self: Isolated test fixture instance.
        Returns:
            None. Assertions check the observed behavior.
        '''
        proc, report = self.run_suite(self.config([self.check('assert 2+2==5')]))
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(report['checks'][0]['status'], 'failed')

    def test_pending_requirement_is_blocked(self):
        '''Pending requirement is blocked.

        Args:
            self: Isolated test fixture instance.
        Returns:
            None. Assertions check the observed behavior.
        '''
        check = self.check(pending=True)
        del check['command']
        proc, report = self.run_suite(self.config([check]))
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(report['checks'][0]['status'], 'blocked')

    def test_missing_requirement_check_is_invalid(self):
        '''Missing requirement check is invalid.

        Args:
            self: Isolated test fixture instance.
        Returns:
            None. Assertions check the observed behavior.
        '''
        config = self.config([self.check()])
        config['requirements'][0]['checks']=['nonexistent']
        proc, report = self.run_suite(config)
        self.assertEqual(proc.returncode, 2)
        self.assertIsNone(report)

    def test_required_category_cannot_be_omitted(self):
        '''Required category cannot be omitted.

        Args:
            self: Isolated test fixture instance.
        Returns:
            None. Assertions check the observed behavior.
        '''
        config = self.config([self.check()])
        config['required_categories']=['e2e']
        proc, _ = self.run_suite(config)
        self.assertEqual(proc.returncode, 2)

    def test_negative_exit_and_timeout_are_distinct(self):
        '''Negative exit and timeout are distinct.

        Args:
            self: Isolated test fixture instance.
        Returns:
            None. Assertions check the observed behavior.
        '''
        check = self.check('import sys;sys.exit(7)', expected_exit=7)
        proc, report = self.run_suite(self.config([check]))
        self.assertEqual(proc.returncode, 0)
        first = Path(report['checks'][0]['stdout'])
        check['command']=['{python}','-c','import time;time.sleep(10)']
        check['timeout']=.1
        proc, report = self.run_suite(self.config([check]))
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(report['checks'][0]['execution_status'], 'timeout')
        self.assertTrue(first.exists(), 'previous evidence must survive')
        self.assertEqual(len(list(self.output.glob('*/report.json'))), 2)

    def test_file_structure_failure_and_success(self):
        '''File structure failure and success.

        Args:
            self: Isolated test fixture instance.
        Returns:
            None. Assertions check the observed behavior.
        '''
        check={'id':'structure','name':'Structure contract','category':'structure','oracle':'service.py must be a file.',
               'paths':[{'path':'service.py','kind':'file'}]}
        proc, report = self.run_suite(self.config([check]))
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(report['checks'][0]['status'], 'failed')
        (self.root/'service.py').write_text('')
        proc, _ = self.run_suite(self.config([check]))
        self.assertEqual(proc.returncode, 0)

    def test_structure_cannot_escape_project(self):
        '''Structure cannot escape project.

        Args:
            self: Isolated test fixture instance.
        Returns:
            None. Assertions check the observed behavior.
        '''
        check={'id':'structure','name':'Structure contract','category':'structure','oracle':'Only paths within the project are allowed.',
               'paths':[{'path':'../outside.py','kind':'file'}]}
        proc, _ = self.run_suite(self.config([check]))
        self.assertEqual(proc.returncode, 2)

    def test_empty_check_list_is_not_pass(self):
        '''Empty check list is not pass.

        Args:
            self: Isolated test fixture instance.
        Returns:
            None. Assertions check the observed behavior.
        '''
        proc, _ = self.run_suite(self.config_path_config_empty())
        self.assertEqual(proc.returncode, 2)

    @staticmethod
    def config_path_config_empty():
        '''Build an invalid empty-suite fixture.

        Args:
            None. Uses enclosing state or CLI arguments.
        Returns:
            Configuration with no checks or requirements.
        '''
        return {'scope':'empty', 'checks':[], 'requirements':[]}


if __name__ == '__main__':
    unittest.main()
