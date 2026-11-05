#!/usr/bin/env bash
# Rebuild every simulator page, in Thai and English, from the canvas sources in src/.
#   Thai pages:    <sim>/ for every simulator in src/
#   English pages: en/index.html  en/<sim>/
# English text comes from tools/i18n/en.json; the build stops if any Thai text has
# no translation, so add new strings there when you add or edit a page.
# Usage: bash tools/build.sh
set -euo pipefail
cd "$(dirname "$0")/.."
PY="python3 tools/dc2html.py"

# generated sources: the Sources pages and the Plate Tectonics map data
python3 tools/gen_sources.py >/dev/null
python3 - <<'PYEOF'
t = open("data/plate-tectonics/Main.template.html", encoding="utf-8").read()
d = open("data/plate-tectonics/data.js", encoding="utf-8").read().strip()
open("src/plate-tectonics/Main.dc.html", "w", encoding="utf-8").write(t.replace("/*@DATA*/", d))
PYEOF
EN=(--lang en --dict tools/i18n/en.json --runtime ../../shared/dc-runtime.js)

# page <src> <thai-out> <english-out> <thai crumbs...> -- <english crumbs...>
page() {
  local src=$1 th=$2 en=$3; shift 3
  local th_crumbs=() en_crumbs=()
  while [[ $1 != -- ]]; do th_crumbs+=(--crumb "$1"); shift; done; shift
  while [[ $# -gt 0 ]]; do en_crumbs+=(--crumb "$1"); shift; done
  $PY "$src" "$th" "${RENAMES[@]}" "${th_crumbs[@]}" --alt "English=../en/$th"
  $PY "$src" "en/$en" "${RENAMES[@]}" "${EN[@]}" "${en_crumbs[@]}" --alt "ไทย=../../$th"
}

# ---------- Ocean Wave Simulator ----------
RENAMES=(--rename Main.dc.html=index.html --rename Uses.dc.html=uses.html --rename Coast.dc.html=coast.html --rename Sources.dc.html=sources.html)
page src/ocean-waves/Main.dc.html ocean-waves/index.html ocean-waves/index.html \
  "หน้าหลัก=../index.html" "Ocean Wave Simulator=" -- \
  "Home=../index.html" "Ocean Wave Simulator="
page src/ocean-waves/Uses.dc.html ocean-waves/uses.html ocean-waves/uses.html \
  "หน้าหลัก=../index.html" "Ocean Wave Simulator=index.html" "ประโยชน์ของคลื่นทะเล=" -- \
  "Home=../index.html" "Ocean Wave Simulator=index.html" "Uses of ocean waves="
page src/ocean-waves/Coast.dc.html ocean-waves/coast.html ocean-waves/coast.html \
  "หน้าหลัก=../index.html" "Ocean Wave Simulator=index.html" "คลื่นใกล้ฝั่งและแมงกะพรุน=" -- \
  "Home=../index.html" "Ocean Wave Simulator=index.html" "Near-shore waves and jellyfish="
page src/ocean-waves/Sources.dc.html ocean-waves/sources.html ocean-waves/sources.html \
  "หน้าหลัก=../index.html" "Ocean Wave Simulator=index.html" "แหล่งข้อมูล=" -- \
  "Home=../index.html" "Ocean Wave Simulator=index.html" "Sources="

# ---------- Camera Lab ----------
ORDER=(Lens Sensor Fusion Spatial Stabilize Environment)
declare -A TH=(
  [Lens]="01 เลนส์และระยะโฟกัส"            [Sensor]="02 แสงและเซนเซอร์"
  [Fusion]="03 หลายกล้องและการประมวลผลภาพ"  [Spatial]="04 กล้องคู่และ Spatial"
  [Stabilize]="05 ระบบกันสั่น"              [Environment]="06 อุณหภูมิ ความชื้น รังสี"
)
declare -A ENT=(
  [Lens]="01 Lenses and focal length"      [Sensor]="02 Light and sensor"
  [Fusion]="03 Multi-camera and ISP"       [Spatial]="04 Stereo cameras and Spatial"
  [Stabilize]="05 Stabilisation"           [Environment]="06 Temperature, humidity, radiation"
)
RENAMES=(--rename Main.dc.html=index.html --rename Sources.dc.html=sources.html)
for n in "${ORDER[@]}"; do RENAMES+=(--rename "$n.dc.html=${n,,}.html"); done

page src/camera-lab/Main.dc.html camera-lab/index.html camera-lab/index.html \
  "หน้าหลัก=../index.html" "Camera Lab=" -- "Home=../index.html" "Camera Lab="
for n in "${ORDER[@]}"; do
  page "src/camera-lab/$n.dc.html" "camera-lab/${n,,}.html" "camera-lab/${n,,}.html" \
    "หน้าหลัก=../index.html" "Camera Lab=index.html" "${TH[$n]}=" -- \
    "Home=../index.html" "Camera Lab=index.html" "${ENT[$n]}="
done
page src/camera-lab/Sources.dc.html camera-lab/sources.html camera-lab/sources.html \
  "หน้าหลัก=../index.html" "Camera Lab=index.html" "แหล่งข้อมูล=" -- \
  "Home=../index.html" "Camera Lab=index.html" "Sources="

# ---------- Plate Tectonics Lab ----------
RENAMES=(--rename Main.dc.html=index.html --rename Physics.dc.html=physics.html --rename Safety.dc.html=safety.html --rename Sources.dc.html=sources.html)
page src/plate-tectonics/Main.dc.html plate-tectonics/index.html plate-tectonics/index.html \
  "หน้าหลัก=../index.html" "Plate Tectonics Lab=" -- "Home=../index.html" "Plate Tectonics Lab="
page src/plate-tectonics/Physics.dc.html plate-tectonics/physics.html plate-tectonics/physics.html \
  "หน้าหลัก=../index.html" "Plate Tectonics Lab=index.html" "ฟิสิกส์ของแผ่นดินไหว=" -- \
  "Home=../index.html" "Plate Tectonics Lab=index.html" "Earthquake physics="
page src/plate-tectonics/Safety.dc.html plate-tectonics/safety.html plate-tectonics/safety.html \
  "หน้าหลัก=../index.html" "Plate Tectonics Lab=index.html" "การรับมือและความปลอดภัย=" -- \
  "Home=../index.html" "Plate Tectonics Lab=index.html" "Response and safety="
page src/plate-tectonics/Sources.dc.html plate-tectonics/sources.html plate-tectonics/sources.html \
  "หน้าหลัก=../index.html" "Plate Tectonics Lab=index.html" "แหล่งข้อมูล=" -- \
  "Home=../index.html" "Plate Tectonics Lab=index.html" "Sources="

# ---------- Engineering labs (one main page + sources each) ----------
lab() {
  local dir=$1 name=$2
  RENAMES=(--rename Main.dc.html=index.html --rename Sources.dc.html=sources.html)
  page "src/$dir/Main.dc.html" "$dir/index.html" "$dir/index.html" \
    "หน้าหลัก=../index.html" "$name=" -- "Home=../index.html" "$name="
  page "src/$dir/Sources.dc.html" "$dir/sources.html" "$dir/sources.html" \
    "หน้าหลัก=../index.html" "$name=index.html" "แหล่งข้อมูล=" -- \
    "Home=../index.html" "$name=index.html" "Sources="
}
lab mechanics-lab "Mechanics Lab"
RENAMES=(--rename Main.dc.html=index.html --rename Swim.dc.html=swim.html --rename Statics.dc.html=statics.html \
  --rename Dynamics.dc.html=dynamics.html --rename Thermo.dc.html=thermo.html --rename Fluids.dc.html=fluids.html \
  --rename Sources.dc.html=sources.html)
page src/mechanics-lab/Main.dc.html mechanics-lab/index.html mechanics-lab/index.html \
  "หน้าหลัก=../index.html" "Mechanics Lab=" -- "Home=../index.html" "Mechanics Lab="
page src/mechanics-lab/Sources.dc.html mechanics-lab/sources.html mechanics-lab/sources.html \
  "หน้าหลัก=../index.html" "Mechanics Lab=index.html" "แหล่งข้อมูล=" -- \
  "Home=../index.html" "Mechanics Lab=index.html" "Sources="
declare -A MTH=([Swim]="ออกตัวว่ายน้ำ" [Statics]="สถิตยศาสตร์" [Dynamics]="พลศาสตร์" [Thermo]="อุณหพลศาสตร์" [Fluids]="กลศาสตร์ของไหล")
declare -A MEN=([Swim]="Swim start" [Statics]="Statics" [Dynamics]="Dynamics" [Thermo]="Thermodynamics" [Fluids]="Fluid mechanics")
for n in Statics Dynamics Thermo Fluids Swim; do
  page "src/mechanics-lab/$n.dc.html" "mechanics-lab/${n,,}.html" "mechanics-lab/${n,,}.html" \
    "หน้าหลัก=../index.html" "Mechanics Lab=index.html" "${MTH[$n]}=" -- \
    "Home=../index.html" "Mechanics Lab=index.html" "${MEN[$n]}="
done
lab beam-fea "Beam FEA"
lab circuit-lab "Circuit Lab"
lab chem-bio-lab "Chem · Bio Lab"

# ---------- English landing page ----------
$PY index.html en/index.html --plain --lang en --dict tools/i18n/en.json \
  --replace 'href="en/index.html" hreflang="en" lang="en" data-ps-lang="en" aria-label="Switch to English">=>href="../index.html" hreflang="th" lang="th" data-ps-lang="th" aria-label="Switch to Thai">' \
  --replace '</svg>English</a>=></svg>ไทย</a>' \
  --replace "document.documentElement.lang === 'th' && localStorage=>false && localStorage"
echo "built Thai + English pages"
