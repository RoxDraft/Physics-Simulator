# Plate Tectonics Lab data

`data.js` is the data block embedded in `src/plate-tectonics/Main.dc.html` (inserted by `tools/build.sh`
in place of `/*@DATA*/` in `Main.template.html`). It was produced by `build-data.mjs` from these open datasets:

| File | Source | Licence |
|---|---|---|
| `earthquakes-23k.csv` | USGS ANSS ComCat, M ≥ 5.5, 1965–2016 (copy in github.com/plotly/datasets) | Public domain |
| `volcano_db.csv` | Smithsonian Global Volcanism Program, Holocene list (older copy in github.com/plotly/datasets) | Free with attribution |
| `PB2002_boundaries.json` | Bird (2003) plate boundaries, github.com/fraxen/tectonicplates | ODC-BY 1.0 |
| `land-110m.json`, `countries-110m.json` | Natural Earth via npm `world-atlas@2.0.2` | Public domain |

To rebuild:

```bash
mkdir work && cd work
git clone --depth 1 https://github.com/fraxen/tectonicplates plates
git clone --depth 1 --filter=blob:none --sparse https://github.com/plotly/datasets pd
(cd pd && git sparse-checkout set --no-cone /earthquakes-23k.csv /volcano_db.csv)
npm i world-atlas@2.0.2 topojson-client@3.1.0 d3-geo@3.1.1
node ../build-data.mjs . > ../data.js
```

Country statistics use our own rule: an earthquake belongs to the country it is inside, or to the nearest
country whose land is within 300 km; otherwise it is "open ocean". These are not official statistics.
