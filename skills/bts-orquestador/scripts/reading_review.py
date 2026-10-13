"""Pure reading-review policy; inputs must be corroborated by the caller.

No OCR, document search, network or spreadsheet mutation is performed here.
An OCR hit is not a corroborated hit. Confidence alone proves no completeness.
"""
from bts_core import InputReview

LOGICAL_KEYS = ('G', 'H', 'I', 'J.montos', 'J.clausulas', 'K', 'L', 'M', 'N')
REASON = 'Revisar documento: no se pudo determinar la inclusión por lectura insuficiente'


def assess_lookup(*, document_present, file_search_complete,
                  target_corroborated, coverage_complete, reading_signals,
                  directed_review_complete, negative_corroborated,
                  technical_error=False):
    """Separate file absence, inconclusive reading and corroborated negative.

    A negative requires complete relevant page/region coverage and a directed
    review of the original; when suspicion exists, recovery must have resolved
    it and the caller must pass reading_signals=[] on a new evidence version.
    Included only means the target is corroborated, not that coverage is valid.
    """
    flags = (document_present, file_search_complete, target_corroborated,
             coverage_complete, directed_review_complete,
             negative_corroborated, technical_error)
    if any(type(flag) is not bool for flag in flags):
        raise InputReview('READING_FLAG_TYPE')
    if not isinstance(reading_signals, list) or any(
            not isinstance(s, str) or not s.strip() for s in reading_signals):
        raise InputReview('READING_SIGNALS_TYPE')
    if target_corroborated and (not document_present or negative_corroborated):
        raise InputReview('READING_EVIDENCE_CONFLICT')
    if technical_error:
        return 'TECHNICAL_PENDING'
    if target_corroborated:
        return 'INCLUDED'
    if not document_present:
        return 'FILE_ABSENT' if file_search_complete else 'TECHNICAL_PENDING'
    if reading_signals or not (coverage_complete and directed_review_complete
                               and negative_corroborated):
        return 'READING_INCONCLUSIVE'
    return 'VALUE_ABSENT'


def make_review_issue(*, issue_id, row_context_id, document_id, document_name,
                      location, affected_logical_keys, evidence_ids):
    """Never invent a location or use another person's document as a reference."""
    for value in (issue_id, row_context_id, document_id, document_name):
        if not isinstance(value, str) or not value.strip():
            raise InputReview('REVIEW_REFERENCE_MISSING')
    if location is not None and (not isinstance(location, str) or not location.strip()):
        raise InputReview('REVIEW_LOCATION_INVALID')
    if (not isinstance(affected_logical_keys, list) or not affected_logical_keys
            or any(k not in LOGICAL_KEYS for k in affected_logical_keys)):
        raise InputReview('REVIEW_KEYS_INVALID')
    if (not isinstance(evidence_ids, list) or not evidence_ids
            or any(not isinstance(e, str) or not e.strip() for e in evidence_ids)):
        raise InputReview('REVIEW_EVIDENCE_MISSING')
    return dict(issue_id=issue_id, row_context_id=row_context_id,
                document_id=document_id, document_name=document_name,
                location=location, affected_logical_keys=sorted(set(affected_logical_keys)),
                evidence_ids=list(dict.fromkeys(evidence_ids)),
                reason=REASON, status='ACTIVE')


def review_output(issues, row_context_id):
    """Render P for one context; reject foreign/duplicate or malformed issues.

    Empty means no active issues in this supplied version, not certified OCR.
    Resolved entries are kept in history and omitted from the current column.
    """
    if not isinstance(issues, list) or not isinstance(row_context_id, str) or not row_context_id:
        raise InputReview('REVIEW_INPUT_INVALID')
    lines, seen = [], set()
    for issue in issues:
        if not isinstance(issue, dict) or issue.get('row_context_id') != row_context_id:
            raise InputReview('REVIEW_CONTEXT_CONFLICT')
        if issue.get('status') not in ('ACTIVE', 'RESOLVED'):
            raise InputReview('REVIEW_STATUS_INVALID')
        checked = make_review_issue(**{k: issue.get(k) for k in (
            'issue_id', 'row_context_id', 'document_id', 'document_name',
            'location', 'affected_logical_keys', 'evidence_ids')})
        if issue.get('reason') != REASON or checked['issue_id'] in seen:
            raise InputReview('REVIEW_ISSUE_CONFLICT')
        seen.add(checked['issue_id'])
        if issue['status'] == 'RESOLVED':
            continue
        location = checked['location'] or 'página/sección no determinada'
        lines.append(f"{REASON} — Documento: {checked['document_name']} "
                     f"[{checked['document_id']}]; {location}; validación afectada: "
                     + ', '.join(checked['affected_logical_keys']))
    return '\n'.join(lines)
