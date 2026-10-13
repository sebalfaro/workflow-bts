"""Candidate routing, not evidence of a benchmark or permission to publish."""
from context_runtime import ContextError

MODELS = {'gpt-5.6-luna', 'gpt-5.6-terra', 'gpt-5.6-sol',
          'gpt-5.4-mini', 'gpt-4.1-mini', 'gpt-6.1-sol', 'gpt-6-astra'}
SIGNALS = {'incomplete_coverage', 'table_disorder', 'unreadable_region',
           'identifier_conflict', 'extraction_disagreement', 'complex_scope'}
TASKS = {'classify', 'extract', 'validate', 'reading_recovery',
         'hash_compare', 'publish'}


def select_route(task, signals=(), attempted=(), qualified_models=()):
    """Selection is explicit and bounded. Qualification must come from evidence.

    Cheapest is not automatically safest. 5.6 Terra competes against 6.1 Sol;
    the default reference uses Sol, which has lower listed output token cost.
    Historical candidates are exercised by the benchmark, not auto-promoted.
    """
    if task not in TASKS or isinstance(signals, str) or isinstance(attempted, str):
        raise ContextError('INVALID_ROUTING_INPUT')
    if not set(signals) <= SIGNALS or not set(attempted) <= MODELS:
        raise ContextError('UNKNOWN_SIGNAL_OR_MODEL')
    if isinstance(qualified_models, str) or not set(qualified_models) <= MODELS:
        raise ContextError('INVALID_QUALIFICATION')
    if task in {'hash_compare', 'publish'}:
        return dict(action='DETERMINISTIC', model=None,
                    publication_allowed=False, reason='adapter required; no model write')
    difficult = bool(signals) or task == 'reading_recovery'
    candidates = (['gpt-6.1-sol', 'gpt-6-astra'] if difficult or task == 'validate'
                  else ['gpt-5.6-luna', 'gpt-6.1-sol', 'gpt-6-astra'])
    for model in candidates:
        if model not in attempted:
            return dict(action='EXECUTE' if model in qualified_models else 'EVALUATE_ONLY',
                        model=model, publication_allowed=False,
                        reason='complexity escalation' if difficult else 'task route',
                        signals=sorted(set(signals)))
    return dict(action='REVIEW_REQUIRED', model=None, publication_allowed=False,
                reason='bounded routes exhausted; never infer absence')
