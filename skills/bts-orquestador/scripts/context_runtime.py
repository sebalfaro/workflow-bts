"""Local, single-writer context boundary. Not a model-memory eraser or Sheet adapter."""
import hashlib
import json
import os
from pathlib import Path


class ContextError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def require_id(value):
    if not isinstance(value, str) or not value.strip():
        raise ContextError('NONEMPTY_ID_REQUIRED')
    return value


class ContextRuntime:
    """Neutral immutable extraction cache; explicit grants per occurrence.

    Journal hashes describe the boundary; checkpoints contain recoverable data.
    Use a private directory. No concurrency or shared-Drive durability guarantee.
    An unfinished journal requires recovery instead of silently reopening.
    """

    def __init__(self, directory, run_id):
        self.run_id = require_id(run_id)
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.journal = self.directory / 'context-journal.jsonl'
        self.cache = {}
        self.grants = {}
        self.active = None
        self.provider = None
        self.seen = set()
        self.head = '0' * 64
        opened = None
        if self.journal.exists():
            for line in self.journal.read_text().splitlines():
                entry = json.loads(line)
                checksum = entry.pop('sha256')
                if entry['previous_sha256'] != self.head or digest(entry) != checksum:
                    raise ContextError('JOURNAL_HASH_MISMATCH')
                if entry['run_id'] != self.run_id:
                    raise ContextError('RUN_MISMATCH')
                self.head = checksum
                if entry['event'] == 'OPEN':
                    opened = entry['row_context_id']
                    self.seen.add(opened)
                elif entry['event'] == 'CLOSE':
                    if opened != entry['row_context_id']:
                        raise ContextError('JOURNAL_CONTEXT_MISMATCH')
                    checkpoint = self.directory / entry['checkpoint_file']
                    if (not checkpoint.is_file() or
                            hashlib.sha256(checkpoint.read_bytes()).hexdigest() != entry['checkpoint_sha256']):
                        raise ContextError('CHECKPOINT_HASH_MISMATCH')
                    opened = None
                elif entry['event'] == 'PROVIDER':
                    self.provider = entry['provider_scope']
            if opened is not None:
                raise ContextError('RECOVERY_REQUIRED: unfinished context')

    def _event(self, event, **data):
        entry = dict(event=event, run_id=self.run_id,
                     previous_sha256=self.head, **data)
        checksum = digest(entry)
        entry['sha256'] = checksum
        with self.journal.open('a') as stream:
            stream.write(canonical(entry) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        self.head = checksum

    def select_provider(self, provider):
        require_id(provider)
        if self.active is not None:
            raise ContextError('CHECKPOINT_REQUIRED_BEFORE_PROVIDER_CHANGE')
        if provider != self.provider:
            self._event('PROVIDER', provider_scope=provider,
                        previous_provider=self.provider)
            self.provider = provider
            self.grants.clear()

    def cache_extraction(self, source_bytes, extraction):
        if not isinstance(source_bytes, bytes):
            raise ContextError('SOURCE_BYTES_REQUIRED')
        if not isinstance(extraction, dict):
            raise ContextError('EXTRACTION_OBJECT_REQUIRED')
        source_hash = hashlib.sha256(source_bytes).hexdigest()
        record = dict(source_sha256=source_hash, extraction=extraction)
        key = digest(record)  # includes extraction version, not just original bytes
        self.cache[key] = canonical(record)
        return key

    def grant(self, row_context_id, document_id, cache_key):
        require_id(row_context_id)
        require_id(document_id)
        if self.active is not None or not self.provider:
            raise ContextError('GRANT_BEFORE_OPEN_IN_PROVIDER_SCOPE')
        if cache_key not in self.cache:
            raise ContextError('UNKNOWN_EXTRACTION')
        grants = self.grants.setdefault((self.provider, row_context_id), {})
        if document_id in grants and grants[document_id] != cache_key:
            raise ContextError('DOCUMENT_VERSION_CONFLICT')
        grants[document_id] = cache_key

    def open_context(self, row_context_id, source_af, ruleset_hash):
        require_id(row_context_id)
        require_id(ruleset_hash)
        if not self.provider or self.active is not None:
            raise ContextError('PROVIDER_REQUIRED_OR_CONTEXT_STILL_OPEN')
        if row_context_id in self.seen:
            raise ContextError('CONTEXT_ALREADY_USED: use a new evaluation context')
        if not isinstance(source_af, list) or len(source_af) != 6:
            raise ContextError('SOURCE_AF_REQUIRED')
        docs = []
        for doc_id, key in sorted(self.grants.get((self.provider, row_context_id), {}).items()):
            docs.append(dict(document_id=doc_id, extraction_key=key,
                             **json.loads(self.cache[key])))
        payload = dict(boundary_version='bts-context-1', run_id=self.run_id,
                       provider_scope=self.provider, row_context_id=row_context_id,
                       source_af=source_af, ruleset_hash=ruleset_hash, documents=docs)
        serialized = canonical(payload)  # copy, never expose a mutable active object
        self._event('OPEN', row_context_id=row_context_id,
                    provider_scope=self.provider, input_sha256=digest(payload),
                    document_ids=[d['document_id'] for d in docs])
        self.seen.add(row_context_id)
        self.active = serialized
        return json.loads(serialized)

    def validate_response(self, response):
        if self.active is None or not isinstance(response, dict):
            raise ContextError('ACTIVE_CONTEXT_AND_RESPONSE_REQUIRED')
        payload = json.loads(self.active)
        for field in ('run_id', 'provider_scope', 'row_context_id'):
            if response.get(field) != payload[field]:
                raise ContextError('RESPONSE_CONTEXT_MISMATCH')
        if response.get('input_sha256') != digest(payload):
            raise ContextError('RESPONSE_INPUT_MISMATCH')
        evidence = response.get('document_ids')
        allowed = {d['document_id'] for d in payload['documents']}
        if (not isinstance(evidence, list) or
                any(not isinstance(x, str) or x not in allowed for x in evidence) or
                len(evidence) != len(set(evidence))):
            raise ContextError('FOREIGN_OR_INVALID_DOCUMENT_EVIDENCE')
        # This validates association only, not document completeness or truth.
        return json.loads(canonical(response))

    def checkpoint_and_close(self, response):
        checked = self.validate_response(response)
        payload = json.loads(self.active)
        checkpoint = dict(input=payload, response=checked,
                          durability='LOCAL_FSYNC_NOT_SHARED_COMMIT')
        data = (canonical(checkpoint) + '\n').encode()
        filename = 'checkpoint-' + digest(payload) + '.json'
        path = self.directory / filename
        temporary = path.with_suffix('.tmp')
        try:
            with temporary.open('xb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        except OSError:
            temporary.unlink(missing_ok=True)
            raise
        directory_fd = os.open(self.directory, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
        self._event('CLOSE', row_context_id=payload['row_context_id'],
                    checkpoint_file=filename,
                    checkpoint_sha256=hashlib.sha256(data).hexdigest())
        self.active = None
        self.grants.pop((self.provider, payload['row_context_id']), None)
        return dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(),
                    journal_sha256=self.head)
