"""Export actual pad-envelope centers, separate from KiCad footprint origins."""
import csv
import json
from pathlib import Path
import pcbnew as p
import wx

APP = wx.App(False)
ROOT = Path(__file__).resolve().parent
b = p.LoadBoard(str(ROOT / 'source/Braille-Evaluation.kicad_pcb'))
origin = b.GetDesignSettings().GetAuxOrigin()
with (ROOT / 'bom/Evaluation-BOM-SMD.csv').open(encoding='utf-8-sig', newline='') as f:
    bom = list(csv.DictReader(f))
expected = {s.strip() for r in bom for s in r['Designator'].split(',')}
positions = []
report = {}
for fp in b.GetFootprints():
    if fp.GetReference() not in expected:
        continue
    pads = [x for x in fp.Pads() if x.GetAttribute() == p.PAD_ATTRIB_SMD]
    assert pads, fp.GetReference()
    boxes = [x.GetBoundingBox() for x in pads]
    left, right = min(x.GetLeft() for x in boxes), max(x.GetRight() for x in boxes)
    top, bottom = min(x.GetTop() for x in boxes), max(x.GetBottom() for x in boxes)
    x, y = (left + right) / 2, (top + bottom) / 2
    angle = fp.GetOrientationDegrees() % 360
    positions.append({'Designator': fp.GetReference(),
                      'Mid X': f'{p.ToMM(x-origin.x):.6f}mm',
                      'Mid Y': f'{p.ToMM(origin.y-y):.6f}mm',
                      'Layer': 'Top', 'Rotation': f'{angle:.6f}'})
    report[fp.GetReference()] = {
        'source_coordinate_pad_center_mm': [p.ToMM(x), p.ToMM(-y)],
        'fabrication_origin_mm': [p.ToMM(origin.x), p.ToMM(-origin.y)],
        'rotation_degrees': angle,
    }
assert len(positions) == 72
assert {r['Designator'] for r in positions} == expected
with (ROOT / 'assembly/Evaluation-Top-Centroid.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, ['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation'])
    w.writeheader()
    w.writerows(sorted(positions, key=lambda r: r['Designator']))
(ROOT / 'verification/centroid-verification.json').write_text(json.dumps(report, indent=2))
print('Exported 72 actual SMD pad-envelope centers with the same origin as Gerber/drills.')
for name in ['C5', 'C6', 'IC1', 'Q1', 'U2']:
    print(name, report[name])
