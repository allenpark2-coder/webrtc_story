from manim import *
from config import *
from components.common import *
from components.network import topology_node

class Chapter5Topologies(Scene):
    def construct(self):
        self.camera.background_color = BG
        header = chapter_header(*CHAPTERS[4]).to_edge(UP, buff=0.2)
        self.play(FadeIn(header, shift=DOWN))

        title_mesh = safe_text("1. Mesh：每個人互連", 25, PURPLE, BOLD).shift(UP*2.1)
        self.play(FadeIn(title_mesh))
        pts = [LEFT*3+UP*0.9, RIGHT*3+UP*0.9, LEFT*3+DOWN*1.1, RIGHT*3+DOWN*1.1]
        nodes = VGroup(*[topology_node(str(i+1), PURPLE, 0.3).move_to(p) for i,p in enumerate(pts)])
        lines = VGroup()
        for i in range(4):
            for j in range(i+1,4):
                lines.add(Line(nodes[i].get_center(), nodes[j].get_center(), color=PURPLE, stroke_width=2))
        self.play(FadeIn(nodes), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.08))
        warn = safe_text("人數增加 → 上傳連線數快速增加", 20, RED, BOLD).shift(DOWN*2.0)
        self.play(FadeIn(warn))
        self.wait(0.5)
        self.play(FadeOut(nodes), FadeOut(lines), FadeOut(title_mesh), FadeOut(warn))

        title_sfu = safe_text("2. SFU：每人上傳一份，由伺服器選擇性轉發", 24, BLUE, BOLD).shift(UP*2.2)
        sfu = Server("SFU", BLUE, 1.25, 1.45).move_to(ORIGIN)
        left_nodes = VGroup(*[topology_node(f"U{i+1}", BLUE, 0.28).shift(LEFT*4+UP*(1.2-i*1.2)) for i in range(3)])
        right_nodes = VGroup(*[topology_node(f"U{i+4}", BLUE, 0.28).shift(RIGHT*4+UP*(1.2-i*1.2)) for i in range(3)])
        self.play(FadeIn(title_sfu), GrowFromCenter(sfu), FadeIn(left_nodes), FadeIn(right_nodes))
        uplinks = VGroup(*[Arrow(n.get_right(), sfu.get_left(), color=BLUE, buff=0.1, stroke_width=2) for n in left_nodes])
        downlinks = VGroup(*[Arrow(sfu.get_right(), n.get_left(), color=BLUE, buff=0.1, stroke_width=2) for n in right_nodes])
        self.play(LaggedStart(*[Create(a) for a in uplinks], lag_ratio=0.15), LaggedStart(*[Create(a) for a in downlinks], lag_ratio=0.15))
        good = safe_text("主流多人會議：伺服器不必解碼混畫面，延遲較低、可做 simulcast/SVC 選層", 18, BLUE)
        good.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(good))
        self.wait(0.7)
        self.play(FadeOut(title_sfu), FadeOut(sfu), FadeOut(left_nodes), FadeOut(right_nodes), FadeOut(uplinks), FadeOut(downlinks), FadeOut(good))

        title_mcu = safe_text("3. MCU：伺服器解碼、混合、再編碼", 25, ORANGE, BOLD).shift(UP*2.2)
        mcu = Server("MCU", ORANGE, 1.35, 1.5).move_to(ORIGIN)
        users = VGroup(*[topology_node(f"U{i+1}", ORANGE, 0.28).shift(LEFT*4+UP*(1.2-i*1.2)) for i in range(3)])
        mixed = RoundedRectangle(corner_radius=0.12, width=2.2, height=1.35, fill_color=LIGHT_ORANGE, fill_opacity=1, stroke_color=ORANGE)
        mixed.shift(RIGHT*3.8)
        mixed_text = safe_text("混合畫面\nComposite", 20, ORANGE, BOLD).move_to(mixed)
        self.play(FadeIn(title_mcu), GrowFromCenter(mcu), FadeIn(users), FadeIn(mixed), FadeIn(mixed_text))
        ins = VGroup(*[Arrow(n.get_right(), mcu.get_left(), color=ORANGE, buff=0.1, stroke_width=2) for n in users])
        out = Arrow(mcu.get_right(), mixed.get_left(), color=ORANGE, buff=0.1, stroke_width=3)
        self.play(LaggedStart(*[Create(a) for a in ins], lag_ratio=0.15), Create(out))
        note = safe_text("優點：接收端簡單；缺點：伺服器 CPU/GPU 成本高、通常延遲也更高。", 18, ORANGE)
        note.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(note))
        self.wait(0.8)

        self.play(FadeOut(*self.mobjects))
        summary = safe_text("WebRTC 核心旅程", 40, INK, BOLD).shift(UP*2.2)
        flow = VGroup(
            safe_text("Signaling / SDP", 22, PURPLE, BOLD),
            safe_text("→ ICE / STUN / TURN", 22, BLUE, BOLD),
            safe_text("→ DTLS", 22, GREEN, BOLD),
            safe_text("→ SRTP", 22, GREEN, BOLD),
            safe_text("→ ABR / Congestion Control", 22, ORANGE, BOLD),
            safe_text("→ Mesh / SFU / MCU", 22, PURPLE, BOLD),
        ).arrange(DOWN, buff=0.22)
        self.play(FadeIn(summary), LaggedStart(*[FadeIn(x, shift=UP) for x in flow], lag_ratio=0.18))
        end = safe_text("從『找到彼此』，到『安全地傳』，再到『多人規模化』。", 25, INK, BOLD).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(end))
        self.wait(1.5)
