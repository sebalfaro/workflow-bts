"""Executable local boundary test; no model calls, OCR or external writes."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/bts-orquestador/scripts'))
from context_runtime import ContextError, ContextRuntime, digest


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    runtime = ContextRuntime(output, 'local-isolation-trial')
    observations = []
    for provider, context, marker in [
            ('P-A', 'A-1', 'ONLY_A_1'), ('P-A', 'A-2', 'ONLY_A_2'),
            ('P-B', 'B-1', 'ONLY_B_1'), ('P-A', 'A-3', 'ONLY_A_3')]:
        runtime.select_provider(provider)
        key = runtime.cache_extraction(marker.encode(), {'literal': marker})
        runtime.grant(context, 'document-' + context, key)
        payload = runtime.open_context(context, ['Person', 'Synthetic', '000001', provider, 'F', 'X'], 'synthetic-rules')
        allowed = ['document-' + context]
        assert [doc['document_id'] for doc in payload['documents']] == allowed
        content = json.dumps(payload)
        assert all(item['exclusive_marker'] not in content for item in observations)
        response = dict(run_id=payload['run_id'], provider_scope=provider,
                        row_context_id=context, input_sha256=digest(payload), document_ids=allowed,
                        execution_status='LOCAL_BOUNDARY_ONLY_NOT_MODEL_RESULT')
        crossed = dict(response, document_ids=['FOREIGN_DOCUMENT'])
        rejected = False
        try:
            runtime.validate_response(crossed)
        except ContextError:
            rejected = True
        assert rejected
        receipt = runtime.checkpoint_and_close(response)
        observations.append(dict(provider_scope=provider, row_context_id=context,
                                 exclusive_marker=marker, input_sha256=digest(payload),
                                 foreign_document_rejected=rejected, checkpoint=receipt))
    resumed = ContextRuntime(output, 'local-isolation-trial')
    payload = resumed.open_context('after-restart', ['Person', 'Synthetic', '000001', 'P-A', 'F', 'X'], 'synthetic-rules')
    assert payload['documents'] == []
    response = dict(run_id=payload['run_id'], provider_scope=payload['provider_scope'],
                    row_context_id=payload['row_context_id'], input_sha256=digest(payload), document_ids=[])
    receipt = resumed.checkpoint_and_close(response)
    report = dict(status='LOCAL_BOUNDARY_CONFIRMED', observations=observations,
                  restart_without_implicit_associations=True, restart_checkpoint=receipt,
                  model_context_erasure_verified=False, pilot_integration_verified=False,
                  shared_store_or_other_machine_recovery_verified=False)
    (output / 'result.json').write_text(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.output)
    print(json.dumps({'status': result['status'], 'contexts': len(result['observations']) + 1}))
