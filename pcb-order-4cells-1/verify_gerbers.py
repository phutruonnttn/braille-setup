"""Independent Gerber/Excellon readback using gerbonara."""
from pathlib import Path
from collections import Counter
import json
import warnings
import xml.etree.ElementTree as ET
from gerbonara import LayerStack
from gerbonara.graphic_objects import Flash

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT.parent / 'pcb-audit/extracted'
warnings.filterwarnings('ignore', category=SyntaxWarning, message='.*G90 header.*')
results = {}
for folder, source_name, nominal_size, pth, npth in [
    ('cell', 'Braille Cell.brd', (7.62, 29.718), {0.35: 15, 0.6: 12}, {1.1: 6, 1.6: 2, 2.1: 2}),
    ('evaluation', 'Braille Evaluation Board.brd', (98.01225, 89.6112),
     {0.35: 183, 0.6: 96, 0.8: 36, 0.813: 3, 1.0: 3, 1.016: 4}, {3.0: 4}),
]:
    stack = LayerStack.open(ROOT / 'gerbers' / folder)
    assert Counter(round(x.aperture.diameter, 6) for x in stack.drill_pth.objects) == pth
    assert Counter(round(x.aperture.diameter, 6) for x in stack.drill_npth.objects) == npth
    required = {('top', 'copper'), ('bottom', 'copper'), ('top', 'mask'),
                ('bottom', 'mask'), ('mechanical', 'outline')}
    assert required <= set(stack.graphic_layers)
    # Outline aperture thickness does not change the fabricated centerline dimensions.
    outline = stack.graphic_layers[('mechanical', 'outline')]
    endpoint_x = [getattr(o, f'x{i}') for o in outline.objects for i in [1, 2]]
    endpoint_y = [getattr(o, f'y{i}') for o in outline.objects for i in [1, 2]]
    size = (max(endpoint_x)-min(endpoint_x), max(endpoint_y)-min(endpoint_y))
    assert all(abs(a-b) < 0.001 for a, b in zip(size, nominal_size)), size
    record = {'outline_centerline_size_mm': size,
              'PTH_drills_by_diameter_mm': pth, 'NPTH_drills_by_diameter_mm': npth,
              'independent_parser': 'gerbonara', 'layers_found': sorted('/'.join(k) for k in stack.graphic_layers)}
    if folder == 'cell':
        board = ET.parse(next(ORIGINAL.rglob(source_name))).find('.//board')
        terminals = [(float(s.find('via').get('x')) + 20.32,
                      float(s.find('via').get('y')) + 9.779)
                     for s in board.findall('./signals/signal')]
        for side in ['top', 'bottom']:
            objects = stack.graphic_layers[(side, 'mask')].objects
            for x, y in terminals:
                matches = [o for o in objects if isinstance(o, Flash) and
                           abs(o.x-x)<0.0005 and abs(o.y-y)<0.0005]
                assert len(matches) == 1, (side, x, y)
                assert matches[0].aperture.diameter > 0.75
        record['all_12_coil_terminals_exposed_on_both_masks'] = True
    for side in ['top', 'bottom']:
        # Avoid the missing-paste warning for a bare, all-through-hole cell PCB.
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            svg = str(stack.to_pretty_svg(side=side, margin=1))
        (ROOT / 'previews' / f'{folder}-{side}.svg').write_text(svg)
    results[folder] = record

(ROOT / 'verification/gerber-readback.json').write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
