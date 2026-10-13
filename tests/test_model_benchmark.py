import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import benchmark_models as benchmark


class BenchmarkGuards(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.output = Path(self.tmp.name)
        self.case = json.loads((ROOT / 'tests/fixtures/model-benchmark.json').read_text())['cases'][0]

    def test_dry_run_records_preparation_not_model_success(self):
        result = benchmark.evaluate(self.output, 'gpt-5.6-luna', self.case, 1, False)
        self.assertEqual(result['status'], 'PREPARED_NOT_EXECUTED')
        self.assertNotIn('passed', result)
        self.assertIsNone(result['usage'])
        model_input = json.loads(next(self.output.glob('*/input.json')).read_text())
        self.assertNotIn('expected', model_input)

    def test_backend_failure_has_no_score_or_checkpoint_success(self):
        failure = subprocess.CompletedProcess([], 1, '', 'backend unavailable')
        with patch.object(benchmark.subprocess, 'run', return_value=failure):
            result = benchmark.evaluate(self.output, 'gpt-5.6-luna', self.case, 1, True)
        self.assertEqual(result['status'], 'BACKEND_FAILED_NO_MODEL_RESULT')
        self.assertNotIn('passed', result)
        self.assertNotIn('checkpoint', result)

    def test_timeout_is_not_model_or_google_timeout_success(self):
        with patch.object(benchmark.subprocess, 'run', side_effect=subprocess.TimeoutExpired([], 90)):
            result = benchmark.evaluate(self.output, 'gpt-5.6-luna', self.case, 1, True)
        self.assertEqual(result['status'], 'RUNNER_TIMEOUT_NO_CONFIRMED_RESULT')
        self.assertNotIn('passed', result)

    def test_invalid_response_cannot_receive_a_score(self):
        success = subprocess.CompletedProcess([], 0, '{}\n', '')
        with patch.object(benchmark.subprocess, 'run', return_value=success):
            result = benchmark.evaluate(self.output, 'gpt-5.6-luna', self.case, 1, True)
        self.assertEqual(result['status'], 'RESPONSE_OR_BOUNDARY_REJECTED')
        self.assertNotIn('passed', result)

    def test_duplicate_execution_never_overwrites_evidence(self):
        benchmark.evaluate(self.output, 'gpt-5.6-luna', self.case, 1, False)
        with self.assertRaises(FileExistsError):
            benchmark.evaluate(self.output, 'gpt-5.6-luna', self.case, 1, False)

    def test_fresh_invocation_does_not_resume_or_fork(self):
        cmd = benchmark.command('gpt-5.6-luna', self.output, self.output/'schema', self.output/'response')
        self.assertIn('--ephemeral', cmd)
        self.assertIn('--ignore-user-config', cmd)
        self.assertNotIn('resume', cmd)
        self.assertNotIn('fork', cmd)
        self.assertIn('memories', cmd)
        self.assertIn('multi_agent', cmd)


if __name__ == '__main__':
    unittest.main()
