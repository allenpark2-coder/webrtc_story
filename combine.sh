#!/usr/bin/env bash
set -euo pipefail

mkdir -p output
FILES=(
  "$(find media/videos -type f -name 'Chapter1Signaling.mp4' | head -n1)"
  "$(find media/videos -type f -name 'Chapter2IceStunTurn.mp4' | head -n1)"
  "$(find media/videos -type f -name 'Chapter3DtlsSrtp.mp4' | head -n1)"
  "$(find media/videos -type f -name 'Chapter4Abr.mp4' | head -n1)"
  "$(find media/videos -type f -name 'Chapter5Topologies.mp4' | head -n1)"
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
