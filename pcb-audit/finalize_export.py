"""Normalize checked manufacturing data for a two-design supplier handoff.

Run with Python + gerbonara. Copper, mask and outline data stay unchanged.
"""
from pathlib import Path
from collections import Counter
import json
import zipfile
import warnings
import hashlib
import shutil
from gerbonara import LayerStack

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / 'pcb-audit' / 'final-export'
EXPORT = ROOT / 'export'
BACKUP = ROOT / 'pcb-audit' / 'export-before-final'
WORK.mkdir(exist_ok=True)
EXPORT.mkdir(exist_ok=True)
BACKUP.mkdir(exist_ok=True)
warnings.filterwarnings('ignore', category=SyntaxWarning, message='.*G90 header.*')

EXTENSIONS = {
    '-F_Cu.gbr': '.gtl', '-B_Cu.gbr': '.gbl',
    '-F_Mask.gbr': '.gts', '-B_Mask.gbr': '.gbs',
    '-F_Silkscreen.gbr': '.gto', '-B_Silkscreen.gbr': '.gbo',
    '-F_Paste.gbr': '.gtp', '-B_Paste.gbr': '.gbp',
    '-Edge_Cuts.gbr': '.gm1',
}

COMMON = '''MANUFACTURING DATA - FINAL SUPPLIER HANDOFF

This archive contains ONE PCB design. Manufacturing quantity is ordered
separately. Do not panelize multiple cells by interpreting quantity as artwork.

2 copper layers; nominal 1.6 mm FR-4, 1 oz copper.
Route on the CENTERLINE of the outline. The 0.2032 mm outline stroke is a
drawing width, not additional board material. Job Size is the nominal
centerline size, not the outer stroke bounding box. Do not scale this artwork.
All layers and drills use the same bottom-left fabrication origin in mm.

PTH.drl = PLATED holes. NPTH.drl = NON-PLATED holes.
Use these separate files and preserve the plating classification.
Do not change hole diameters or copper pad dimensions without checking fit.

Checked design constraints: copper spacing 0.1524 mm (6 mil), copper-to-routed
edge 0.30 mm, copper-to-NPTH 0.20 mm. Through-drills down to 0.35 mm.
Local soldermask expansion at the 1.27 mm headers is 0.025 mm; preserve the
separate mask windows. Nominal mask web between neighboring header pads is
0.112 mm. Header finished holes are 0.60 mm; mating pins must fit those holes.
Factory CAM/DFM must support these dimensions; these are not relaxed settings
chosen by the factory. Nominal PCB thickness should match printed assembly.

Included: both copper/mask layers, outline, separate PTH/NPTH drill files,
job information, and applicable NONEMPTY silk/paste layers only.
No BOM, centroid or board source is inside this Gerber archive.
If ordering assembly, use the corrected BOM and regenerated centroid from
the existing project delivery; do not mix in the author's old centroid.

Checked previously in KiCad: zero error-level DRC violations and zero missing
connections under the constraints above. This packaging revision changes
no copper, mask, outline, drill geometry or component positions.
Gerber/Excellon readback was checked independently after packaging.
Hardware operation and factory-specific DFM are not yet verified.
'''

reports = {}
for folder, stem, zipname, size, pth_count, npth_count in [
    ('cell', 'Braille-Cell', 'PCB-nho-Gerber.zip', (7.62, 29.718), 27, 10),
    ('evaluation', 'Braille-Evaluation', 'PCB-to-Gerber.zip', (98.01225, 89.6112), 325, 4),
]:
    source = ROOT / 'pcb-order-4cells/gerbers' / folder
    dest = WORK / folder
    dest.mkdir(exist_ok=True)
    # This work directory belongs solely to this script.
    for old in dest.iterdir():
        if old.is_file():
            old.unlink()
    original = LayerStack.open(source)
    kept = {}
    omitted = []
    for layer_key, layer in original.graphic_layers.items():
        oldname = layer.original_path.name
        if layer_key[1] in ('silk', 'paste') and not any(o.polarity_dark for o in layer.objects):
            omitted.append(oldname)
            continue
        suffix = next(k for k in EXTENSIONS if oldname.endswith(k))
        newname = stem + EXTENSIONS[suffix]
        shutil.copyfile(source / oldname, dest / newname)
        kept[oldname] = newname
    for filename in [stem + '-PTH.drl', stem + '-NPTH.drl']:
        data = (source / filename).read_text()
        # Put the absolute-position directive in the Excellon header, where
        # strict readers expect it. Tool table, units and coordinates are intact.
        header, body = data.split('\n%\n', 1)
        assert body.startswith('G90\n')
        (dest / filename).write_text(header + '\nG90\n%\n' + body[len('G90\n'):])
    job = json.loads((source / (stem + '-job.gbrjob')).read_text())
    job['GeneralSpecs']['Size'] = {'X': size[0], 'Y': size[1]}
    for rule in job['DesignRules']:
        for key in ['PadToPad', 'PadToTrack', 'TrackToTrack']:
            rule[key] = 0.1524
    attrs = []
    for attr in job['FilesAttributes']:
        old = attr['Path']
        if old in kept:
            attr['Path'] = kept[old]
            attrs.append(attr)
    job['FilesAttributes'] = attrs
    (dest / (stem + '-job.gbrjob')).write_text(json.dumps(job, indent=2) + '\n')
    notes = COMMON + f'\nBOARD: {stem}\nNominal size: {size[0]:.5f} x {size[1]:.5f} mm.\nDrilling: {pth_count} plated + {npth_count} non-plated holes.\n'
    if folder == 'cell':
        notes += '''
SMALL BOARD SPECIFIC:
Six coils per cell. All TWELVE coil solder terminal holes must have EXPOSED
COPPER ON BOTH SIDES, exactly as the supplied soldermask artwork specifies.
Do not tent, plug or fill those terminals. Coil mask opening diameter is
0.8064 mm; copper pad diameter is 0.7564 mm; drill is 0.35 mm.
The THREE other routing vias remain tented. Copper/drilling match the official
small-cell layout. No silkscreen text is intended on this small board.
'''
    else:
        notes += '''
LARGE BOARD SPECIFIC:
The board supports up to eight Braille cells. Top silkscreen and top paste
are included. Bottom silk and bottom paste have no printed features and are
omitted. Component positions and fabrication origin are unchanged, so the
regenerated Evaluation-Top-Centroid.csv remains aligned with this Gerber set.
The source retains silk-related warnings and one one-layer via warning.
'''
    (dest / 'README-MANUFACTURING.txt').write_text(notes)

    readback = LayerStack.open(dest)
    assert set(readback.graphic_layers) == set(original.graphic_layers) - {
        k for k, v in original.graphic_layers.items()
        if k[1] in ('silk', 'paste') and not any(o.polarity_dark for o in v.objects)
    }
    assert len(readback.drill_pth.objects) == pth_count
    assert len(readback.drill_npth.objects) == npth_count
    drill = lambda l: Counter((round(o.x, 6), round(o.y, 6), round(o.aperture.diameter, 6)) for o in l.objects)
    assert drill(readback.drill_pth) == drill(original.drill_pth)
    assert drill(readback.drill_npth) == drill(original.drill_npth)
    for old, new in kept.items():
        assert (source / old).read_bytes() == (dest / new).read_bytes()
    profile = readback.graphic_layers[('mechanical', 'outline')]
    xs = [getattr(o, 'x' + str(i)) for o in profile.objects for i in [1, 2]]
    ys = [getattr(o, 'y' + str(i)) for o in profile.objects for i in [1, 2]]
    measured = (max(xs)-min(xs), max(ys)-min(ys))
    assert all(abs(x-y)<0.001 for x, y in zip(measured, size))
    assert all((dest / x['Path']).exists() for x in job['FilesAttributes'])

    candidate = WORK / zipname
    with zipfile.ZipFile(candidate, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(dest.iterdir()):
            z.write(f, f.name)
    with zipfile.ZipFile(candidate) as z:
        assert z.testzip() is None
    for oldname in [zipname, zipname + '.txt']:
        old = EXPORT / oldname
        if old.exists():
            fingerprint = hashlib.sha256(old.read_bytes()).hexdigest()[:12]
            backup = BACKUP / (oldname + '.' + fingerprint + '.bak')
            if not backup.exists():
                shutil.copyfile(old, backup)
            old.unlink()
    shutil.copyfile(candidate, EXPORT / zipname)
    reports[zipname] = {'outline_centerline_size_mm': measured,
                        'PTH_count': pth_count, 'NPTH_count': npth_count,
                        'omitted_empty_layers': omitted,
                        'copper_mask_outline_bytes_unchanged': True,
                        'drill_geometry_unchanged': True,
                        'job_paths_verified': True, 'zip_crc_ok': True,
                        'sha256': hashlib.sha256(candidate.read_bytes()).hexdigest()}

(WORK / 'verification.json').write_text(json.dumps(reports, indent=2))
assert sorted(x.name for x in EXPORT.iterdir() if x.is_file()) == ['PCB-nho-Gerber.zip', 'PCB-to-Gerber.zip']
print(json.dumps(reports, indent=2))
print('Final export contains exactly two valid .zip manufacturing packages.')
