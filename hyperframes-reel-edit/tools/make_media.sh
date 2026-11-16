#!/usr/bin/env bash
# Rebuild the derived media from ../rawreel.mov (the original is never modified).
# Output: work/dialogue*.wav, assets/media/aroll.mp4 (1080x1920 SDR proxy + processed dialogue)
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=../rawreel.mov
mkdir -p work assets/media
ffmpeg -v error -y -i "$SRC" -map 0:a:0 -ac 1 -ar 16000 work/dialogue16k.wav
ffmpeg -v error -y -i "$SRC" -map 0:a:0 -c:a pcm_s24le work/dialogue48k.wav
# dialogue: HPF 70 Hz -> gentle comp -> loudnorm (-14 LUFS, -1.5 dBTP), measured values from pass 1
ffmpeg -v error -y -i work/dialogue48k.wav -af "highpass=f=70,acompressor=threshold=-30dB:ratio=2.2:attack=12:release=220:makeup=1,loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=-33.68:measured_TP=-8.68:measured_LRA=5.90:measured_thresh=-44.53:offset=-0.21,aresample=48000" -c:a pcm_s24le work/dialogue_processed.wav
# picture: iPhone HLG (BT.2020 / ARIB STD-B67) -> SDR BT.709, 1080x1920, 30 fps, GOP 15 for seek-safety
ffmpeg -v error -y -i "$SRC" -i work/dialogue_processed.wav -map 0:v:0 -map 1:a:0 \
  -vf "zscale=tin=arib-std-b67:t=bt709:pin=bt2020:p=bt709:min=bt2020nc:m=bt709:r=tv:npl=203,format=yuv420p,scale=1080:1920:flags=lanczos,setsar=1" \
  -r 30 -c:v libx264 -preset medium -crf 15 -g 15 -keyint_min 15 -sc_threshold 0 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart assets/media/aroll.mp4
echo "done: assets/media/aroll.mp4"
