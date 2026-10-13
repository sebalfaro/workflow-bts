import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       'skills/bts-orquestador/scripts'))
from context_runtime import ContextError, ContextRuntime, digest
from model_routing import select_route


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.runtime = ContextRuntime(self.tmp.name, 'run-test')
        self.runtime.select_provider('provider-A')
        self.key = self.runtime.cache_extraction(b'fictional source A',
                                                  {'literal': 'EXCLUSIVE_A_MARKER'})

    def open_a(self):
        self.runtime.grant('context-A', 'doc-A', self.key)
        return self.runtime.open_context('context-A', ['A', 'B', '01', 'A', 'F', 'X'], 'rules')

    def response(self, payload):
        return dict(run_id=payload['run_id'], row_context_id=payload['row_context_id'],
                    provider_scope=payload['provider_scope'], input_sha256=digest(payload),
                    document_ids=[d['document_id'] for d in payload['documents']])

    def test_same_provider_next_worker_has_no_prior_document(self):
        a = self.open_a()
        self.runtime.checkpoint_and_close(self.response(a))
        b = self.runtime.open_context('context-B', ['A', 'B', '01', 'A', 'F', 'Y'], 'rules')
        self.assertNotIn('EXCLUSIVE_A_MARKER', json.dumps(b))
        self.assertEqual(b['documents'], [])  # repeated ID does not transfer association

    def test_provider_switch_invalidates_candidate_grants_but_keeps_neutral_cache(self):
        self.runtime.grant('context-B', 'doc-A', self.key)
        self.runtime.select_provider('provider-B')
        b = self.runtime.open_context('context-B', ['A', 'B', '01', 'B', 'F', 'Y'], 'rules')
        self.assertEqual(b['documents'], [])
        self.assertIn(self.key, self.runtime.cache)

    def test_explicit_collective_document_grant_is_required_for_reuse(self):
        a = self.open_a()
        self.runtime.checkpoint_and_close(self.response(a))
        self.runtime.grant('context-B', 'doc-A', self.key)
        b = self.runtime.open_context('context-B', ['A', 'B', '02', 'A', 'F', 'Y'], 'rules')
        self.assertEqual(b['documents'][0]['document_id'], 'doc-A')

    def test_foreign_result_context_and_document_are_rejected(self):
        a = self.open_a()
        for field, value in [('row_context_id', 'context-B'), ('provider_scope', 'provider-B'),
                             ('run_id', 'other-run'), ('input_sha256', 'wrong'),
                             ('document_ids', ['doc-B'])]:
            response = self.response(a)
            response[field] = value
            with self.assertRaises(ContextError):
                self.runtime.validate_response(response)

    def test_uncheckpointed_context_cannot_be_replaced_or_provider_changed(self):
        self.open_a()
        with self.assertRaises(ContextError):
            self.runtime.select_provider('provider-B')
        with self.assertRaises(ContextError):
            self.runtime.open_context('context-B', [None] * 6, 'rules')

    def test_checkpoint_failure_does_not_clean_active_context(self):
        a = self.open_a()
        with patch('context_runtime.os.replace', side_effect=OSError('simulated failure')):
            with self.assertRaises(OSError):
                self.runtime.checkpoint_and_close(self.response(a))
        self.assertIsNotNone(self.runtime.active)

    def test_caller_mutation_cannot_modify_active_context(self):
        a = self.open_a()
        a['documents'].clear()
        with self.assertRaises(ContextError):
            self.runtime.validate_response(self.response(a))

    def test_restart_after_checkpoint_verifies_files_and_prevents_context_reuse(self):
        a = self.open_a()
        receipt = self.runtime.checkpoint_and_close(self.response(a))
        resumed = ContextRuntime(self.tmp.name, 'run-test')
        with self.assertRaises(ContextError):
            resumed.open_context('context-A', [None] * 6, 'rules')
        Path(receipt['path']).write_text('tampered')
        with self.assertRaisesRegex(ContextError, 'CHECKPOINT_HASH_MISMATCH'):
            ContextRuntime(self.tmp.name, 'run-test')

    def test_unfinished_restart_requires_recovery(self):
        self.open_a()
        with self.assertRaisesRegex(ContextError, 'RECOVERY_REQUIRED'):
            ContextRuntime(self.tmp.name, 'run-test')

    def test_journal_tamper_is_rejected(self):
        self.runtime.journal.write_text(self.runtime.journal.read_text().replace('provider-A', 'X'))
        with self.assertRaisesRegex(ContextError, 'JOURNAL_HASH_MISMATCH'):
            ContextRuntime(self.tmp.name, 'run-test')

    def test_extraction_version_and_source_change_have_distinct_cache_keys(self):
        self.assertNotEqual(self.key, self.runtime.cache_extraction(b'fictional source A', {'literal': 'new'}))
        self.assertNotEqual(self.key, self.runtime.cache_extraction(b'changed', {'literal': 'EXCLUSIVE_A_MARKER'}))


class RoutingTests(unittest.TestCase):
    def test_unqualified_route_is_evaluation_only(self):
        result = select_route('extract')
        self.assertEqual(result['model'], 'gpt-5.6-luna')
        self.assertEqual(result['action'], 'EVALUATE_ONLY')

    def test_signal_escalates_without_publishing(self):
        result = select_route('extract', ['incomplete_coverage'])
        self.assertEqual(result['model'], 'gpt-6.1-sol')
        self.assertFalse(result['publication_allowed'])

    def test_qualified_model_still_cannot_publish(self):
        result = select_route('extract', qualified_models=['gpt-5.6-luna'])
        self.assertEqual(result['action'], 'EXECUTE')
        self.assertFalse(result['publication_allowed'])

    def test_exhausted_route_remains_review(self):
        result = select_route('reading_recovery', attempted=['gpt-6.1-sol', 'gpt-6-astra'])
        self.assertEqual(result['action'], 'REVIEW_REQUIRED')

    def test_exact_comparison_and_publication_are_deterministic(self):
        for task in ('hash_compare', 'publish'):
            self.assertEqual(select_route(task)['action'], 'DETERMINISTIC')

    def test_unknown_inputs_fail_closed(self):
        for task, signals in [('unknown', []), ('extract', ['unknown']), ('extract', 'complex_scope')]:
            with self.assertRaises(ContextError):
                select_route(task, signals)


if __name__ == '__main__':
    unittest.main()
