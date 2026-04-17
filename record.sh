#!/bin/bash
# record.sh -- Simple scrcpy recording launcher with auto filename
# Usage: ./record.sh [duration_seconds]

DURATION="${1:-300}"
FILENAME="scrcpy_$(date +%Y%m%d_%H%M%S).mp4"

echo "🎥 scrcpy Recorder"
echo "━━━━━━━━━━━━━━━━━━━━━"
echo "Output: $FILENAME"
echo "Duration: ${DURATION}s"
echo "Press Ctrl+C to stop early"
echo ""

scrcpy --record "$FILENAME" --max-size 1080 --max-fps 30 --video-bit-rate 8M --stay-awake

if [ -f "$FILENAME" ]; then
    SIZE=$(du -h "$FILENAME" | cut -f1)
    echo ""
    echo "✅ Saved: $FILENAME ($SIZE)"
else
    echo "❌ Recording failed"
fi
