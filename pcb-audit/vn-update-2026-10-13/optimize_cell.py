"""Move connected track vertices slightly; pads, vias, holes and outline fixed.

Numerical geometry is only a routing aid. KiCad DRC is the acceptance gate.
"""
from pathlib import Path
import json
import numpy as np
import shapely as s
from shapely.geometry import Point, LineString, Polygon, box
from shapely.affinity import rotate, translate
from shapely.ops import polygonize
from scipy.optimize import minimize, least_squares

ROOT=Path(__file__).resolve().parent
g=json.loads((ROOT/'verification/cell-geometry-before.json').read_text())
ts=g['tracks']
keys=[]; index={}
def node(net,pos):
    k=(net,*pos)
    if k not in index:
        index[k]=len(keys); keys.append(k)
    return index[k]
ends=np.array([[node(t['net'],t['start']),node(t['net'],t['end'])] for t in ts])
orig=np.array([k[1:] for k in keys])
anchors={(p['net'],*p['pos']) for p in g['pads']} | {(v['net'],*v['pos']) for v in g['vias']}
free=np.array([i for i,k in enumerate(keys) if k not in anchors])
w=np.array([t['width'] for t in ts])
lines0=s.linestrings(orig[ends])
outline=next(iter(polygonize([LineString(x) for x in g['outline']])))
edge=outline.boundary

padshapes=[]
for p in g['pads']:
    if 'polygon' in p:
        padshapes.append(Polygon(p['polygon']))
        continue
    sx,sy=p['drill'] if p['npth'] else p['size']
    if p['shape']==0 or p['npth']:
        shape=Point(0,0).buffer(sx/2,quad_segs=64)
    elif p['shape']==5:
        r=p['radius']
        shape=box(-sx/2+r,-sy/2+r,sx/2-r,sy/2-r).buffer(r,quad_segs=32)
    else:
        raise ValueError(p)
    shape=translate(rotate(shape,p['angle'],origin=(0,0)),*p['pos'])
    padshapes.append(shape)

# Include nearby pairs, with ample margin for +/-0.30mm movement at each end.
pairs=[]
for i,t in enumerate(ts):
    for k in range(i+1,len(ts)):
        u=ts[k]
        if t['net']!=u['net'] and t['layer']==u['layer']:
            if lines0[i].distance(lines0[k])-(w[i]+w[k])/2 < .95:
                pairs.append((i,k))
pairs=np.array(pairs)
lp=[]
for i,t in enumerate(ts):
    for k,p in enumerate(g['pads']):
        if p['net']==t['net']:
            continue
        if p['npth'] or t['layer'] in p['layers']:
            if lines0[i].distance(padshapes[k])-w[i]/2 < .95:
                lp.append((i,k))
lp=np.array(lp)
lv=[]
for i,t in enumerate(ts):
    for k,v in enumerate(g['vias']):
        if t['net']!=v['net'] and lines0[i].distance(Point(v['pos']))-(w[i]+v['diameter'])/2<.95:
            lv.append((i,k))
lv=np.array(lv)
ps=np.array(padshapes,dtype=object)
vp=s.points([v['pos'] for v in g['vias']])
vd=np.array([v['diameter'] for v in g['vias']])
target=.2010

def geometry(x):
    xy=orig.copy(); xy[free]=x.reshape(-1,2)
    return xy,s.linestrings(xy[ends])

def constraints(x):
    xy,ls=geometry(x)
    c=[s.distance(ls[pairs[:,0]],ls[pairs[:,1]])-(w[pairs[:,0]]+w[pairs[:,1]])/2-target,
       s.distance(ls[lp[:,0]],ps[lp[:,1]])-w[lp[:,0]]/2-target,
       s.distance(ls[lv[:,0]],vp[lv[:,1]])-(w[lv[:,0]]+vd[lv[:,1]])/2-target]
    # Distance to routed outline, including chamfered corners.
    inside=s.covers(outline,ls)
    c.append(s.distance(ls,edge)*np.where(inside,1,-1)-w/2-.2005)
    return np.concatenate(c)

original_lengths=s.length(lines0)
def objective(x):
    xy,ls=geometry(x)
    return np.sum((xy[free]-orig[free])**2)+.005*np.sum((s.length(ls)-original_lengths)**2)

x0=orig[free].ravel()
print('free vertices',len(free),'constraints',len(constraints(x0)),
      'initial worst clearance shortfall',round(float(min(constraints(x0))),6),flush=True)
warm=least_squares(lambda x:np.r_[(x-x0)*.025,np.minimum(constraints(x),0)*30],
                   x0,bounds=(x0-.3,x0+.3),max_nfev=250,ftol=1e-10,xtol=1e-10,gtol=1e-10)
print('warm routing shortfall',float(min(constraints(warm.x))),flush=True)
r=minimize(objective,warm.x,method='SLSQP',bounds=[(z-.30,z+.30) for z in x0],
           constraints={'type':'ineq','fun':constraints},
           options={'maxiter':150,'ftol':1e-10,'disp':True})
xy,ls=geometry(r.x)
res={'optimizer_success':bool(r.success),'message':r.message,
     'worst_constraint_mm':float(min(constraints(r.x))),
     'maximum_node_movement_mm':float(max(np.linalg.norm(xy-orig,axis=1))),
     'tracks':[]}
for i,t in enumerate(ts):
    a,b=xy[ends[i]]
    res['tracks'].append({'uuid':t['uuid'],'start':a.round(6).tolist(),
                          'end':b.round(6).tolist(),'net':t['net'],'layer':t['layer'],
                          'width':t['width']})
(ROOT/'verification/cell-routing-proposal.json').write_text(json.dumps(res,indent=2)+'\n')
print({k:v for k,v in res.items() if k!='tracks'},flush=True)
if res['worst_constraint_mm'] < -0.0001:
    raise SystemExit('Routing proposal is not feasible; do not export.')
