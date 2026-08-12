# 小明與小美的 WebRTC 視訊通話之旅

一套可直接渲染的 Manim 五章 WebRTC 教學動畫。核心目的不是「讓 PPT 動起來」，而是把生活故事與真實協定流程同步呈現。

## 五章

1. **Signaling & SDP** — 小明與小美透過信令伺服器交換 SDP Offer / Answer。
2. **ICE / STUN / TURN** — NAT 後的兩端先用 STUN 得到外部位址，ICE 測試 candidate pair，必要時走 TURN relay。
3. **DTLS & SRTP** — ICE Connected 後做 DTLS handshake，導出金鑰，再用 SRTP/SRTCP 保護媒體與控制封包。
4. **ABR / Congestion Control** — RTT、loss、可用頻寬惡化時，調整 bitrate / resolution / FPS / layer。
5. **Mesh / SFU / MCU** — 從兩人 P2P 擴展到多人通訊拓撲。

> 重要：Mamba 若出現在你的產品/研究中，可視為特定 ABR 方法；它不是 WebRTC 規範要求的標準模組。動畫中刻意把「WebRTC 標準流程」與「特定 ABR 演算法」分開。

## 安裝

Ubuntu 22.04/24.04：

```bash
sudo apt update
sudo apt install -y ffmpeg libcairo2-dev libpango1.0-dev pkg-config python3-venv \
  fonts-noto-cjk

python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## 先測第一章

```bash
source .venv/bin/activate
python -m manim -pql scenes/ch01_signaling.py Chapter1Signaling
```

## 一次渲染五章

```bash
./render_all.sh
```

預設 `QUALITY=h`（1080p）。快速預覽：

```bash
QUALITY=l ./render_all.sh
```

## 合併五章

```bash
./combine.sh
```

輸出：

```text
output/webrtc_story.mp4
```

## 中文字型

程式預設：

```python
FONT = "Noto Sans CJK TC"
```

若系統字型名稱不同，修改 `config.py` 即可。Linux 可用：

```bash
fc-list | grep -i "Noto Sans CJK"
```

## 建議交給 Codex 的指令

```text
這是一個 Manim WebRTC 教學動畫專案。請先建立 Python venv 並安裝 requirements.txt，
用 QUALITY=l ./render_all.sh 做快速 render。逐章修正所有 runtime error、字型問題、
文字超出畫面、物件重疊與動畫節奏問題，直到五章都能成功輸出。然後用 QUALITY=h
重新渲染並執行 ./combine.sh。不要改變 WebRTC 技術語意；若技術敘述需要修正，請先
保留原意並把修改寫到 CHANGELOG.md。
```

## 後續可升級

- 把向量人物換成透明 PNG / SVG 角色立繪。
- 使用 edge-tts / Azure / ElevenLabs 等 TTS 產生旁白，再用 FFmpeg 混音。
- 加中文字幕 SRT。
- 加音效：封包飛行、鎖頭、交通壅塞、TURN 中繼。
- 加 RFC / MDN / WebRTC 官方技術註解版。
