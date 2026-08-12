#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd "$PROJECT_DIR"

QUALITY=${QUALITY:-h}
FPS=${FPS:-30}

case "$QUALITY" in
  l) RESOLUTION=480p ;;
  m) RESOLUTION=720p ;;
  h) RESOLUTION=1080p ;;
  k) RESOLUTION=2160p ;;
  *) echo "Unsupported QUALITY: $QUALITY"; exit 1 ;;
esac

PROFILE="${RESOLUTION}${FPS}"

mkdir -p output
FILES=(
  "media/videos/ch01_signaling/$PROFILE/Chapter1Signaling.mp4"
  "media/videos/ch02_ice_stun_turn/$PROFILE/Chapter2IceStunTurn.mp4"
  "media/videos/ch03_dtls_srtp/$PROFILE/Chapter3DtlsSrtp.mp4"
  "media/videos/ch04_abr/$PROFILE/Chapter4Abr.mp4"
  "media/videos/ch05_topologies/$PROFILE/Chapter5Topologies.mp4"
)

for f in "${FILES[@]}"; do
  [[ -f "$f" ]] || { echo "Missing rendered file: $f"; exit 1; }
done

LIST=output/concat.txt
: > "$LIST"
for f in "${FILES[@]}"; do
  printf "file '%s'\n" "$(realpath "$f")" >> "$LIST"
done

ffmpeg -y -f concat -safe 0 -i "$LIST" -c copy output/webrtc_story.mp4

echo "Created output/webrtc_story.mp4"
