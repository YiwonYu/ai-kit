import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / 'scripts/run_experiment.py'


class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / 'runs'

    def run_code(self, code, timeout=5):
        result = subprocess.run([sys.executable, str(RUNNER), '--output-dir', str(self.out),
                                 '--seed', '17', '--timeout', str(timeout), '--',
                                 sys.executable, '-c', code], capture_output=True, text=True, timeout=15)
        dirs = sorted(self.out.iterdir(), key=lambda x: x.stat().st_mtime_ns)
        folder = dirs[-1]
        return result, folder, json.loads((folder / 'metadata.json').read_text())

    def test_success_logs_seed_and_metadata(self):
        p, folder, m = self.run_code("import os,sys;print(os.environ['HARNESS_SEED']);print('err',file=sys.stderr)")
        self.assertEqual(p.returncode, 0)
        self.assertEqual(m['status'], 'success')
        self.assertEqual(m['returncode'], 0)
        self.assertEqual((folder / 'stdout.log').read_text().strip(), '17')
        self.assertEqual((folder / 'stderr.log').read_text().strip(), 'err')
        self.assertIn('ended_at', m)

    def test_failure_preserves_previous_run(self):
        _, first, _ = self.run_code("print('saved')")
        p, folder, m = self.run_code('import sys;sys.exit(7)')
        self.assertEqual(p.returncode, 1)
        self.assertEqual(m['status'], 'failed')
        self.assertEqual(m['returncode'], 7)
        self.assertNotEqual(first, folder)
        self.assertEqual((first / 'stdout.log').read_text().strip(), 'saved')

    def test_timeout_keeps_partial_log(self):
        p, folder, m = self.run_code("import time;print('started',flush=True);time.sleep(10)", .4)
        self.assertEqual(p.returncode, 124)
        self.assertEqual(m['status'], 'timeout')
        self.assertIn('started', (folder / 'stdout.log').read_text())

    def test_missing_executable(self):
        p = subprocess.run([sys.executable, str(RUNNER), '--output-dir', str(self.out),
                            '--timeout', '2', '--', '/nonexistent/ai-kit-command'], capture_output=True)
        m = json.loads(next(self.out.glob('*/metadata.json')).read_text())
        self.assertEqual(p.returncode, 2)
        self.assertEqual(m['status'], 'launch_error')
        self.assertIsNone(m['returncode'])

    def test_rejects_invalid_timeout(self):
        for value in ['0', '-1', 'nan', 'inf']:
            with self.subTest(value=value):
                p = subprocess.run([sys.executable, str(RUNNER), '--timeout', value,
                                    '--', sys.executable, '-c', 'pass'], capture_output=True)
                self.assertEqual(p.returncode, 2)

    @unittest.skipUnless(os.name == 'posix', 'POSIX process groups')
    def test_timeout_stops_child_group(self):
        marker = Path(self.tmp.name) / 'child-finished'
        child = f"import time;from pathlib import Path;time.sleep(1.2);Path({str(marker)!r}).write_text('bad')"
        code = f"import subprocess,sys,time;subprocess.Popen([sys.executable,'-c',{child!r}]);time.sleep(10)"
        p, _, _ = self.run_code(code, .3)
        self.assertEqual(p.returncode, 124)
        import time
        time.sleep(1.3)
        self.assertFalse(marker.exists())


if __name__ == '__main__':
    unittest.main()
