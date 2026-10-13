"""Read-only geometry audit for the supplier messages received 2026-10-13.

This measures routed straight tracks and round vias. It is NOT a full DRC:
pad shapes, zones, mask, drill registration and assembly rules are not checked.
Run with /tmp/braille-gerber-compare-env/bin/python.
"""
from pathlib import Path
from collections import Counter
from math import hypot
import re
import json
import zipfile
import hashlib
from gerbonara import LayerStack

ROOT = Path(__file__).resolve().parent.parent


def parse(text):
    tokens = iter(re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', text))
    def node():
        out = []
        for t in tokens:
            if t == ')':
                return out
            out.append(node() if t == '(' else t.strip('"'))
        return out
    assert next(tokens) == '('
    return node()


def value(node, key):
    return next((x[1:] for x in node if isinstance(x, list) and x[0] == key), [])


def point_distance(p, a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]
    den = dx*dx + dy*dy
    t = max(0, min(1, ((p[0]-a[0])*dx+(p[1]-a[1])*dy)/den)) if den else 0
    return hypot(p[0]-a[0]-t*dx, p[1]-a[1]-t*dy)


def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def segment_distance(a, b, c, d):
    if cross(a,b,c)*cross(a,b,d)<0 and cross(c,d,a)*cross(c,d,b)<0:
        return 0
    return min(point_distance(a,c,d), point_distance(b,c,d),
               point_distance(c,a,b), point_distance(d,a,b))


def brief(t):
    return {k:v for k,v in t.items() if k!='bbox'}


results = {}
for stem, archive in [('Braille-Cell','PCB-nho-Gerber.zip'),
                      ('Braille-Evaluation','PCB-to-PCBA.zip')]:
    source = ROOT/'export'/'PCB-source-KiCad'/f'{stem}.kicad_pcb'
    board = parse(source.read_text())
    tracks, vias = [], []
    for n in board:
        if not isinstance(n,list):
            continue
        if n[0]=='segment':
            a,b = [tuple(map(float,value(n,k))) for k in ('start','end')]
            tracks.append({'start':a,'end':b,'width':float(value(n,'width')[0]),
                'layer':value(n,'layer')[0],'net':value(n,'net')[0],
                'bbox':(min(a[0],b[0]),min(a[1],b[1]),max(a[0],b[0]),max(a[1],b[1]))})
        elif n[0]=='via':
            vias.append({'at':tuple(map(float,value(n,'at'))),
                         'diameter':float(value(n,'size')[0]),
                         'drill':float(value(n,'drill')[0]),'net':value(n,'net')[0]})
    pair_counts = {'below_0.20_mm':0,'below_0.35_mm':0}
    minimum = (float('inf'),None,None)
    examples = []
    for i,t in enumerate(tracks):
        for u in tracks[i+1:]:
            if t['net']==u['net'] or t['layer']!=u['layer']:
                continue
            a,b=t['bbox'],u['bbox']
            limit=.35+(t['width']+u['width'])/2
            if max(a[0]-b[2],b[0]-a[2],a[1]-b[3],b[1]-a[3]) > limit:
                continue
            gap=segment_distance(t['start'],t['end'],u['start'],u['end'])-(t['width']+u['width'])/2
            if gap<minimum[0]:
                minimum=(gap,t,u)
            for threshold,key in [(.20,'below_0.20_mm'),(.35,'below_0.35_mm')]:
                if gap<threshold-1e-6:
                    pair_counts[key]+=1
            if gap<.20-1e-6 and len(examples)<6:
                examples.append({'gap_mm':round(gap,7),'a':brief(t),'b':brief(u)})
    arc_count=sum(isinstance(n,list) and n[0]=='arc' for n in board)
    via_track_min = (float('inf'), None, None)
    via_track_counts = {'below_0.20_mm':0, 'below_0.35_mm':0}
    for v in vias:
        for t in tracks:
            if v['net']==t['net']:
                continue
            gap=point_distance(v['at'],t['start'],t['end'])-(v['diameter']+t['width'])/2
            if gap<via_track_min[0]:
                via_track_min=(gap,v,t)
            for threshold,key in [(.20,'below_0.20_mm'),(.35,'below_0.35_mm')]:
                if gap<threshold-1e-6:
                    via_track_counts[key]+=1
    zpath=ROOT/'export'/archive
    with zipfile.ZipFile(zpath) as z:
        crc_ok=z.testzip() is None
    stack=LayerStack.open(zpath)
    flashes={side:dict(Counter(round(o.aperture.diameter,6)
                for o in stack.graphic_layers[(side,'copper')].objects
                if type(o).__name__=='Flash' and type(o.aperture).__name__=='CircleAperture'))
             for side in ('top','bottom')}
    results[stem]={
        'source':str(source.relative_to(ROOT)), 'archive':str(zpath.relative_to(ROOT)),
        'archive_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),
        'archive_crc_ok':crc_ok,
        'straight_track_count':len(tracks),'unmeasured_track_arc_count':arc_count,
        'track_width_counts_mm':dict(Counter(t['width'] for t in tracks)),
        'routing_via_count':len(vias),
        'routing_via_dimensions':dict(Counter(f"D={v['diameter']}; drill={v['drill']}; ring={(v['diameter']-v['drill'])/2:.4f}" for v in vias)),
        'gerber_circle_flash_diameters_mm':flashes,
        'excellon_PTH_drill_counts_mm':dict(Counter(round(o.aperture.diameter,6) for o in stack.drill_pth.objects)),
        'different_net_same_layer_straight_track_pair_counts':pair_counts,
        'minimum_measured_track_track_gap_mm':round(minimum[0],7),
        'minimum_pair':{'a':brief(minimum[1]),'b':brief(minimum[2])},
        'examples_below_0.20_mm':examples,
        'minimum_measured_via_track_gap_mm':round(via_track_min[0],7),
        'different_net_via_track_pair_counts':via_track_counts,
        'header_nominal_pitch_mm':1.27, 'header_pad_width_mm':1.108,
        'header_nominal_adjacent_pad_edge_gap_mm':round(1.27-1.108,6),
        'scope':'Tracks and round-via sizes; not a full DRC. Pair counts are not unique repair-site counts.'}
out=ROOT/'pcb-audit'/'vn-dfm-2026-10-13.json'
out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
for name,r in results.items():
    print(name, json.dumps({k:r[k] for k in ['track_width_counts_mm','routing_via_dimensions',
        'minimum_measured_track_track_gap_mm','different_net_same_layer_straight_track_pair_counts']},ensure_ascii=False))
print(out)
