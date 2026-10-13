"""Run using KiCad's bundled Python after importing both original Eagle boards."""
from pathlib import Path
import json
import shutil
import xml.etree.ElementTree as ET
import pcbnew as p
import wx

APP = wx.App(False)

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT.parent / 'pcb-audit' / 'extracted'
SOURCE = ROOT / 'source'
VERIFY = ROOT / 'verification'


def mm(x):
    return p.FromMM(x)


def original(name):
    return next(ORIGINAL.rglob(name))


def audit_source(board, eagle_path):
    """Check importer retained original track/via counts and every named net/pad mapping."""
    b = ET.parse(eagle_path).find('.//board')
    fps = {f.GetReference(): f for f in board.GetFootprints()}
    checked = 0
    for signal in b.findall('./signals/signal'):
        for c in signal.findall('contactref'):
            fp = fps[c.get('element')]
            pads = [x for x in fp.Pads() if x.GetNumber() == c.get('pad')]
            assert len(pads) == 1, c.attrib
            assert pads[0].GetNetname() == signal.get('name'), c.attrib
            checked += 1
    tracks = [x for x in board.GetTracks() if not isinstance(x, p.PCB_VIA)]
    vias = [x for x in board.GetTracks() if isinstance(x, p.PCB_VIA)]
    assert len(tracks) == len(b.findall('./signals/signal/wire'))
    assert len(vias) == len(b.findall('./signals/signal/via'))
    return {'original_contactrefs_verified': checked, 'original_tracks': len(tracks),
            'original_vias': len(vias), 'source_zones': len(b.findall('./signals/signal/polygon'))}


def write_rules(stem):
    # Original Eagle clearance is 6 mil; all measured small-board edges >=0.3016 mm.
    # Keep hole-to-copper at 0.20 mm, reflecting actual original geometry.
    (SOURCE / (stem + '.kicad_dru')).write_text('''(version 1)
(rule "Original Eagle 6 mil copper clearance"
  (constraint clearance (min 0.1524mm)))
(rule "Routed edge copper clearance"
  (constraint edge_clearance (min 0.30mm)))
(rule "Hole to copper clearance"
  (constraint hole_clearance (min 0.20mm)))
''')
    (SOURCE / (stem + '.kicad_pro')).write_text(json.dumps({
        'meta': {'filename': stem + '.kicad_pro', 'version': 1},
        'board': {'design_settings': {'rules': {
            'min_clearance': 0.1524, 'min_copper_edge_clearance': 0.30,
            'min_hole_clearance': 0.20, 'min_track_width': 0.1524,
            'min_via_diameter': 0.65, 'min_through_hole_diameter': 0.35,
            'min_silk_text_height': 0.8, 'min_silk_text_thickness': 0.08,
            'solder_mask_clearance': 0.025, 'solder_mask_min_width': 0.10
        }}}
    }, indent=2))


summary = {}
for stem, filename in [('Braille-Cell', 'Braille Cell.brd'),
                       ('Braille-Evaluation', 'Braille Evaluation Board.brd')]:
    path = SOURCE / (stem + '.kicad_pcb')
    board = p.LoadBoard(str(path))
    summary[stem] = audit_source(board, original(filename))
    if stem == 'Braille-Cell':
        # The original author used vias as coil terminals. Model the 12 solder
        # terminals as PTH pads with identical copper, drill, position, and net.
        ef = ET.parse(original(filename)).find('.//board')
        terminal_xy = {}
        for sig in ef.findall('./signals/signal'):
            v = sig.find('via')
            terminal_xy[sig.get('name')] = (mm(float(v.get('x'))), mm(-float(v.get('y'))))
        fp = p.FOOTPRINT(board)
        fp.SetReference('COIL_TERMINALS')
        fp.SetValue('6 coils / 12 exposed PTH solder terminals')
        fp.SetAttributes(p.FP_THROUGH_HOLE)
        fp.SetExcludedFromBOM(True)
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)
        board.Add(fp)
        converted = 0
        for via in list(board.GetTracks()):
            if not isinstance(via, p.PCB_VIA):
                continue
            target = terminal_xy.get(via.GetNetname())
            if target != (via.GetPosition().x, via.GetPosition().y):
                continue
            pad = p.PAD(fp)
            pad.SetNumber(via.GetNetname())
            pad.SetAttribute(p.PAD_ATTRIB_PTH)
            pad.SetShape(p.PAD_SHAPE_CIRCLE)
            pad.SetPosition(via.GetPosition())
            pad.SetSize(p.VECTOR2I(via.GetWidth(p.F_Cu), via.GetWidth(p.F_Cu)))
            pad.SetDrillSize(p.VECTOR2I(via.GetDrillValue(), via.GetDrillValue()))
            layers = p.LSET()
            for layer in (p.F_Cu, p.B_Cu, p.F_Mask, p.B_Mask):
                layers.AddLayer(layer)
            pad.SetLayerSet(layers)
            pad.SetNet(via.GetNet())
            pad.SetLocalSolderMaskMargin(mm(0.025))
            fp.Add(pad)
            board.Remove(via)
            converted += 1
        assert converted == 12
        for f in board.GetFootprints():
            f.Reference().SetVisible(False)
            f.Value().SetVisible(False)
            for pad in f.Pads():
                if pad.GetAttribute() == p.PAD_ATTRIB_PTH:
                    pad.SetLocalSolderMaskMargin(mm(0.025))
        board.GetDesignSettings().SetAuxOrigin(p.VECTOR2I(mm(-20.32), mm(9.779)))
        summary[stem]['coil_vias_converted_to_identical_exposed_PTH_pads'] = converted
    else:
        for f in board.GetFootprints():
            if f.GetValue() == 'BRAILLE-6':
                for pad in f.Pads():
                    pad.SetLocalSolderMaskMargin(mm(0.025))
            if f.GetReference() == 'R1':
                f.SetValue('1k')
            if f.GetReference() in ('IC1', 'IC4'):
                f.SetValue('TBD62083AFG')
            if f.GetReference() == 'U2':
                out = next(x for x in f.Pads() if x.GetNumber() == '2')
                tab = next(x for x in f.Pads() if x.GetNumber() == '4')
                # SOT-223 tab is internally OUT. Same pad number models that link.
                tab.SetNumber('2')
                tab.SetNet(out.GetNet())
                f.SetDuplicatePadNumbersAreJumpers(True)
            if f.GetReference() == 'U$9':
                ground = next(x for x in f.Pads() if x.GetNumber() == 'GND')
                ground.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL)
        board.GetDesignSettings().SetAuxOrigin(p.VECTOR2I(mm(6.53415), mm(-2.4892)))
        summary[stem]['LM317_tab'] = 'pad 4 modeled as internally connected output pad 2'
        summary[stem]['Nano_ground_pad'] = 'solid zone connection instead of one surviving thermal spoke'
    p.SaveBoard(str(path), board)
    write_rules(stem)
    summary[stem]['final_tracks'] = len([x for x in board.GetTracks() if not isinstance(x, p.PCB_VIA)])
    summary[stem]['final_vias'] = len([x for x in board.GetTracks() if isinstance(x, p.PCB_VIA)])
    summary[stem]['PTH_pads'] = sum(x.GetAttribute() == p.PAD_ATTRIB_PTH for f in board.GetFootprints() for x in f.Pads())

(VERIFY / 'source-parity-and-changes.json').write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
