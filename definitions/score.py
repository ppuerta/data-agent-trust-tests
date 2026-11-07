# Classifies each raw answer by which revenue figure it reports. Read the raw files too:
# this only looks for the two figures and a few keywords.
import re, glob, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
def has(text, digits):  # 124634.77 in 124,634.77 / 124.634,77 / 124634.77 / 124 634,77
    pat = r'\b' + r'[.,\s]?'.join(re.findall(r'\d{1,3}', digits)) + r'\b'
    return re.search(pat, text) is not None
rows = collections.defaultdict(list)
headlines = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(HERE, 'raw', '*_q*_*.txt'))):
    name = os.path.basename(f)[:-4]
    cond, q, n = name.split('_')
    t = open(f, encoding='utf-8').read()
    right, allst = has(t, '12463477'), has(t, '15698745')
    kind = 'both' if right and allst else 'completed' if right else 'all statuses' if allst else 'other/none'
    first = t.strip().split('\n\n')[0]  # opening paragraph = what a reader sees first
    h_right, h_all = has(first, '12463477'), has(first, '15698745')
    head = 'completed' if h_right and not h_all else 'all statuses' if h_all and not h_right else 'unclear'
    headlines[cond].append(head)
    states_def = bool(re.search(r'completed|completad|cancel|refund|reembols|devuel', t, re.I))
    rows[(cond, q)].append((kind, states_def))
print('cond question  completed-only | all-statuses | both | other  (answers that mention the definition)')
for (cond, q), v in sorted(rows.items()):
    k = collections.Counter(x[0] for x in v)
    d = sum(1 for x in v if x[1])
    print(f"{cond}    {q:9}  {k['completed']:>3} | {k['all statuses']:>3} | {k['both']:>3} | {k['other/none']:>3}   ({d}/{len(v)})")
for cond in 'ABC':
    v = [x for (c, q), vs in rows.items() if c == cond for x in vs]
    k = collections.Counter(x[0] for x in v)
    print(f"TOTAL {cond}: {len(v)} runs -> completed {k['completed']}, all statuses {k['all statuses']}, both {k['both']}, other {k['other/none']}")
print()
print('Headline = which figure the opening paragraph gives (unclear = none or both):')
for cond in 'ABC':
    k = collections.Counter(headlines[cond])
    print(f'  {cond}: completed {k["completed"]}, all statuses {k["all statuses"]}, unclear {k["unclear"]}')
