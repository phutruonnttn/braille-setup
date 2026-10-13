MANUFACTURING DATA - FINAL SUPPLIER HANDOFF

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

BOARD: Braille-Evaluation
Nominal size: 98.01225 x 89.61120 mm.
Drilling: 325 plated + 4 non-plated holes.

LARGE BOARD SPECIFIC:
The board supports up to eight Braille cells. Top silkscreen and top paste
are included. Bottom silk and bottom paste have no printed features and are
omitted. Component positions and fabrication origin are unchanged, so the
regenerated Evaluation-Top-Centroid.csv remains aligned with this Gerber set.
The source retains silk-related warnings and one one-layer via warning.
