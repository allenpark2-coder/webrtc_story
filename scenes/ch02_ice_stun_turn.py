from manim import *
from config import *
from components.common import *

class Chapter2IceStunTurn(Scene):
    def construct(self):
        self.camera.background_color = BG
        header = chapter_header(*CHAPTERS[1]).to_edge(UP, buff=0.2)
        self.play(FadeIn(header, shift=DOWN))

        ming = Person("小明", BLUE, scale=0.85).shift(LEFT*5.2+DOWN*0.5)
        mei = Person("小美", ORANGE, scale=0.85).shift(RIGHT*5.2+DOWN*0.5)
        wall_l = NATWall().shift(LEFT*3.7+DOWN*0.5)
        wall_r = NATWall().shift(RIGHT*3.7+DOWN*0.5)
        stun = Server("STUN", GREEN, 1.0, 1.25).shift(LEFT*1.1+UP*1.25)
        turn = Server("TURN", ORANGE, 1.0, 1.25).shift(RIGHT*1.1+UP*1.25)
        self.play(FadeIn(ming), FadeIn(mei), FadeIn(wall_l), FadeIn(wall_r), GrowFromCenter(stun), GrowFromCenter(turn))

        q = Packet("STUN Binding Request", GREEN).scale(0.8).move_to(ming.get_right()+RIGHT*0.4)
        self.play(FadeIn(q))
        self.play(MoveAlongPath(q, Line(q.get_center(), stun.get_bottom(), color=GREEN)), run_time=1.0)
        reply = Packet("203.0.113.8:62000", GREEN).scale(0.8).move_to(stun.get_bottom())
        self.play(Transform(q, reply))
        self.play(MoveAlongPath(q, Line(q.get_center(), ming.get_top()+UP*0.1, color=GREEN)), run_time=1.0)

        srflx = safe_text("Server Reflexive Candidate\n= 外界看到的我", 18, GREEN, BOLD).next_to(ming, UP, buff=0.2)
        self.play(FadeOut(q), FadeIn(srflx))

        ice = InfoCard("ICE 像導航系統", [
            "Host candidate：內網地址",
            "Server reflexive：STUN 得到的外部地址",
            "Relay candidate：TURN 中繼地址",
            "ICE 會測試 candidate pair，挑能通且成本較低的路徑",
        ], BLUE, 5.2).shift(DOWN*2.25)
        self.play(FadeIn(ice, shift=UP))

        direct = DashedLine(wall_l.get_right(), wall_r.get_left(), color=BLUE, stroke_width=5)
        direct_label = safe_text("嘗試 Direct P2P", 20, BLUE, BOLD).next_to(direct, UP, buff=0.15)
        self.play(Create(direct), FadeIn(direct_label))
        x = safe_text("✕", 46, RED, BOLD).move_to(direct.get_center())
        self.play(FadeIn(x, scale=1.4))
        fail = safe_text("對稱型 NAT / 防火牆規則 → 直連失敗", 18, RED, BOLD).next_to(direct, DOWN, buff=0.15)
        self.play(FadeIn(fail))

        relay1 = Arrow(wall_l.get_right(), turn.get_left(), color=ORANGE, stroke_width=5, buff=0.1)
        relay2 = Arrow(turn.get_right(), wall_r.get_left(), color=ORANGE, stroke_width=5, buff=0.1)
        self.play(FadeOut(x), FadeOut(fail), FadeOut(direct), FadeOut(direct_label), Create(relay1), Create(relay2))
        tag = safe_text("Relay via TURN", 21, ORANGE, BOLD).next_to(turn, DOWN, buff=0.15)
        self.play(FadeIn(tag))

        pkt = Packet("media", ORANGE).scale(0.7).move_to(wall_l.get_right())
        self.play(FadeIn(pkt), MoveAlongPath(pkt, Line(wall_l.get_right(), turn.get_left(), color=ORANGE)), run_time=0.8)
        self.play(MoveAlongPath(pkt, Line(turn.get_right(), wall_r.get_left(), color=ORANGE)), run_time=0.8)
        self.play(FadeOut(pkt))
        self.wait(1.2)
