"""Verify final supplier archives after packaging."""
from collections import Counter
from pathlib import Path
import json
import re
import tempfile
import zipfile

from gerbonara import LayerStack


ROOT = Path(__file__).resolve().parent
RELEASE = ROOT / "release-vn-020mm"
OUT = ROOT / "verification" / "release-verification.json"


expected = {
    "Braille-Cell-Gerbers-VN-020mm.zip": {
        "size": (7.62, 29.718),
        "pth": {0.35: 15, 0.6: 12},
        "npth": {1.1: 6, 1.6: 2, 2.1: 2},
        "job": "Braille-Cell-job.gbrjob",
    },
    "Braille-Evaluation-Gerbers-VN-020mm.zip": {
        "size": (98.01225, 89.6112),
        "pth": {0.35: 183, 0.6: 96, 0.8: 36, 0.813: 3, 1.0: 3, 1.016: 4},
        "npth": {3.0: 4},
        "job": "Braille-Evaluation-job.gbrjob",
    },
}

results = {}
for name, cfg in expected.items():
    archive = RELEASE / name
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        names = set(z.namelist())
        with tempfile.TemporaryDirectory() as td:
            z.extractall(td)
            root = Path(td)
            stack = LayerStack.open(root)
            pth = Counter(round(x.aperture.diameter, 6) for x in stack.drill_pth.objects)
            npth = Counter(round(x.aperture.diameter, 6) for x in stack.drill_npth.objects)
            assert pth == cfg["pth"], (name, pth)
            assert npth == cfg["npth"], (name, npth)
            outline = stack.graphic_layers[("mechanical", "outline")]
            xs = [getattr(o, f"x{i}") for o in outline.objects for i in (1, 2)]
            ys = [getattr(o, f"y{i}") for o in outline.objects for i in (1, 2)]
            size = (max(xs) - min(xs), max(ys) - min(ys))
            assert all(abs(a - b) < 0.001 for a, b in zip(size, cfg["size"]))

            # All artwork/drills use the chosen positive plot origin.
            for f in root.iterdir():
                # Copper, mask, profile and drills must be positive.  The large
                # board's legacy top legend intentionally extends 0.0115 mm
                # left of the fabrication origin and is covered by the recorded
                # silkscreen-edge warnings; it does not affect fabrication.
                if f.suffix.lower() in {".gtl", ".gbl", ".gts", ".gbs", ".gtp", ".gm1", ".drl"}:
                    text = f.read_text()
                    assert not re.search(r"(?:^|\n)[XY]-", text), f.name
            for drill in root.glob("*.drl"):
                text = drill.read_text()
                assert "G90\n%\n" in text, drill.name
                assert "%\nG90\n" not in text, drill.name

            job = json.loads((root / cfg["job"]).read_text())
            assert job["GeneralSpecs"]["Size"] == {"X": cfg["size"][0], "Y": cfg["size"][1]}
            assert all((root / x["Path"]).exists() for x in job["FilesAttributes"])

    results[name] = {
        "zip_crc_ok": True,
        "outline_centerline_size_mm": list(cfg["size"]),
        "PTH_drills": dict(sorted(pth.items())),
        "NPTH_drills": dict(sorted(npth.items())),
        "same_positive_origin": True,
        "job_paths_exist": True,
    }

pcba_name = "Braille-Evaluation-PCBA-VN-020mm.zip"
with zipfile.ZipFile(RELEASE / pcba_name) as z:
    assert z.testzip() is None
    names = set(z.namelist())
    for required in [
        "Evaluation-BOM-Corrected.csv", "Evaluation-BOM-SMD.csv",
        "Evaluation-BOM-Hand-Assembly.csv", "Evaluation-Top-Centroid.csv",
        "Gerber/Braille-Evaluation-F_Cu.gtl",
        "Gerber/Braille-Evaluation-PTH.drl",
        "Gerber/Braille-Evaluation-NPTH.drl",
    ]:
        assert required in names, required
results[pcba_name] = {"zip_crc_ok": True, "required_pcba_files_present": True}

order_name = "Braille-PCB-Order-4-small-1-large-VN-020mm.zip"
with zipfile.ZipFile(RELEASE / order_name) as z:
    assert z.testzip() is None
    assert {
        "ORDER-NOTE.txt",
        "Braille-Cell-Gerbers-VN-020mm.zip",
        "Braille-Evaluation-Gerbers-VN-020mm.zip",
        "Braille-Evaluation-PCBA-VN-020mm.zip",
    } <= set(z.namelist())
results[order_name] = {"zip_crc_ok": True, "required_nested_archives_present": True}

OUT.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
