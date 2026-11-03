#!/usr/bin/env bash
# Rebuild every simulator page from the canvas sources in src/.
# Usage: bash tools/build.sh
set -euo pipefail
cd "$(dirname "$0")/.."
PY="python3 tools/dc2html.py"
HOME_CRUMB=(--crumb "หน้าหลัก=../index.html")

# ---------- Ocean Wave Simulator ----------
W=(--rename Main.dc.html=index.html --rename Uses.dc.html=uses.html)
$PY src/ocean-waves/Main.dc.html ocean-waves/index.html "${W[@]}" "${HOME_CRUMB[@]}" \
  --crumb "Ocean Wave Simulator="
$PY src/ocean-waves/Uses.dc.html ocean-waves/uses.html "${W[@]}" "${HOME_CRUMB[@]}" \
  --crumb "Ocean Wave Simulator=index.html" --crumb "ประโยชน์ของคลื่นทะเล="

# ---------- Camera Lab ----------
C=(--rename Main.dc.html=index.html)
declare -A TITLE=(
  [Lens]="01 เลนส์และระยะโฟกัส"
  [Sensor]="02 แสงและเซนเซอร์"
  [Fusion]="03 หลายกล้องและการประมวลผลภาพ"
  [Spatial]="04 กล้องคู่และ Spatial"
  [Stabilize]="05 ระบบกันสั่น"
  [Environment]="06 อุณหภูมิ ความชื้น รังสี"
)
ORDER=(Lens Sensor Fusion Spatial Stabilize Environment)
for n in "${ORDER[@]}"; do C+=(--rename "$n.dc.html=${n,,}.html"); done

$PY src/camera-lab/Main.dc.html camera-lab/index.html "${C[@]}" "${HOME_CRUMB[@]}" --crumb "Camera Lab="
for n in "${ORDER[@]}"; do
  $PY "src/camera-lab/$n.dc.html" "camera-lab/${n,,}.html" "${C[@]}" "${HOME_CRUMB[@]}" \
    --crumb "Camera Lab=index.html" --crumb "${TITLE[$n]}="
done
echo "built ocean-waves/ and camera-lab/"
