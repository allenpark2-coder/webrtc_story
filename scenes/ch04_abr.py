from manim import *
from config import *
from components.common import *

class Chapter4Abr(Scene):
    def construct(self):
        self.camera.background_color = BG
        header = chapter_header(*CHAPTERS[3]).to_edge(UP, buff=0.2)
        self.play(FadeIn(header, shift=DOWN))

        mei = Person("小美", ORANGE, scale=0.85).shift(LEFT*5+UP*0.7)
        bubble = mei.speech("咦？網路突然變慢了！", RIGHT)
        self.play(FadeIn(mei), FadeIn(bubble))

        metrics_before = VGroup(
            metric_box("可用頻寬", "5 Mbps"),
            metric_box("RTT", "50 ms"),
            metric_box("Packet loss", "1%"),
        ).arrange(RIGHT, buff=0.25).shift(UP*1.55+RIGHT*2.0)
        self.play(FadeIn(metrics_before, shift=UP))

        jam = safe_text("⚠ 網路壅塞", 28, RED, BOLD).move_to(UP*0.35+RIGHT*1.7)
        self.play(FadeIn(jam, scale=1.3))
        vals = ["1 Mbps", "220 ms", "10%"]
        metrics_after = VGroup(
            metric_box("可用頻寬", vals[0], RED),
            metric_box("RTT", vals[1], RED),
            metric_box("Packet loss", vals[2], RED),
        ).arrange(RIGHT, buff=0.25).move_to(metrics_before)
        self.play(Transform(metrics_before, metrics_after))

        controller = InfoCard("ABR / Congestion Controller", [
            "觀察：RTT、loss、transport feedback / TWCC 等",
            "估計：目前可安全使用的 bitrate",
            "調整：encoder bitrate / resolution / FPS / layer",
            "目標：畫質下降一點，但延遲不要爆掉",
        ], ORANGE, 5.6).shift(DOWN*1.15+RIGHT*2.7)
        self.play(FadeIn(controller, shift=LEFT))

        ladder = VGroup(
            safe_text("1080p · 30 fps · 4 Mbps", 18, INK),
            safe_text("720p · 30 fps · 2 Mbps", 18, INK),
            safe_text("720p · 15 fps · 1.2 Mbps", 18, INK),
            safe_text("480p · 15 fps · 0.6 Mbps", 18, GREEN, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).shift(LEFT*3.7+DOWN*1.8)
        title = safe_text("自適應畫質階梯", 20, ORANGE, BOLD).next_to(ladder, UP, buff=0.2)
        self.play(FadeIn(title), LaggedStart(*[FadeIn(x, shift=RIGHT) for x in ladder], lag_ratio=0.25))

        note = safe_text("註：Mamba 可視為特定 ABR / 頻寬控制方法之一；它不是 WebRTC 標準本身。", 18, GRAY)
        note.to_edge(DOWN, buff=0.15)
        self.play(FadeIn(note))
        self.wait(1.3)
