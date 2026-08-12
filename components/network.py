from manim import *
from config import *
from components.common import safe_text


def moving_packet(scene, packet, path, run_time=1.2):
    scene.play(MoveAlongPath(packet, path), run_time=run_time, rate_func=linear)


def pulse_line(scene, line, color=GREEN):
    glow = line.copy().set_color(color).set_stroke(width=8, opacity=0.65)
    scene.play(Create(glow), run_time=0.35)
    scene.play(FadeOut(glow), run_time=0.25)


def topology_node(label, color=BLUE, radius=0.25):
    c = Circle(radius=radius, fill_color=color, fill_opacity=0.15, stroke_color=color, stroke_width=2)
    t = safe_text(label, 14, color, BOLD).move_to(c)
    return VGroup(c, t)
