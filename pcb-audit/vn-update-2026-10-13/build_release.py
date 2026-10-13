"""Build reproducible supplier ZIPs from the checked VN 0.20 mm export."""
from pathlib import Path
import csv
import hashlib
import json
import shutil
import zipfile


ROOT = Path(__file__).resolve().parent
RELEASE = ROOT / "release-vn-020mm"
STAGE = RELEASE / "stage"


def reset_dir(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def normalize_excellon(path):
    data = path.read_text()
    header, body = data.split("\n%\n", 1)
    if body.startswith("G90\n"):
        body = body[len("G90\n"):]
        header += "\nG90"
    path.write_text(header + "\n%\n" + body)


def update_job(path, size, allowed_files, pad_to_pad=0.15):
    job = json.loads(path.read_text())
    job["GeneralSpecs"]["Size"] = {"X": size[0], "Y": size[1]}
    for rule in job.get("DesignRules", []):
        rule["PadToPad"] = pad_to_pad
        rule["PadToTrack"] = 0.20
        rule["TrackToTrack"] = 0.20
        rule["TrackToRegion"] = 0.20
        rule["RegionToRegion"] = 0.20
    job["FilesAttributes"] = [
        x for x in job.get("FilesAttributes", []) if x["Path"] in allowed_files
    ]
    path.write_text(json.dumps(job, indent=2) + "\n")


def make_zip(path, files, base):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, f.relative_to(base))
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None


reset_dir(RELEASE)
STAGE.mkdir()

designs = {
    "cell": {
        "stem": "Braille-Cell",
        "size": (7.62, 29.718),
        "keep": [
            "Braille-Cell-F_Cu.gtl", "Braille-Cell-B_Cu.gbl",
            "Braille-Cell-F_Mask.gts", "Braille-Cell-B_Mask.gbs",
            "Braille-Cell-Edge_Cuts.gm1", "Braille-Cell-PTH.drl",
            "Braille-Cell-NPTH.drl", "Braille-Cell-job.gbrjob",
            "README-MANUFACTURING.txt",
        ],
        "zip": "Braille-Cell-Gerbers-VN-020mm.zip",
    },
    "evaluation": {
        "stem": "Braille-Evaluation",
        "size": (98.01225, 89.6112),
        "keep": [
            "Braille-Evaluation-F_Cu.gtl", "Braille-Evaluation-B_Cu.gbl",
            "Braille-Evaluation-F_Mask.gts", "Braille-Evaluation-B_Mask.gbs",
            "Braille-Evaluation-F_Paste.gtp",
            "Braille-Evaluation-F_Silkscreen.gto",
            "Braille-Evaluation-Edge_Cuts.gm1",
            "Braille-Evaluation-PTH.drl", "Braille-Evaluation-NPTH.drl",
            "Braille-Evaluation-job.gbrjob", "README-MANUFACTURING.txt",
        ],
        "zip": "Braille-Evaluation-Gerbers-VN-020mm.zip",
    },
}

gerber_zips = {}
for name, cfg in designs.items():
    source = ROOT / "gerbers" / name
    dest = STAGE / name
    dest.mkdir()
    for filename in cfg["keep"]:
        shutil.copyfile(source / filename, dest / filename)
    for drill in dest.glob("*.drl"):
        normalize_excellon(drill)
    job_path = dest / f"{cfg['stem']}-job.gbrjob"
    allowed = {x for x in cfg["keep"] if x != "README-MANUFACTURING.txt"}
    update_job(job_path, cfg["size"], allowed)
    output = RELEASE / cfg["zip"]
    make_zip(output, sorted(dest.iterdir()), dest)
    gerber_zips[name] = output

# Evaluation-board PCBA archive.
pcba = STAGE / "PCBA"
(pcba / "Gerber").mkdir(parents=True)
for f in sorted((STAGE / "evaluation").iterdir()):
    shutil.copyfile(f, pcba / "Gerber" / f.name)
for f in [
    ROOT / "bom" / "Evaluation-BOM-Corrected.csv",
    ROOT / "bom" / "Evaluation-BOM-SMD.csv",
    ROOT / "bom" / "Evaluation-BOM-Hand-Assembly.csv",
    ROOT / "assembly" / "Evaluation-Top-Centroid.csv",
]:
    shutil.copyfile(f, pcba / f.name)
make_zip(
    RELEASE / "Braille-Evaluation-PCBA-VN-020mm.zip",
    sorted(x for x in pcba.rglob("*") if x.is_file()), pcba,
)

# Supplier handoff containing two board ZIPs plus the PCBA option and order note.
order_note = RELEASE / "ORDER-NOTE.txt"
order_note.write_text(
    "BRAILLE PCB ORDER - VN 0.20 MM REVISION\n\n"
    "Requested quantity: FOUR identical small Braille cell PCBs and ONE large "
    "evaluation/driver PCB.\n\n"
    "Small board: 7.620 x 29.718 mm. Large board: 98.01225 x 89.61120 mm.\n"
    "Both are 2-layer, nominal 1.6 mm FR-4, 1 oz copper.\n\n"
    "Please run DFM on the enclosed final ZIPs and return the CAM preview before "
    "production. The small board has 0.2010 mm minimum ordinary copper clearance, "
    "0.2032 mm tracks, 0.35 mm minimum drill, and a 0.15 mm local fixed-pad "
    "exception. Preserve exposed copper/mask openings on both sides of all twelve "
    "coil terminals.\n"
)
order_files = [
    order_note,
    gerber_zips["cell"],
    gerber_zips["evaluation"],
    RELEASE / "Braille-Evaluation-PCBA-VN-020mm.zip",
]
make_zip(
    RELEASE / "Braille-PCB-Order-4-small-1-large-VN-020mm.zip",
    order_files, RELEASE,
)

# Reproducibility/source archive for the team, not required by the factory.
source_files = sorted((ROOT / "source").glob("Braille-Cell.kicad_*")) + [
    ROOT / "apply_routing.py", ROOT / "optimize_cell.py",
    ROOT / "verify_vn_export.py", ROOT / "verify_release.py",
    ROOT / "build_release.py",
    ROOT / "README-VN-UPDATE.md",
]
make_zip(RELEASE / "Braille-Cell-KiCad-Source-VN-020mm.zip", source_files, ROOT)

hashes = []
for f in sorted(RELEASE.glob("*.zip")):
    hashes.append(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}")
(RELEASE / "SHA256SUMS.txt").write_text("\n".join(hashes) + "\n")

# The stage is reproducible and should not be part of the handoff.
shutil.rmtree(STAGE)
print("\n".join(str(x) for x in sorted(RELEASE.iterdir())))
