#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd "$PROJECT_DIR"
export PYTHONPATH="$PROJECT_DIR${PYTHONPATH:+:$PYTHONPATH}"

QUALITY=${QUALITY:-h}   # l=480p, m=720p, h=1080p, k=4K
FPS=${FPS:-30}

SCENES=(
  "scenes/ch01_signaling.py Chapter1Signaling"
  "scenes/ch02_ice_stun_turn.py Chapter2IceStunTurn"
  "scenes/ch03_dtls_srtp.py Chapter3DtlsSrtp"
  "scenes/ch04_abr.py Chapter4Abr"
  "scenes/ch05_topologies.py Chapter5Topologies"
)

for item in "${SCENES[@]}"; do
  file=${item% *}
  scene=${item##* }
  echo "==> Rendering $scene"
  manim -q${QUALITY} --fps "$FPS" "$file" "$scene"
done

echo "Done. Manim videos are under media/videos/..."
echo "Run ./combine.sh after rendering."
