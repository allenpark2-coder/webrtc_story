from manim import *
from config import *
from components.common import *

class Chapter3DtlsSrtp(Scene):
    def construct(self):
        self.camera.background_color = BG
        header = chapter_header(*CHAPTERS[2]).to_edge(UP, buff=0.2)
        self.play(FadeIn(header, shift=DOWN))

        ming = Person("小明", BLUE, scale=0.9).shift(LEFT*5+DOWN*0.4)
        mei = Person("小美", ORANGE, scale=0.9).shift(RIGHT*5+DOWN*0.4)
        path = Line(ming.get_right(), mei.get_left(), color=GREEN, stroke_width=6)
        label = safe_text("ICE Connected ✓", 24, GREEN, BOLD).next_to(path, UP, buff=0.2)
        self.play(FadeIn(ming), FadeIn(mei), Create(path), FadeIn(label))

        steps = ["ClientHello", "ServerHello", "Certificate", "Fingerprint 驗證", "Finished"]
        y0 = 1.45
        arrows = VGroup()
        texts = VGroup()
        for i, s in enumerate(steps):
            y = y0 - i*0.55
            if i % 2 == 0:
                arr = Arrow(LEFT*2.8+UP*y, RIGHT*2.8+UP*y, color=GREEN, buff=0.1, stroke_width=3)
            else:
                arr = Arrow(RIGHT*2.8+UP*y, LEFT*2.8+UP*y, color=GREEN, buff=0.1, stroke_width=3)
            txt = safe_text(s, 17, INK, BOLD).next_to(arr, UP, buff=0.03)
            arrows.add(arr); texts.add(txt)
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.35),
                  LaggedStart(*[FadeIn(t) for t in texts], lag_ratio=0.35), run_time=2.2)

        key = safe_text("🔑  DTLS 建立共享金鑰", 25, GREEN, BOLD).move_to(DOWN*1.7)
        self.play(FadeIn(key, scale=1.2))

        self.play(FadeOut(arrows), FadeOut(texts), FadeOut(label))
        rtp = Packet("RTP video", BLUE, lock=False).move_to(ming.get_right()+RIGHT*0.7)
        srtp = Packet("SRTP video", GREEN, lock=True).move_to(ORIGIN)
        self.play(FadeIn(rtp))
        self.play(rtp.animate.move_to(LEFT*1.3), run_time=0.5)
        self.play(Transform(rtp, srtp))
        self.play(rtp.animate.move_to(mei.get_left()+LEFT*0.6), run_time=0.8)
        self.play(FadeOut(rtp))

        note = InfoCard("角色分工", [
            "DTLS：握手、身分/指紋驗證、導出金鑰材料",
            "SRTP：真正保護 Audio / Video RTP 封包",
            "SRTCP：保護 RTCP 控制資訊",
        ], GREEN, 5.2).shift(DOWN*2.55)
        self.play(FadeIn(note, shift=UP))
        self.wait(1.2)
