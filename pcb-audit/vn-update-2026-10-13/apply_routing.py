"""Apply the reviewed 0.20 mm routing proposal to the small Braille PCB.

Run with KiCad's bundled Python.  The script is deliberately idempotent: each
track must either still match the audited pre-change geometry or already match
the proposal.  It never changes pads, vias, holes, nets, board outline, widths,
or item UUIDs.
"""
from pathlib import Path
import json
import math
import pcbnew as p
import wx


APP = wx.App(False)
ROOT = Path(__file__).resolve().parent
BOARD_PATH = ROOT / "source" / "Braille-Cell.kicad_pcb"
BEFORE_PATH = ROOT / "verification" / "cell-geometry-before.json"
PROPOSAL_PATH = ROOT / "verification" / "cell-routing-proposal.json"
REPORT_PATH = ROOT / "verification" / "cell-routing-applied.json"
TOLERANCE_MM = 0.000_002


def xy_mm(v):
    return (p.ToMM(v.x), p.ToMM(v.y))


def close(a, b):
    return math.dist(a, b) <= TOLERANCE_MM


def point_mm(xy):
    return p.VECTOR2I(p.FromMM(float(xy[0])), p.FromMM(float(xy[1])))


before = json.loads(BEFORE_PATH.read_text())
proposal = json.loads(PROPOSAL_PATH.read_text())
assert proposal["optimizer_success"], proposal["message"]
assert proposal["worst_constraint_mm"] >= -1e-8, proposal["worst_constraint_mm"]

before_by_uuid = {x["uuid"]: x for x in before["tracks"]}
proposal_by_uuid = {x["uuid"]: x for x in proposal["tracks"]}
assert len(before_by_uuid) == len(proposal_by_uuid) == 88
assert set(before_by_uuid) == set(proposal_by_uuid)

board = p.LoadBoard(str(BOARD_PATH))
tracks = {
    x.m_Uuid.AsString(): x
    for x in board.GetTracks()
    if not isinstance(x, p.PCB_VIA)
}
assert set(tracks) == set(proposal_by_uuid), (
    "Track UUID mismatch",
    sorted(set(proposal_by_uuid) - set(tracks)),
    sorted(set(tracks) - set(proposal_by_uuid)),
)

counts_before = {
    "tracks": len(tracks),
    "vias": sum(isinstance(x, p.PCB_VIA) for x in board.GetTracks()),
    "footprints": len(board.GetFootprints()),
    "pads": sum(1 for f in board.GetFootprints() for _ in f.Pads()),
    "zones": len(board.Zones()),
}

changed = 0
already_applied = 0
maximum_actual_movement = 0.0
for uuid, track in tracks.items():
    old = before_by_uuid[uuid]
    new = proposal_by_uuid[uuid]
    assert track.GetNetname() == new["net"]
    assert board.GetLayerName(track.GetLayer()) == new["layer"]
    assert abs(p.ToMM(track.GetWidth()) - new["width"]) <= TOLERANCE_MM

    current_start = xy_mm(track.GetStart())
    current_end = xy_mm(track.GetEnd())
    is_before = close(current_start, old["start"]) and close(current_end, old["end"])
    is_after = close(current_start, new["start"]) and close(current_end, new["end"])
    if not (is_before or is_after):
        raise RuntimeError(
            f"Track {uuid} no longer matches the audited source or proposal: "
            f"{current_start} -> {current_end}"
        )
    if is_after:
        already_applied += 1
        continue

    maximum_actual_movement = max(
        maximum_actual_movement,
        math.dist(old["start"], new["start"]),
        math.dist(old["end"], new["end"]),
    )
    track.SetStart(point_mm(new["start"]))
    track.SetEnd(point_mm(new["end"]))
    changed += 1

p.SaveBoard(str(BOARD_PATH), board)

reloaded = p.LoadBoard(str(BOARD_PATH))
reloaded_tracks = {
    x.m_Uuid.AsString(): x
    for x in reloaded.GetTracks()
    if not isinstance(x, p.PCB_VIA)
}
counts_after = {
    "tracks": len(reloaded_tracks),
    "vias": sum(isinstance(x, p.PCB_VIA) for x in reloaded.GetTracks()),
    "footprints": len(reloaded.GetFootprints()),
    "pads": sum(1 for f in reloaded.GetFootprints() for _ in f.Pads()),
    "zones": len(reloaded.Zones()),
}
assert counts_after == counts_before
assert set(reloaded_tracks) == set(proposal_by_uuid)
for uuid, track in reloaded_tracks.items():
    new = proposal_by_uuid[uuid]
    assert close(xy_mm(track.GetStart()), new["start"]), uuid
    assert close(xy_mm(track.GetEnd()), new["end"]), uuid

report = {
    "board": str(BOARD_PATH.relative_to(ROOT)),
    "proposal_optimizer_success": proposal["optimizer_success"],
    "proposal_worst_constraint_mm": proposal["worst_constraint_mm"],
    "tracks_changed_this_run": changed,
    "tracks_already_applied": already_applied,
    "maximum_endpoint_movement_mm": maximum_actual_movement,
    "unchanged_item_counts": counts_after,
    "changed_geometry": "track start/end coordinates only",
    "unchanged": [
        "nets", "track widths", "pads", "vias", "holes", "outline", "UUIDs"
    ],
}
REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
