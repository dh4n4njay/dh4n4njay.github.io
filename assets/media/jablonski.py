"""Animated Jablonski diagrams for dh4n4njay.github.io — site palette.

Three scenes: Fluorescence, Phosphorescence, TADF.
Render (from this directory, with manim installed):
    manim -qm --fps 30 jablonski.py Fluorescence
    manim -qm --fps 30 jablonski.py Phosphorescence
    manim -qm --fps 30 jablonski.py TADF
Each scene ends in its starting state, so the videos loop cleanly.
"""
from manim import *

BG = "#070b14"
TEXTC = "#e6ecf5"
MUTED = "#8ea3b8"
EMISSION = "#3ce88f"     # fluorescence
EXCITATION = "#7c6cf0"   # absorption
IC_COLOR = "#e8b84a"     # radiationless processes (IC / VR / ISC / RISC)
PHOS = "#f2884b"         # phosphorescence

config.background_color = BG
config.pixel_width = 840
config.pixel_height = 840
config.frame_width = 8.4
config.frame_height = 8.4

FONT = "DejaVu Sans"


def level(y, x0, x1, main=True):
    return Line(
        [x0, y, 0], [x1, y, 0],
        color=TEXTC if main else MUTED,
        stroke_width=3.5 if main else 1.6,
        stroke_opacity=1 if main else 0.55,
    )


def vib_stack(y, x0, x1, n=2, gap=0.3):
    return VGroup(*[level(y + gap * (i + 1), x0, x1, main=False) for i in range(n)])


def zigzag(p0, p1, steps=6, amp=0.14):
    """Radiationless-transition path between two points."""
    path = VMobject(color=IC_COLOR, stroke_width=3.5)
    pts = [list(p0) + [0]]
    for i in range(1, steps):
        xx = p0[0] + (p1[0] - p0[0]) * i / steps
        yy = p0[1] + (p1[1] - p0[1]) * i / steps
        pts.append([xx, yy + (amp if i % 2 else -amp), 0])
    pts.append(list(p1) + [0])
    path.set_points_as_corners(pts)
    return path


def title(text):
    t = Text(text, font=FONT, font_size=26, color=MUTED)
    t.to_edge(UP, buff=0.35)
    return t


def slabel(txt, mobj, direction=LEFT):
    t = Text(txt, font=FONT, font_size=28, color=TEXTC)
    t.next_to(mobj, direction, buff=0.28)
    return t


class Fluorescence(Scene):
    def construct(self):
        x0, x1 = -2.6, 2.6
        s0_y, s1_y, s2_y = -3.1, 0.4, 2.2

        s0, s1, s2 = level(s0_y, x0, x1), level(s1_y, x0, x1), level(s2_y, x0, x1)
        self.add(s0, vib_stack(s0_y, x0, x1, n=3), s1, vib_stack(s1_y, x0, x1),
                 s2, vib_stack(s2_y, x0, x1, n=1),
                 slabel("S₀", s0), slabel("S₁", s1), slabel("S₂", s2),
                 title("Fluorescence"))

        abs_x, fl_x = -1.5, 1.5
        s2_top = s2_y + 0.3
        electron = Dot([abs_x, s0_y, 0], radius=0.09, color=EXCITATION)
        self.add(electron)

        absorption = Arrow([abs_x, s0_y, 0], [abs_x, s2_top, 0], color=EXCITATION,
                           buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.06)
        abs_label = Text("Absorption", font=FONT, font_size=22, color=EXCITATION)
        abs_label.rotate(PI / 2).next_to(absorption, LEFT, buff=0.18)

        ic = zigzag([abs_x, s2_top], [0.0, s1_y])
        ic_label = Text("IC / VR", font=FONT, font_size=20, color=IC_COLOR)
        ic_label.next_to(ic.get_center(), UR, buff=0.2)

        fluor = Arrow([fl_x, s1_y, 0], [fl_x, s0_y + 0.3, 0], color=EMISSION,
                      buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.06)
        fl_label = Text("Fluorescence", font=FONT, font_size=22, color=EMISSION)
        fl_label.rotate(PI / 2).next_to(fluor, RIGHT, buff=0.18)

        hv_in = Text("hν", font=FONT, font_size=24, color=EXCITATION)
        hv_in.next_to([abs_x, s0_y, 0], DL, buff=0.22)
        hv_out = Text("hν′", font=FONT, font_size=24, color=EMISSION)
        hv_out.next_to([fl_x, s0_y + 0.3, 0], DR, buff=0.22)
        flash = Circle(radius=0.32, color=EMISSION, stroke_width=4).move_to([fl_x, s0_y + 0.3, 0])

        self.play(FadeIn(hv_in, scale=0.6), run_time=0.5)
        self.play(GrowArrow(absorption), electron.animate.move_to([abs_x, s2_top, 0]),
                  FadeIn(abs_label), run_time=1.0)
        self.play(FadeOut(hv_in), run_time=0.3)
        self.play(Create(ic), MoveAlongPath(electron, ic), FadeIn(ic_label),
                  run_time=1.4, rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)
        self.play(GrowArrow(fluor), electron.animate.move_to([fl_x, s0_y + 0.3, 0]),
                  FadeIn(fl_label), run_time=0.8)
        self.play(Broadcast(flash, focal_point=[fl_x, s0_y + 0.3, 0], n_mobs=2, run_time=1.0),
                  FadeIn(hv_out, scale=0.6))
        self.wait(0.6)
        self.play(FadeOut(absorption), FadeOut(abs_label), FadeOut(ic), FadeOut(ic_label),
                  FadeOut(fluor), FadeOut(fl_label), FadeOut(hv_out),
                  electron.animate.move_to([abs_x, s0_y, 0]), run_time=0.9)
        self.wait(0.4)


class SingletTripletBase(Scene):
    """Shared S0 / S1 / T1 frame for phosphorescence and TADF."""

    T1_Y = 0.3

    def build_frame(self, heading, subtitle=None, t1_label_below=False):
        self.s0_y, self.s1_y, self.t1_y = -3.1, 1.4, self.T1_Y
        sx0, sx1 = -3.2, -0.4   # singlet block (S1)
        tx0, tx1 = 0.5, 3.3     # triplet block (T1)
        gx0, gx1 = -3.2, 3.3    # ground state spans both

        s0 = level(self.s0_y, gx0, gx1)
        s1 = level(self.s1_y, sx0, sx1)
        t1 = level(self.t1_y, tx0, tx1)
        t1_label = Text("T₁", font=FONT, font_size=28, color=TEXTC)
        if t1_label_below:
            t1_label.next_to(t1.get_end(), DOWN, buff=0.22).shift(LEFT * 0.15)
        else:
            t1_label.next_to(t1, RIGHT, buff=0.28)
        head = title(heading)
        self.add(s0, vib_stack(self.s0_y, gx0, gx1, n=2), s1, vib_stack(self.s1_y, sx0, sx1, n=1),
                 t1, vib_stack(self.t1_y, tx0, tx1, n=1),
                 slabel("S₀", s0), slabel("S₁", s1), t1_label, head)
        if subtitle:
            sub = Text(subtitle, font=FONT, font_size=17, color=MUTED)
            sub.next_to(head, DOWN, buff=0.14)
            self.add(sub)
        self.sx1, self.tx0 = sx1, tx0
        self.abs_x = -2.5

    def absorb(self):
        electron = Dot([self.abs_x, self.s0_y, 0], radius=0.09, color=EXCITATION)
        self.add(electron)
        absorption = Arrow([self.abs_x, self.s0_y, 0], [self.abs_x, self.s1_y, 0],
                           color=EXCITATION, buff=0, stroke_width=5,
                           max_tip_length_to_length_ratio=0.05)
        abs_label = Text("Absorption", font=FONT, font_size=22, color=EXCITATION)
        abs_label.rotate(PI / 2).next_to(absorption, LEFT, buff=0.18)
        hv_in = Text("hν", font=FONT, font_size=24, color=EXCITATION)
        hv_in.next_to([self.abs_x, self.s0_y, 0], DL, buff=0.22)

        self.play(FadeIn(hv_in, scale=0.6), run_time=0.5)
        self.play(GrowArrow(absorption), electron.animate.move_to([self.abs_x, self.s1_y, 0]),
                  FadeIn(abs_label), run_time=1.0)
        self.play(FadeOut(hv_in), run_time=0.3)
        return electron, VGroup(absorption, abs_label)


class Phosphorescence(SingletTripletBase):
    def construct(self):
        self.build_frame("Phosphorescence")
        electron, used = self.absorb()

        isc = zigzag([self.sx1, self.s1_y], [self.tx0 + 0.3, self.t1_y], steps=5)
        isc_label = Text("ISC", font=FONT, font_size=22, color=IC_COLOR)
        isc_label.next_to(isc.get_center(), UP, buff=0.3)

        self.play(Create(isc), MoveAlongPath(electron, isc), FadeIn(isc_label),
                  run_time=1.3, rate_func=rate_functions.ease_in_out_sine)

        slow = Text("long-lived (µs–s)", font=FONT, font_size=18, color=MUTED)
        slow.next_to([self.tx0 + 1.4, self.t1_y, 0], UP, buff=0.55)
        self.play(FadeIn(slow), run_time=0.5)
        self.wait(1.0)

        ph_x = 2.6
        phos = Arrow([ph_x, self.t1_y, 0], [ph_x, self.s0_y + 0.3, 0], color=PHOS,
                     buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.06)
        ph_label = Text("Phosphorescence", font=FONT, font_size=22, color=PHOS)
        ph_label.rotate(PI / 2).next_to(phos, RIGHT, buff=0.18)
        hv_out = Text("hν″", font=FONT, font_size=24, color=PHOS)
        hv_out.next_to([ph_x, self.s0_y, 0], DL, buff=0.2)
        flash = Circle(radius=0.32, color=PHOS, stroke_width=4).move_to([ph_x, self.s0_y + 0.3, 0])

        self.play(GrowArrow(phos), electron.animate.move_to([ph_x, self.s0_y + 0.3, 0]),
                  FadeIn(ph_label), run_time=1.0)
        self.play(Broadcast(flash, focal_point=[ph_x, self.s0_y + 0.3, 0], n_mobs=2, run_time=1.0),
                  FadeIn(hv_out, scale=0.6))
        self.wait(0.5)
        self.play(FadeOut(used), FadeOut(isc), FadeOut(isc_label), FadeOut(slow),
                  FadeOut(phos), FadeOut(ph_label), FadeOut(hv_out),
                  electron.animate.move_to([self.abs_x, self.s0_y, 0]), run_time=0.9)
        self.wait(0.4)


class TADF(SingletTripletBase):
    T1_Y = 0.55  # small singlet–triplet gap is the point of TADF

    def construct(self):
        self.build_frame("TADF", subtitle="thermally activated delayed fluorescence",
                         t1_label_below=True)

        # ΔEST bracket on the far right
        gap_x = 3.55
        gap = DoubleArrow([gap_x, self.t1_y, 0], [gap_x, self.s1_y, 0], buff=0,
                          color=MUTED, stroke_width=2.5, tip_length=0.14)
        gap_label = Text("ΔEST", font=FONT, font_size=18, color=MUTED)
        gap_label.next_to(gap, UP, buff=0.12)
        self.add(gap, gap_label)

        electron, used = self.absorb()

        mid_x = (self.sx1 + self.tx0) / 2
        isc = ArcBetweenPoints([self.sx1, self.s1_y, 0], [self.tx0 + 0.2, self.t1_y, 0],
                               angle=0.9, color=IC_COLOR, stroke_width=3.5)
        isc_label = Text("ISC", font=FONT, font_size=20, color=IC_COLOR)
        isc_label.next_to([mid_x, (self.s1_y + self.t1_y) / 2 - 0.35, 0], DOWN, buff=0.15)

        self.play(Create(isc), MoveAlongPath(electron, isc), FadeIn(isc_label),
                  run_time=1.2, rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.6)

        risc = ArcBetweenPoints([self.tx0 + 0.2, self.t1_y, 0], [self.sx1, self.s1_y, 0],
                                angle=0.9, color=IC_COLOR, stroke_width=3.5)
        risc_label = Text("RISC (heat)", font=FONT, font_size=20, color=IC_COLOR)
        risc_label.next_to([mid_x, (self.s1_y + self.t1_y) / 2 + 0.35, 0], UP, buff=0.15)

        self.play(Create(risc), MoveAlongPath(electron, risc), FadeIn(risc_label),
                  run_time=1.2, rate_func=rate_functions.ease_in_out_sine)

        fl_x = -1.4
        fluor = Arrow([fl_x, self.s1_y, 0], [fl_x, self.s0_y + 0.3, 0], color=EMISSION,
                      buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.05)
        fl_label = Text("Delayed fluorescence", font=FONT, font_size=22, color=EMISSION)
        fl_label.rotate(PI / 2).next_to(fluor, RIGHT, buff=0.18)
        hv_out = Text("hν′", font=FONT, font_size=24, color=EMISSION)
        hv_out.next_to([fl_x, self.s0_y, 0], DL, buff=0.2)
        flash = Circle(radius=0.32, color=EMISSION, stroke_width=4).move_to([fl_x, self.s0_y + 0.3, 0])

        self.play(GrowArrow(fluor), electron.animate.move_to([fl_x, self.s0_y + 0.3, 0]),
                  FadeIn(fl_label), run_time=0.9)
        self.play(Broadcast(flash, focal_point=[fl_x, self.s0_y + 0.3, 0], n_mobs=2, run_time=1.0),
                  FadeIn(hv_out, scale=0.6))
        self.wait(0.5)
        self.play(FadeOut(used), FadeOut(isc), FadeOut(isc_label),
                  FadeOut(risc), FadeOut(risc_label),
                  FadeOut(fluor), FadeOut(fl_label), FadeOut(hv_out),
                  electron.animate.move_to([self.abs_x, self.s0_y, 0]), run_time=0.9)
        self.wait(0.4)
