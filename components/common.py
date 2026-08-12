from manim import *
from config import *


def safe_text(text, size=BODY_FONT_SIZE, color=INK, weight=NORMAL):
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)


def chapter_header(chapter_no, title, tech, color):
    bar = RoundedRectangle(corner_radius=0.18, width=13.3, height=1.15,
                           fill_color=color, fill_opacity=1, stroke_opacity=0)
    left = safe_text(chapter_no, 24, WHITE, BOLD)
    mid = safe_text(title, 34, WHITE, BOLD)
    right = safe_text(tech, 22, WHITE)
    left.move_to(bar.get_left() + RIGHT*0.65)
    mid.move_to(bar.get_center() + LEFT*1.0)
    right.move_to(bar.get_right() + LEFT*1.7)
    return VGroup(bar, left, mid, right)


class Person(VGroup):
    def __init__(self, name, shirt=BLUE, hair="#3B2F2F", gender="m", scale=1.0):
        super().__init__()
        head = Circle(radius=0.38, fill_color="#FFD8B4", fill_opacity=1, stroke_color=INK, stroke_width=2)
        hair_shape = Arc(radius=0.39, start_angle=0.15, angle=PI-0.3, color=hair, stroke_width=14)
        hair_shape.shift(UP*0.09)
        body = RoundedRectangle(corner_radius=0.16, width=0.9, height=0.72,
                                fill_color=shirt, fill_opacity=1, stroke_color=INK, stroke_width=2)
        body.next_to(head, DOWN, buff=0.02)
        eye_l = Dot(head.get_center()+LEFT*0.13+UP*0.03, radius=0.025, color=INK)
        eye_r = Dot(head.get_center()+RIGHT*0.13+UP*0.03, radius=0.025, color=INK)
        mouth = Arc(radius=0.12, start_angle=PI+0.25, angle=PI-0.5, color=RED, stroke_width=2)
        mouth.move_to(head.get_center()+DOWN*0.12)
        label = safe_text(name, 18, INK, BOLD).next_to(body, DOWN, buff=0.08)
        self.add(body, head, hair_shape, eye_l, eye_r, mouth, label)
        self.scale(scale)
        self.body = body
        self.head = head
        self.name_label = label

    def speech(self, text, direction=RIGHT):
        bubble = RoundedRectangle(corner_radius=0.15, width=max(2.1, len(text)*0.25), height=0.7,
                                  fill_color=WHITE, fill_opacity=1, stroke_color=GRAY, stroke_width=2)
        bubble.next_to(self, direction, buff=0.25)
        label = safe_text(text, 18, INK).move_to(bubble)
        return VGroup(bubble, label)


class Server(VGroup):
    def __init__(self, label, accent=BLUE, width=1.2, height=1.55):
        super().__init__()
        rack = RoundedRectangle(corner_radius=0.12, width=width, height=height,
                                fill_color="#25324A", fill_opacity=1, stroke_color=accent, stroke_width=2)
        slots = VGroup()
        for y in [0.38, 0.05, -0.28]:
            line = RoundedRectangle(corner_radius=0.04, width=width*0.72, height=0.18,
                                    fill_color="#3D4D6B", fill_opacity=1, stroke_opacity=0)
            line.move_to(rack.get_center()+UP*y)
            led = Dot(line.get_right()+LEFT*0.09, radius=0.025, color=GREEN)
            slots.add(line, led)
        text = safe_text(label, 18, INK, BOLD).next_to(rack, DOWN, buff=0.1)
        self.add(rack, slots, text)


class Packet(VGroup):
    def __init__(self, label, color=BLUE, lock=False):
        super().__init__()
        box = RoundedRectangle(corner_radius=0.08, width=1.4, height=0.55,
                               fill_color=color, fill_opacity=0.12, stroke_color=color, stroke_width=2)
        txt = safe_text(label, 16, color, BOLD).move_to(box)
        self.add(box, txt)
        if lock:
            shackle = Arc(radius=0.13, start_angle=0, angle=PI, color=color, stroke_width=3)
            shackle.move_to(box.get_right()+LEFT*0.18+UP*0.12)
            lock_body = Square(side_length=0.18, fill_color=color, fill_opacity=1, stroke_opacity=0)
            lock_body.move_to(box.get_right()+LEFT*0.18+DOWN*0.02)
            self.add(shackle, lock_body)


class NATWall(VGroup):
    def __init__(self, label="NAT / Firewall"):
        super().__init__()
        bricks = VGroup()
        bw, bh = 0.42, 0.22
        for r in range(5):
            cols = 3
            for c in range(cols):
                brick = Rectangle(width=bw, height=bh, fill_color="#B75A3C", fill_opacity=1,
                                  stroke_color="#7A3426", stroke_width=1)
                brick.shift(RIGHT*((c-1)*bw + (0.21 if r%2 else 0)) + UP*((r-2)*bh))
                bricks.add(brick)
        label_obj = safe_text(label, 15, RED, BOLD).next_to(bricks, DOWN, buff=0.08)
        self.add(bricks, label_obj)


class InfoCard(VGroup):
    def __init__(self, title, lines, accent=BLUE, width=3.7):
        super().__init__()
        h = 0.75 + len(lines)*0.36
        box = RoundedRectangle(corner_radius=0.14, width=width, height=h,
                               fill_color=WHITE, fill_opacity=1, stroke_color=accent, stroke_width=2)
        ttl = safe_text(title, 19, accent, BOLD)
        ttl.move_to(box.get_top()+DOWN*0.28)
        content = VGroup(*[safe_text(line, 16, INK) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        content.next_to(ttl, DOWN, buff=0.18).align_to(box, LEFT).shift(RIGHT*0.22)
        self.add(box, ttl, content)


def arrow_between(a, b, color=BLUE, buff=0.15, dashed=False, width=4):
    if dashed:
        return DashedLine(a.get_right(), b.get_left(), color=color, stroke_width=width, buff=buff)
    return Arrow(a.get_right(), b.get_left(), color=color, stroke_width=width, buff=buff, max_tip_length_to_length_ratio=0.15)


def metric_box(label, value, accent=ORANGE):
    box = RoundedRectangle(corner_radius=0.12, width=2.2, height=0.85,
                           fill_color=WHITE, fill_opacity=1, stroke_color=accent, stroke_width=2)
    l = safe_text(label, 15, GRAY).move_to(box.get_top()+DOWN*0.20)
    v = safe_text(value, 22, accent, BOLD).move_to(box.get_bottom()+UP*0.27)
    return VGroup(box, l, v)
