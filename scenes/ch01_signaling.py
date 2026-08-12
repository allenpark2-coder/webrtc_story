from manim import *
from config import *
from components.common import *

class Chapter1Signaling(Scene):
    def construct(self):
        self.camera.background_color = BG
        header = chapter_header(*CHAPTERS[0]).to_edge(UP, buff=0.2)
        self.play(FadeIn(header, shift=DOWN))

        ming = Person("小明", BLUE, scale=1.0).shift(LEFT*5+DOWN*0.6)
        mei = Person("小美", ORANGE, gender="f", scale=1.0).shift(RIGHT*5+DOWN*0.6)
        signal = Server("Signaling Server", PURPLE).move_to(UP*0.2)
        self.play(FadeIn(ming), FadeIn(mei), GrowFromCenter(signal))

        b1 = ming.speech("我想和小美視訊！", RIGHT)
        b2 = mei.speech("好啊，但你在哪裡？", LEFT)
        self.play(FadeIn(b1, scale=0.8), FadeIn(b2, scale=0.8))
        self.wait(0.5)
        self.play(FadeOut(b1), FadeOut(b2))

        offer = Packet("SDP Offer", PURPLE).move_to(ming.get_right()+RIGHT*0.8+UP*0.45)
        answer = Packet("SDP Answer", PURPLE).move_to(mei.get_left()+LEFT*0.8+DOWN*0.35)
        p1 = Line(offer.get_center(), signal.get_left()+LEFT*0.05, color=PURPLE)
        self.play(FadeIn(offer), MoveAlongPath(offer, p1), run_time=1.0)
        p2 = Line(signal.get_right(), mei.get_left(), color=PURPLE)
        self.play(MoveAlongPath(offer, p2), run_time=1.0)
        self.play(FadeOut(offer))

        p3 = Line(answer.get_center(), signal.get_right(), color=PURPLE)
        self.play(FadeIn(answer), MoveAlongPath(answer, p3), run_time=1.0)
        p4 = Line(signal.get_left(), ming.get_right(), color=PURPLE)
        self.play(MoveAlongPath(answer, p4), run_time=1.0)
        self.play(FadeOut(answer))

        card = InfoCard("SDP = 通訊名片", [
            "• 我能傳 Audio / Video",
            "• Codec：H.264 / VP8 / Opus",
            "• ICE ufrag / pwd",
            "• DTLS fingerprint",
            "• 網路候選資訊可後續補上",
        ], PURPLE, 5.0).shift(DOWN*2.35)
        self.play(FadeIn(card, shift=UP))

        note = safe_text("重點：WebRTC 不規定你要用哪種 Signaling Server；它只需要雙方能交換 SDP / ICE 資訊。", 19, INK)
        note.to_edge(DOWN, buff=0.15)
        self.play(Write(note))
        self.wait(1.2)
