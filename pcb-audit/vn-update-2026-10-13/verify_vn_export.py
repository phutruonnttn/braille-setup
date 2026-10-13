"""Read back the VN 0.20 mm Gerber/Excellon export independently."""
from collections import Counter
from pathlib import Path
import json
import warnings
import xml.etree.ElementTree as ET

from gerbonara import LayerStack
from gerbonara.graphic_objects import Flash


ROOT = Path(__file__).resolve().parent
GERBERS = ROOT / "gerbers" / "cell"
ORIGINAL = (
    ROOT.parent / "extracted" / "Braille Cell Eagle Source Files"
    / "Braille Cell Eagle Source Files" / "Braille Cell.brd"
)
OUT = ROOT / "verification" / "cell-gerber-readback.json"
PREVIEWS = ROOT / "previews"
warnings.filterwarnings("ignore", category=SyntaxWarning, message=".*G90 header.*")

stack = LayerStack.open(GERBERS)
required = {
    ("top", "copper"), ("bottom", "copper"),
    ("top", "mask"), ("bottom", "mask"),
    ("mechanical", "outline"),
}
assert required <= set(stack.graphic_layers), sorted(stack.graphic_layers)

pth = Counter(round(x.aperture.diameter, 6) for x in stack.drill_pth.objects)
npth = Counter(round(x.aperture.diameter, 6) for x in stack.drill_npth.objects)
assert pth == {0.35: 15, 0.6: 12}, pth
assert npth == {1.1: 6, 1.6: 2, 2.1: 2}, npth

outline = stack.graphic_layers[("mechanical", "outline")]
xs = [getattr(o, f"x{i}") for o in outline.objects for i in (1, 2)]
ys = [getattr(o, f"y{i}") for o in outline.objects for i in (1, 2)]
size = (max(xs) - min(xs), max(ys) - min(ys))
assert abs(size[0] - 7.62) < 0.001, size
assert abs(size[1] - 29.718) < 0.001, size

# The original design uses the first via of each of the twelve coil nets as a
# solder terminal.  The KiCad source models those locations as exposed PTH pads
# without changing their copper/drill geometry.
eagle = ET.parse(ORIGINAL).find(".//board")
terminals = [
    (float(signal.find("via").get("x")) + 20.32,
     float(signal.find("via").get("y")) + 9.779)
    for signal in eagle.findall("./signals/signal")
]
assert len(terminals) == 12

terminal_checks = {}
for side in ("top", "bottom"):
    mask = stack.graphic_layers[(side, "mask")].objects
    copper = stack.graphic_layers[(side, "copper")].objects
    checked = 0
    for x, y in terminals:
        mask_hits = [
            o for o in mask
            if isinstance(o, Flash) and abs(o.x - x) < 0.0005
            and abs(o.y - y) < 0.0005 and o.aperture.diameter >= 0.80
        ]
        copper_hits = [
            o for o in copper
            if isinstance(o, Flash) and abs(o.x - x) < 0.0005
            and abs(o.y - y) < 0.0005 and o.aperture.diameter >= 0.75
        ]
        assert len(mask_hits) == 1, (side, "mask", x, y, mask_hits)
        assert len(copper_hits) == 1, (side, "copper", x, y, copper_hits)
        checked += 1
    terminal_checks[side] = checked

for side in ("top", "bottom"):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        svg = str(stack.to_pretty_svg(side=side, margin=1))
    (PREVIEWS / f"cell-vn-{side}.svg").write_text(svg)

result = {
    "independent_parser": "gerbonara",
    "outline_centerline_size_mm": [round(x, 6) for x in size],
    "required_layers_present": True,
    "PTH_drills_by_diameter_mm": dict(sorted(pth.items())),
    "NPTH_drills_by_diameter_mm": dict(sorted(npth.items())),
    "coil_terminals_verified": terminal_checks,
    "all_12_coil_terminals_have_copper_and_mask_openings_on_both_sides": True,
}
OUT.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
