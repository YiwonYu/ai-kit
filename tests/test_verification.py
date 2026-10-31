import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/verify_pipeline.py'


class VerificationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / 'reports'
        self.config_path = self.root / 'verification.json'

    def check(self, code='pass', **fields):
        return dict(id='expected-output', name='독립적인 기대값 확인', category='unit',
                    oracle='fixture의 기대값을 assert하고 그 결과를 exit code로 전달한다.',
                    command=['{python}', '-c', code], timeout=5, **fields)

    def config(self, checks):
        return {'scope':'temporary fixture only', 'required_categories':[],
                'requirements':[{'id':'fixture requirement','checks':[checks[0]['id']]}], 'checks':checks}

    def run_suite(self, config):
        self.config_path.write_text(json.dumps(config))
        proc = subprocess.run([sys.executable, str(SCRIPT), '--config', str(self.config_path),
                               '--root', str(self.root), '--output-dir', str(self.output)],
                              capture_output=True, text=True, timeout=20)
        reports = sorted(self.output.glob('*/report.json'), key=lambda x:x.stat().st_mtime_ns)
        return proc, json.loads(reports[-1].read_text()) if reports else None

    def test_pass_report_has_evidence_and_frozen_config(self):
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
        proc, report = self.run_suite(self.config([self.check('assert 2+2==5')]))
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(report['checks'][0]['status'], 'failed')

    def test_pending_requirement_is_blocked(self):
        check = self.check(pending=True)
        del check['command']
        proc, report = self.run_suite(self.config([check]))
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(report['checks'][0]['status'], 'blocked')

    def test_missing_requirement_check_is_invalid(self):
        config = self.config([self.check()])
        config['requirements'][0]['checks']=['nonexistent']
        proc, report = self.run_suite(config)
        self.assertEqual(proc.returncode, 2)
        self.assertIsNone(report)

    def test_required_category_cannot_be_omitted(self):
        config = self.config([self.check()])
        config['required_categories']=['e2e']
        proc, _ = self.run_suite(config)
        self.assertEqual(proc.returncode, 2)

    def test_negative_exit_and_timeout_are_distinct(self):
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
        check={'id':'structure','name':'구조 계약','category':'structure','oracle':'service.py가 실제 파일이어야 한다.',
               'paths':[{'path':'service.py','kind':'file'}]}
        proc, report = self.run_suite(self.config([check]))
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(report['checks'][0]['status'], 'failed')
        (self.root/'service.py').write_text('')
        proc, _ = self.run_suite(self.config([check]))
        self.assertEqual(proc.returncode, 0)

    def test_structure_cannot_escape_project(self):
        check={'id':'structure','name':'구조 계약','category':'structure','oracle':'프로젝트 내부 경로만 허용한다.',
               'paths':[{'path':'../outside.py','kind':'file'}]}
        proc, _ = self.run_suite(self.config([check]))
        self.assertEqual(proc.returncode, 2)

    def test_empty_check_list_is_not_pass(self):
        proc, _ = self.run_suite(self.config_path_config_empty())
        self.assertEqual(proc.returncode, 2)

    @staticmethod
    def config_path_config_empty():
        return {'scope':'empty', 'checks':[], 'requirements':[]}


if __name__ == '__main__':
    unittest.main()
