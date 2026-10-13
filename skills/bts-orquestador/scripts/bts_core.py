"""Pure comparison helpers for BTS contract 5.2, candidate revision F6-1. No workflow, writes, OCR or network.

Inputs are already corroborated normalized facts. These helpers do not prove
identity, applicability, scope, document authenticity, or semantic clauses.
"""
from datetime import date
from decimal import Decimal, InvalidOperation, localcontext
from collections import Counter
import hashlib
import json
import re
import unicodedata

class InputReview(ValueError):
    """Caller must record revision/dependency; never coerce to False/absence."""

def canonical_hash(value):
    """Snapshot digest, not a row identifier. JSON objects with string keys only."""
    def check(v):
        if isinstance(v, dict):
            if any(not isinstance(k,str) for k in v): raise InputReview('NON_STRING_KEY')
            for x in v.values(): check(x)
        elif isinstance(v,list):
            for x in v: check(x)
        elif isinstance(v,float): raise InputReview('FLOAT_NOT_ALLOWED')
        elif v is not None and not isinstance(v,(str,int,bool)):
            raise InputReview('UNSUPPORTED_SNAPSHOT_TYPE')
    check(value)
    raw=json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

def file_hash(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def format_name(value):
    """Case, accents, Unicode canonical decomposition, whitespace only."""
    if not isinstance(value,str): raise InputReview('NAME_TYPE')
    s=''.join(c for c in unicodedata.normalize('NFD',value) if not unicodedata.combining(c))
    return ' '.join(s.upper().split())

def provider_candidate(folder, provider, exception, number=None):
    """Candidate by name only: caller proves root, number provenance and uniqueness."""
    f,p,e=map(format_name,(folder,provider,exception))
    if not p:raise InputReview('PROVIDER_MISSING')
    if number is not None and (not isinstance(number,str) or not re.fullmatch(r'[0-9]+',number)):
        raise InputReview('PROVIDER_NUMBER_TYPE')
    if f==e and p==e:return number is None
    m=re.fullmatch(r'(.+?) PROVEEDOR-\s*([0-9]+)',f)
    return bool(m and m[1]==p and (number is None or m[2]==number))

def identifier(literal, kind):
    """No padding, truncation, digit repair or forced DNI type."""
    if not isinstance(literal,str) or not literal:raise InputReview('IDENTIFIER_MISSING')
    if kind in ('PASAPORTE','OTRO'):return literal
    if kind=='DNI':
        if not (re.fullmatch(r'[0-9]+',literal) or re.fullmatch(r'[0-9]{1,3}(?:\.[0-9]{3})+',literal)):
            raise InputReview('DNI_FORMAT')
        return literal.replace('.','')
    if kind in ('CUIT','CUIL'):
        if not (re.fullmatch(r'[0-9]{11}',literal) or re.fullmatch(r'[0-9]{2}-[0-9]{8}-[0-9]',literal)):
            raise InputReview('CUIT_FORMAT')
        return literal.replace('-','')
    raise InputReview('IDENTIFIER_TYPE_UNCERTAIN')

def central_dni(cuit, explicit_dni=None):
    result=identifier(cuit,'CUIT')[2:10]
    if explicit_dni is not None and identifier(explicit_dni,'DNI')!=result:
        raise InputReview('IDENTITY_CONFLICT')
    return result

def name_candidate(left,right,allow_omission=False):
    """Token comparison only. Omissions require confirmed DNI and semantic review.
    Caller keeps surname/given-name roles and does not accept surname contradiction.
    Do not use allow_omission for clause entities or name-only associations.
    """
    a,b=Counter(format_name(left).split()),Counter(format_name(right).split())
    if not a or not b:raise InputReview('NAME_MISSING')
    return a==b or (allow_omission and (a<=b or b<=a))

def iso_date(value):
    if not isinstance(value,str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',value):
        raise InputReview('DATE_NOT_NORMALIZED')
    try:return date.fromisoformat(value)
    except ValueError as e:raise InputReview('DATE_INVALID') from e

def expiry_at_least(expiry, minimum):
    """H date predicate only: deliberately no start-date argument."""
    return iso_date(expiry)>=iso_date(minimum)

def period_in_range(period, first, last):
    """I period predicate only: no payment-date or balance argument."""
    for value in (period,first,last):
        if not isinstance(value,str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}',value):
            raise InputReview('PERIOD_NOT_NORMALIZED')
        iso_date(value+'-01')
    if first>last:raise InputReview('PERIOD_CONFIG_CONFLICT')
    return first<=period<=last

def interval_covers(start,end,event_start,event_end,logical_key,blank_end_observed=False):
    """Only L/M/N, dates whose day-level interpretation has been corroborated.
    Hours/uncertain endpoints require document review before this helper.
    """
    if logical_key not in ('L','M','N'):raise InputReview('INTERVAL_RULE_NOT_APPLICABLE')
    a,b=iso_date(event_start),iso_date(event_end)
    if a>b:raise InputReview('EVENT_CONFIG_CONFLICT')
    begin=iso_date(start)
    if end is None:
        if logical_key=='L' and blank_end_observed is True:return begin<=a
        raise InputReview('END_UNKNOWN')
    finish=iso_date(end)
    if finish<begin:raise InputReview('INTERVAL_INVALID')
    return begin<=a and finish>=b

def exact_amount(value):
    """Canonical nonnegative decimal string, no locale guessing or floats."""
    if not isinstance(value,str) or not re.fullmatch(r'[0-9]+(?:\.[0-9]+)?',value):
        raise InputReview('AMOUNT_NOT_NORMALIZED')
    try:return Decimal(value)
    except InvalidOperation as e:raise InputReview('AMOUNT_INVALID') from e

def amount_at_least(value, minimum):return exact_amount(value)>=exact_amount(minimum)

def compatible_expense_total(limits):
    """Arithmetic AFTER caller proves same compatible set/person/currency/scope.
    Each item has id, category (joint, medical, pharmacy), amount. No automatic
    combining joint and separate limits, overlapping alternatives or repeated IDs.
    Absence is not zero. A single qualifying medical/pharmacy limit is allowed.
    """
    if not isinstance(limits,list) or not limits:raise InputReview('EXPENSE_LIMIT_MISSING')
    ids=set(); cats=set(); amounts=[]
    for item in limits:
        if not isinstance(item,dict):raise InputReview('LIMIT_TYPE')
        ident=item.get('id'); cat=item.get('category')
        if not isinstance(ident,str) or not ident or ident in ids:raise InputReview('DUPLICATE_LIMIT')
        if cat not in ('joint','medical','pharmacy') or cat in cats:raise InputReview('LIMITS_NOT_DISTINCT')
        ids.add(ident); cats.add(cat);amounts.append(exact_amount(item.get('amount')))
    if 'joint' in cats and len(cats)>1:raise InputReview('OVERLAPPING_LIMITS')
    with localcontext() as ctx:
        ctx.prec=sum(len(format(value,'f'))+1 for value in amounts)+10
        return format(sum(amounts,Decimal('0')),'f')

def affected_results(changed_ids,dependencies):
    """Transitive closure on stored evidence/rule/input dependencies. Cycles terminate."""
    def ids(value):
        if not isinstance(value,(list,tuple,set)) or any(not isinstance(x,str) or not x for x in value):
            raise InputReview('DEPENDENCY_IDS_TYPE')
    ids(changed_ids)
    if not isinstance(dependencies,dict) or any(not isinstance(k,str) or not k for k in dependencies):
        raise InputReview('DEPENDENCY_GRAPH_TYPE')
    for inputs in dependencies.values():ids(inputs)
    affected=set(changed_ids)
    while True:
        extra={consumer for consumer,inputs in dependencies.items() if set(inputs)&affected}
        if extra<=affected:return sorted(set(dependencies)&affected)
        affected.update(extra)

def compare_readback(expected, observed):
    """Requires complete typed snapshot from adapter, never write response alone.
    Comparison supports ORQ; does not prove permissions/concurrency/durable commit.
    """
    required={'spreadsheet_id','tab_id','row_context_id','schema_hash','cells'}
    for value in (expected,observed):
        if not isinstance(value,dict) or not required<=value.keys():raise InputReview('READBACK_INCOMPLETE')
        if not isinstance(value['cells'],list) or not value['cells']:raise InputReview('READBACK_EMPTY')
        positions=set()
        for cell in value['cells']:
            if not isinstance(cell,dict) or not {'a1','type','value'}<=cell.keys():raise InputReview('CELL_INCOMPLETE')
            if not isinstance(cell['a1'],str) or not cell['a1'] or not isinstance(cell['type'],str) or not cell['type']:
                raise InputReview('CELL_TYPE_OR_LOCATION_MISSING')
            if cell['a1'] in positions:raise InputReview('DUPLICATE_CELL')
            positions.add(cell['a1'])
        for key in required-{'cells'}:
            if value[key] is None or value[key]=='':raise InputReview('READBACK_IDENTITY_MISSING')
    # A1 identifies each cell; adapter enumeration order is not spreadsheet state.
    def ordered(value):
        return {**value,'cells':sorted(value['cells'],key=lambda cell:cell['a1'])}
    return canonical_hash(ordered(expected))==canonical_hash(ordered(observed))

def describe():
    return {'version':'bts-5.2','kind':'pure_helpers','workflow_execution':False,
            'functions':[name for name in ('canonical_hash','file_hash','format_name','provider_candidate','identifier','central_dni','name_candidate','expiry_at_least','period_in_range','interval_covers','amount_at_least','compatible_expense_total','affected_results','compare_readback')],
            'limits':'Predicates only; semantic evidence, scope and actual readback remain caller responsibilities.'}

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--describe',action='store_true',help='Print interface metadata; no facts evaluated')
    args=parser.parse_args()
    if args.describe:print(json.dumps(describe(),ensure_ascii=False,indent=2))
    else:parser.print_help()
