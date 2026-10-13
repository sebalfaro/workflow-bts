import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/bts-orquestador/scripts'))
import reading_review as policy
from bts_core import InputReview


class ReadingReviewTests(unittest.TestCase):
    def lookup(self, **changes):
        data = dict(document_present=True, file_search_complete=True,
                    target_corroborated=False, coverage_complete=True,
                    reading_signals=[], directed_review_complete=True,
                    negative_corroborated=True, technical_error=False)
        data.update(changes)
        return policy.assess_lookup(**data)

    def issue(self, **changes):
        data = dict(issue_id='synthetic-issue', row_context_id='synthetic-row',
                    document_id='synthetic-doc', document_name='nomina-ficticia.pdf',
                    location='página 2, tabla 1', affected_logical_keys=['N'],
                    evidence_ids=['synthetic-evidence'])
        data.update(changes)
        return policy.make_review_issue(**data)

    def test_negative_ocr_with_suspicion_is_inconclusive(self):
        self.assertEqual(self.lookup(reading_signals=['fila cortada']), 'READING_INCONCLUSIVE')

    def test_incomplete_page_coverage_never_proves_absence(self):
        self.assertEqual(self.lookup(coverage_complete=False), 'READING_INCONCLUSIVE')

    def test_repeated_ocr_without_original_review_is_insufficient(self):
        self.assertEqual(self.lookup(directed_review_complete=False), 'READING_INCONCLUSIVE')

    def test_corroborated_negative_is_value_not_file_absence(self):
        self.assertEqual(self.lookup(), 'VALUE_ABSENT')

    def test_corroborated_hit_can_resolve_inclusion(self):
        self.assertEqual(self.lookup(target_corroborated=True, negative_corroborated=False,
                                    reading_signals=['otra fila ilegible']), 'INCLUDED')

    def test_missing_file_needs_complete_search(self):
        self.assertEqual(self.lookup(document_present=False), 'FILE_ABSENT')
        self.assertEqual(self.lookup(document_present=False, file_search_complete=False),
                         'TECHNICAL_PENDING')

    def test_technical_error_is_not_absence(self):
        self.assertEqual(self.lookup(technical_error=True), 'TECHNICAL_PENDING')

    def test_conflicting_evidence_and_untyped_flags_rejected(self):
        with self.assertRaises(InputReview):
            self.lookup(target_corroborated=True)
        with self.assertRaises(InputReview):
            self.lookup(coverage_complete='yes')

    def test_document_and_location_are_rendered(self):
        text = policy.review_output([self.issue()], 'synthetic-row')
        self.assertIn('nomina-ficticia.pdf [synthetic-doc]', text)
        self.assertIn('página 2, tabla 1', text)
        self.assertIn(policy.REASON, text)

    def test_unknown_location_not_invented(self):
        self.assertIn('página/sección no determinada',
                      policy.review_output([self.issue(location=None)], 'synthetic-row'))

    def test_resolved_issue_preserves_other_active_document(self):
        resolved = self.issue(); resolved['status'] = 'RESOLVED'
        active = self.issue(issue_id='synthetic-other', document_id='doc-other',
                            document_name='otro-ficticio.pdf')
        text = policy.review_output([resolved, active], 'synthetic-row')
        self.assertNotIn('nomina-ficticia.pdf', text)
        self.assertIn('otro-ficticio.pdf', text)

    def test_cross_context_duplicate_and_missing_reference_rejected(self):
        with self.assertRaises(InputReview):
            policy.review_output([self.issue()], 'another-row')
        with self.assertRaises(InputReview):
            policy.review_output([self.issue(), self.issue()], 'synthetic-row')
        with self.assertRaises(InputReview):
            self.issue(document_name='')


if __name__ == '__main__':
    unittest.main()
