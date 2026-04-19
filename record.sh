#!/bin/bash
# record.sh -- Easy scrcpy recording with quality presets
# Usage: ./record.sh [quality] [device]
# Qualities: hd (720p), fhd (1080p), 4k, gaming (high fps)

QUALITY="${1:-hd}"
DEVICE="${2:-}"
BITRATE="5M"
FPS="30"

case "$QUALITY" in
  hd)
    BITRATE="4M"
    SIZE="1280"
    FPS="30"
    ;;
  fhd)
    BITRATE="8M"
    SIZE="1920"
    FPS="30"
    ;;
  4k)
    BITRATE="15M"
    SIZE="3840"
    FPS="24"
    ;;
  gaming)
    BITRATE="12M"
    SIZE="1920"
    FPS="60"
    ;;
  *)
    echo "Unknown quality: $QUALITY"
    exit 1
    ;;
esac

DEVICE_ARG=""
[[ -n "$DEVICE" ]] && DEVICE_ARG="-s $DEVICE"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT="scrcpy_${QUALITY}_${TIMESTAMP}.mp4"

echo "🎥 Recording: $OUTPUT"
echo "   Quality: $QUALITY | Bitrate: $BITRATE | FPS: $FPS | Size: ${SIZE}p"
echo ""

scrcpy $DEVICE_ARG \
  --video-bit-rate=$BITRATE \
  --max-fps=$FPS \
  --max-size=$SIZE \
  --record="$OUTPUT" \
  --stay-awake \
  --disable-screensaver

echo ""
echo "✅ Saved to: $OUTPUT"
