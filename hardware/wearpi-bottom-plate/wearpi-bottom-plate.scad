// wearpi – Raspberry Pi 5 bottom plate with strap slots
// Parametric OpenSCAD model. Edit the values below, then F6 + export STL.
//
// Coordinates follow the Pi 5 top view: origin at the PCB's bottom-left
// corner, GPIO header along the top edge (y = 56), USB/Ethernet at the
// right edge (x = 85), microSD card on the underside at the left edge (x = 0).
// The plate sits under the Pi: its flat face (z = 0) touches the body,
// the standoffs point up into the Pi's mounting holes.
//
// Print flat side down, standoffs up – no supports needed.
// PETG or ASA recommended for a body-worn part (PLA softens in a hot car).

/* [Pi 5 board – don't change unless you know why] */
pcb_w      = 85;     // board length (x)
pcb_h      = 56;     // board width (y)
pcb_r      = 3;      // corner radius
pcb_t      = 1.6;    // board thickness (used for screw length only)
holes      = [[3.5, 3.5], [61.5, 3.5], [3.5, 52.5], [61.5, 52.5]];
sd_y       = 28;     // centre of the microSD card along the x = 0 edge

/* [Plate] */
plate_t    = 3;      // plate thickness
edge_chamfer = 0.8;  // chamfer on the body-side edges (0 = sharp)
margin     = 0;      // grow the plate beyond the PCB outline (mm)

/* [Standoffs & screws] */
standoff_h = 4;      // gap between plate top and PCB underside
standoff_d = 6;      // stays inside the Pi's 6 mm keep-out pad
screw_d    = 2.9;    // M2.5 clearance
cb_d       = 5.6;    // counterbore for M2.5 pan/button heads (flush on the body side)
cb_depth   = 2.0;
engage_max = 4.5;    // max thread depth wanted inside the F-F spacers

/* [Strap slots] */
slots      = true;
slot_len   = 27;     // 27 fits 25 mm webbing; up to ~44 for a 40 mm belt (raise wing_w too)
slot_w     = 4;      // strap/belt thickness + ~1 mm
wing_gap   = 3;      // material between PCB edge and slot
bar_w      = 5;      // outer bar the strap wraps around
wing_w     = 39;     // wing width along y (max 56)
wing_r     = 4;

/* [microSD access] */
sd_access  = true;   // cut-out under the card so you can grip it
sd_cut_w   = 16;
sd_cut_in  = 4;      // how far the cut-out reaches under the PCB

/* [Vents] */
vents      = true;
vent_w     = 2.5;
vent_len   = 28;
vent_pitch = 6;
vent_x0    = 14;     // first vent x
vent_n     = 9;

$fn = 48;
eps = 0.01;

wing_len = wing_gap + slot_w + bar_w;

// ---------- 2D outline ----------
module rrect(x0, y0, x1, y1, r) {
    translate([x0 + r, y0 + r]) offset(r = r) square([x1 - x0 - 2*r, y1 - y0 - 2*r]);
}

module outline() {
    union() {
        rrect(-margin, -margin, pcb_w + margin, pcb_h + margin, pcb_r + margin);
        if (slots) {
            for (side = [0, 1]) {
                x0 = side == 0 ? -margin - wing_len : pcb_w + margin - wing_r*2;
                x1 = side == 0 ? -margin + wing_r*2 : pcb_w + margin + wing_len;
                rrect(x0, pcb_h/2 - wing_w/2, x1, pcb_h/2 + wing_w/2, wing_r);
            }
        }
    }
}

// ---------- plate body with body-side chamfer ----------
module plate_body() {
    if (edge_chamfer > 0) {
        minkowski() {
            linear_extrude(plate_t - edge_chamfer) offset(delta = -edge_chamfer) outline();
            cylinder(h = edge_chamfer, r1 = 0, r2 = edge_chamfer, $fn = 16);
        }
    } else {
        linear_extrude(plate_t) outline();
    }
}

module slot_cut(x) {
    translate([x, pcb_h/2 - slot_len/2, -1])
        hull() {
            translate([slot_w/2, slot_w/2]) cylinder(h = plate_t + 2, d = slot_w);
            translate([slot_w/2, slot_len - slot_w/2]) cylinder(h = plate_t + 2, d = slot_w);
        }
}

module vent_cut(x) {
    translate([x, pcb_h/2 - vent_len/2, -1])
        hull() {
            cylinder(h = plate_t + 2, d = vent_w);
            translate([0, vent_len]) cylinder(h = plate_t + 2, d = vent_w);
        }
}

module plate() {
    difference() {
        union() {
            plate_body();
            // standoffs
            for (h = holes) translate([h[0], h[1], plate_t - eps])
                cylinder(h = standoff_h + eps, d = standoff_d);
        }
        // screw holes + counterbores (body side)
        for (h = holes) translate([h[0], h[1], 0]) {
            translate([0, 0, -1]) cylinder(h = plate_t + standoff_h + 2, d = screw_d);
            translate([0, 0, -1]) cylinder(h = cb_depth + 1, d = cb_d);
        }
        // strap slots
        if (slots) {
            slot_cut(-margin - wing_gap - slot_w);
            slot_cut(pcb_w + margin + wing_gap);
        }
        // microSD access cut-out (joins the left slot when slots are on)
        if (sd_access) {
            translate([0, 0, -1]) linear_extrude(plate_t + 2)
                rrect(-margin - wing_gap - (slots ? 1 : 10), sd_y - sd_cut_w/2,
                      sd_cut_in, sd_y + sd_cut_w/2, 2);
        }
        // vents, kept clear of the standoffs
        if (vents) {
            for (i = [0 : vent_n - 1]) {
                x = vent_x0 + i * vent_pitch;
                if (x < pcb_w - 6) vent_cut(x);
            }
        }
    }
}

plate();

// ---------- screw length helper ----------
stack = (plate_t - cb_depth) + standoff_h + pcb_t;
std   = [6, 8, 10, 12, 14, 16, 18, 20];
fits  = [for (L = std) if (L - stack >= 2 && L - stack <= engage_max) L];
echo(str("Screw: material under head + standoff + PCB = ", stack, " mm"));
echo(str("Recommended: M2.5 x ", len(fits) ? fits[0] : "?", " mm (thread into spacer: ",
         len(fits) ? fits[0] - stack : "?", " mm)"));
echo(str("Overall size: ", pcb_w + 2*margin + (slots ? 2*wing_len : 0), " x ",
         pcb_h + 2*margin, " mm, height ", plate_t + standoff_h, " mm"));
