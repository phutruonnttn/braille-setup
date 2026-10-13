from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'bom'
OUT.mkdir(exist_ok=True)
FIELDS = ['Qty', 'Designator', 'Footprint', 'Comment', 'LCSC Part #',
          'Description', 'Value', 'Manufacturer', 'MPN / Specification', 'Assembly', 'Notes']


def row(qty, refs, footprint, value, description, mpn='', manufacturer='', assembly='SMT', notes=''):
    return dict(zip(FIELDS, [qty, refs, footprint, value, '', description, value,
                            manufacturer, mpn, assembly, notes]))


smd = [
    row(5, 'C1, C2, C3, C4, C5', '0603 (1608 metric)', '100nF',
        'Ceramic capacitor; 25V minimum; X7R; +/-10%', '100nF / >=25V / X7R / 0603',
        notes='C5 is 100nF, NOT 9pF. C1-C4 values unchanged.'),
    row(1, 'C6', '0603 (1608 metric)', '1uF',
        'Ceramic capacitor; 25V minimum; X7R; +/-20%', '1uF / >=25V / X7R / 0603',
        notes='C6 is 1uF, NOT 9pF. Choose adequate effective capacitance under DC bias.'),
    row(56, ', '.join(f'D{i}' for i in range(1, 57)), 'SOT-23-3', 'BAV99',
        'Dual series switching diode; BAV99 pinout', 'BAV99',
        notes='Keep all 56 on the existing 8-cell driver PCB, even with only 4 cells installed.'),
    row(1, 'R3', '0603 (1608 metric)', '240R',
        'Resistor; 240 ohm; +/-1%; >=0.1W', '240R / 1% / 0603'),
    row(4, 'IC2, IC3, IC5, IC6', 'SOIC-16; 1.27mm pitch; ~6mm overall width', '74HC238D',
        '3-to-8 decoder with active-HIGH outputs', '74HC238D',
        notes='Do not substitute 74HC138 (active-LOW). Do not choose TSSOP.'),
    row(2, 'Q1, Q2', 'SOP-18; 1.27mm pitch; Toshiba SOP18-P-375-1.27', 'TBD62783AFG',
        '8-channel SOURCE DMOS driver', 'TBD62783AFG,EL', 'Toshiba',
        notes='Use FG package; not FNG/SSOP or PG/DIP. Pin 9=VCC, pin 10=GND.'),
    row(2, 'IC1, IC4', 'SO18 / SOP-18; 1.27mm pitch; Toshiba SOP18-P-375-1.27', 'TBD62083AFG',
        '8-channel SINK DMOS driver', 'TBD62083AFG,EL', 'Toshiba',
        notes='Authors build log specifies TBD62083AFG. Eagle symbol was labelled TD62083. Pin 9=GND, pin 10=COMMON; verified against Toshiba datasheet.'),
    row(1, 'U2', 'SOT-223', 'LM317',
        'Adjustable positive linear regulator; pin 1=ADJ, 2=OUT, 3=IN; tab=OUT',
        'LM317AEMP/NOPB', 'Texas Instruments',
        notes='Selected LM317A SOT-223 variant. Pin 1=ADJ, 2=OUT, 3=IN; tab=OUT. Current is limited by thermal dissipation on this PCB; do not buy TO-220 or SOIC variant.'),
]

manual = [
    row(1, 'R1', '3362P', '1k', 'Single-turn through-hole trimmer; 1 kohm',
        '3362P-1-102LF', 'Bourns', 'THT / hand solder',
        'Footprint: outer pins 5.08mm apart, wiper offset 2.54mm; do not choose 3362W variant.'),
    row(2, 'J2, J3', '1X02; 2.54mm pitch', '2-pin header',
        'Straight 1x2 through-hole header; optional V_DRIVE/GND breakout',
        '1x2 / 2.54mm pitch', assembly='THT / hand solder',
        notes='J2 was missing from original BOM. Can leave both unpopulated if breakout not needed.'),
    row(1, 'J1', 'POWER_JACK_SLOT', 'DC barrel jack',
        'Through-hole barrel jack matching existing 3 round-hole footprint',
        'Match footprint drawing; 9V supply plug should match jack', assembly='THT / hand solder',
        notes='Do not select by barrel diameter alone. Footprint drawing included; terminal holes are round, 1.0mm.'),
    row(1, 'U$9', 'NANO; two 1x15 rows, 2.54mm pitch, 15.24mm row spacing', 'Arduino Nano',
        'Classic 5V ATmega328P Arduino Nano-compatible module',
        'Classic Arduino Nano 5V / ATmega328P', assembly='Module / hand solder',
        notes='Nano Every / Nano 33 / ESP32 boards are not automatic substitutes.'),
    row(8, 'U$1-U$4: two sockets per cell', '2x3; 1.27mm pitch in both directions', 'Female socket',
        'Female through-hole sockets for 4 active cells, two sockets per cell',
        '2x3 / 1.27mm pitch / mating to male cell headers', assembly='THT / hand solder',
        notes='U$5-U$8 remain unpopulated. For all 8 cells, use 16 sockets instead. Confirm mating height.'),
]

cells = [
    row(4, 'One per cell', '7.620 x 29.718mm; 2-layer', 'Braille Cell PCB',
        'Small bare PCB; use new Braille-Cell-Gerbers.zip', assembly='PCB fabrication'),
    row(8, 'Two per cell', '2x3; 1.27mm pitch in both directions', 'Male header',
        'Straight male through-hole headers; 8 pieces for 4 cells',
        'HPH2-B-06-UA or dimensionally matching header', 'Adam Tech / equivalent', 'Hand solder',
        'Header pin must fit finished 0.60mm holes; match sockets. This is not a battery/JST header.'),
    row(24, 'Six per cell', 'Diameter 1mm x length 10mm', 'Ferrite rod',
        'Uncoated Fair-Rite material 67 ferrite rod', '3067990831', 'Fair-Rite', 'Manual coil assembly'),
    row(24, 'Six per cell', 'Diameter 1mm x thickness 0.5mm', 'NdFeB N52 magnet',
        'Disc micromagnets; assemble all with consistent polarity',
        'NdFeB N52 / 1.0 x 0.5mm', assembly='Manual assembly',
        notes='24 needed; 20 magnets are insufficient for 4 cells. Buy spares separately if desired.'),
    row(24, 'Six per cell', 'Custom wound on 1mm ferrite core', 'Solenoid coil',
        'Wind with 0.05mm enamel-insulated copper wire',
        'Wire diameter 50um / 0.05mm; custom winding', assembly='Manual winding',
        notes='24 coils; winding-turn count/resistance not specified by author, so not invented here.'),
    row(24, 'Six per cell', 'Braille Cam, V12 CAD', 'Printed cam',
        '3D printed cam', assembly='3D print / manual'),
    row(24, 'Six per cell', 'Braille Dot, V12 CAD', 'Printed dot',
        '3D printed dot', assembly='3D print / manual'),
    row(4, 'One per cell', 'Braille Upper, V12 CAD', 'Printed upper',
        '3D printed upper body', assembly='3D print / manual'),
    row(4, 'One per cell', 'Braille Lower, V12 CAD', 'Printed lower',
        '3D printed lower body', assembly='3D print / manual'),
]


def write(name, rows):
    with (OUT / name).open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, FIELDS)
        w.writeheader()
        w.writerows(rows)


write('Evaluation-BOM-SMD.csv', smd)
write('Evaluation-BOM-Hand-Assembly.csv', manual)
write('Evaluation-BOM-Corrected.csv', smd + manual)
write('Four-Cells-BOM.csv', cells)

original_csv = next((ROOT.parent / 'pcb-audit' / 'extracted').rglob('*Top Centroid.csv'))
with original_csv.open(newline='', encoding='utf-8-sig') as f:
    positions = list(csv.DictReader(f))
expected = {r.strip() for part in smd for r in part['Designator'].split(',')}
actual = {r['Designator'] for r in positions}
assert actual == expected, {'missing': expected - actual, 'extra': actual - expected}
assert sum(r['Qty'] for r in smd) == 72 == len(positions)
(ROOT / 'verification' / 'bom-verification.json').write_text(json.dumps({
    'large_boards': 1, 'small_boards': 4, 'active_cell_positions': ['U$1', 'U$2', 'U$3', 'U$4'],
    'SMD_component_count': 72, 'SMD_centroid_designators_exactly_match': True,
    'cell_male_headers': 8, 'evaluation_female_sockets_for_4_cells': 8,
    'ferrite_rods': 24, 'magnets': 24, 'coils': 24,
    'LCSC_part_numbers': 'Not guessed; supplier-specific selection remains',
}, indent=2))
print('Wrote four BOMs; 72 SMD references exactly match original centroid.')
