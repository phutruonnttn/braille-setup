EDITABLE PCB SOURCE FILES — KiCad 10.0.6

Two independent PCB designs:
1. Braille-Cell.kicad_pcb — small cell, 7.620 x 29.718 mm.
2. Braille-Evaluation.kicad_pcb — large driver, 98.01225 x 89.6112 mm.

These are native EDITABLE BOARD files, not Gerbers. Open in KiCad PCB Editor.
Keep the matching .kicad_pro and .kicad_dru next to each .kicad_pcb when running DRC.
Each board contains its own pads/footprints; no external footprint library is
needed merely to open the layout or plot the existing board.

Checked copper clearance: 0.1524 mm (6 mil). Edge clearance 0.30 mm.
Hole-to-copper clearance 0.20 mm. Nominal thickness 1.6 mm.
Preserve 0.025 mm local soldermask margin at the 1.27 mm headers.
Small board: 12 coil PTH solder terminals must remain exposed on both masks;
three other routing vias are tented. Export PTH and NPTH drills separately.

Use the stored auxiliary origin for Gerber/drill/placement exports:
small PCB: Eagle/KiCad X=-20.320, KiCad Y=9.779 mm.
large PCB: X=6.53415, KiCad Y=-2.4892 mm.
The regenerated large-board centroid uses that same fabrication origin.
Do not combine a new origin with the old centroid. Do not scale the board.

Route by the CENTERLINE of Edge.Cuts; its stroke width is 0.2032 mm.
If KiCad job metadata includes stroke width in Size, nominal outline sizes
are those listed above. Manufacturing quantity is supplied separately.

Prior DRC check: zero error-level violations and zero missing connections
for both boards with these project rules. Large board retains cosmetic silk
warnings and one one-layer via warning. PCB small has zero warnings.
These copies are byte-identical to the checked source boards.
No schematic is included; this is a PCB-layout handoff.

Software format: KiCad 10 (.kicad_pcb), not Eagle (.brd) or Altium (.PcbDoc).
Changing the extension does NOT convert between these formats.
