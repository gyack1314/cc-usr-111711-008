"""解释已取得原文中的补贴有效期间业务上下文。"""
from .evidence import records

def snapshot(db,known_at):
    rows=records(db,'context',known_at)
    if not rows:return None
    p=rows[-1]['payload']
    return {'jurisdiction':p['jurisdiction'],'subsidy_start':p['subsidy_start'],'subsidy_end':p['subsidy_end'],'subsidy_per_unit':p['subsidy_per_unit']}

def eligible(s,d,state,period):
    if state is None:return False,'缺少业务上下文'
    return (s.get('jurisdiction',state['jurisdiction'])==state['jurisdiction'],'到岸地区不匹配')

def metrics(allocations,state,period):
    if state is None:return {'context_gap':'缺少业务上下文'}
    return {'applicable_support':state['subsidy_per_unit']*sum(x['quantity'] for x in allocations) if state['subsidy_start']<=period<=state['subsidy_end'] else 0,'jurisdiction':state['jurisdiction']}
