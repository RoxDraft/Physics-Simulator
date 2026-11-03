// Builds the data block for src/plate-tectonics/Main.dc.html.
//
// Inputs (all open data, see data/plate-tectonics/README.md):
//   earthquakes-23k.csv  USGS ComCat significant earthquakes 1965–2016, M >= 5.5
//                        (copy in github.com/plotly/datasets)
//   volcano_db.csv       Smithsonian GVP Holocene volcano list (same repo)
//   PB2002_boundaries.json  Bird (2003) plate boundaries, github.com/fraxen/tectonicplates (ODC-BY)
//   world-atlas land-110m / countries-110m  Natural Earth (public domain), npm world-atlas@2
//
// Usage: node build-data.mjs <folder with the inputs and node_modules> > data.js
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';

const dir = process.argv[2] || '.';
const require = createRequire(path.join(path.resolve(dir), 'x.js'));
const topo = require('topojson-client');
const { geoContains, geoDistance } = require('d3-geo');
const read = f => fs.readFileSync(path.join(dir, f), 'utf8');

const W = 1000, H = 500, R = 6371;
const px = (lo, la) => [(lo + 180) / 360 * W, (90 - la) / 180 * H];
const r1 = v => Math.round(v * 10) / 10;

// ---------- earthquakes ----------
const quakes = read('pd/earthquakes-23k.csv').trim().split(/\r?\n/).slice(1).map(l => {
  const [d, la, lo, m] = l.split(',');
  return { y: +((d.match(/(19|20)\d\d/) || [])[0]), la: +la, lo: +lo, m: +m };
}).filter(e => !isNaN(e.m));

const world = JSON.parse(read('node_modules/world-atlas/countries-110m.json'));
const countries = topo.feature(world, world.objects.countries).features;
const verts = countries.map(c => { const pts = []; const walk = a => typeof a[0] === 'number' ? pts.push(a) : a.forEach(walk); walk(c.geometry ? c.geometry.coordinates : []); return pts; });
// A quake belongs to the country it is inside, or to the nearest country
// whose land is within 300 km; otherwise it is "open ocean".
function country(e) {
  const p = [e.lo, e.la];
  for (const c of countries) if (c.geometry && geoContains(c, p)) return c.properties.name;
  let best = null, bd = 1e9;
  countries.forEach((c, i) => { for (const v of verts[i]) { const d = geoDistance(p, v) * R; if (d < bd) { bd = d; best = c.properties.name; } } });
  return bd <= 300 ? best : 'open ocean';
}
const big = quakes.filter(e => e.m >= 6);
const byC = {};
for (const e of big) {
  e.c = country(e);
  const o = byC[e.c] ||= { m6: 0, m7: 0, m8: 0, max: 0 };
  o.m6++; if (e.m >= 7) o.m7++; if (e.m >= 8) o.m8++; o.max = Math.max(o.max, e.m);
}
const stats = Object.entries(byC).filter(([c]) => c !== 'open ocean').sort((a, b) => b[1].m6 - a[1].m6);

// ---------- volcanoes ----------
const parse = l => { const out = []; let cur = '', q = false; for (const ch of l) { if (ch === '"') q = !q; else if (ch === ',' && !q) { out.push(cur); cur = ''; } else cur += ch; } out.push(cur); return out; };
const vl = read('pd/volcano_db.csv').trim().split(/\r?\n/);
const hdr = vl[0].split(',');
const vols = vl.slice(1).map(parse).map(a => Object.fromEntries(hdr.map((h, i) => [h, a[i]])));
const vAll = {}, vRecent = {};
vols.forEach(v => { vAll[v.Country] = (vAll[v.Country] || 0) + 1; if (v['Last Known'] === 'D1') vRecent[v.Country] = (vRecent[v.Country] || 0) + 1; });

// ---------- map paths ----------
function ringPath(ring, step = 1) {
  let s = '', prev = null;
  ring.forEach((c, i) => {
    if (i % step && i !== ring.length - 1) return;
    const [x, y] = px(c[0], c[1]);
    s += ((!prev || Math.abs(x - prev[0]) > W / 2) ? 'M' : 'L') + r1(x) + ',' + r1(y);
    prev = [x, y];
  });
  return s;
}
const land = JSON.parse(read('node_modules/world-atlas/land-110m.json'));
let landD = '';
for (const f of topo.feature(land, land.objects.land).features) {
  const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
  for (const p of polys) for (const ring of p) landD += ringPath(ring) + 'Z';
}
const pb = JSON.parse(read('plates/GeoJSON/PB2002_boundaries.json'));
let sub = '', other = '';
for (const f of pb.features) { const d = ringPath(f.geometry.coordinates, 2); if (f.properties.Type === 'subduction') sub += d; else other += d; }

const out = {
  source: { quakes: quakes.length, years: [Math.min(...quakes.map(e => e.y)), Math.max(...quakes.map(e => e.y))], m6: big.length, volcanoes: vols.length },
  landD, sub, other,
  quakes: big.filter(e => e.m >= 7).map(e => { const [x, y] = px(e.lo, e.la); return [r1(x), r1(y), e.m, e.y, e.c]; }),
  volcanoes: vols.filter(v => v['Last Known'] === 'D1').map(v => { const [x, y] = px(+v.Longitude, +v.Latitude); return [r1(x), r1(y), v['Volcano Name'], v.Country, v.Type, +v.Elev]; }),
  quakeStats: stats.map(([c, o]) => [c, o.m6, o.m7, o.m8, o.max]),
  volcanoStats: Object.entries(vAll).sort((a, b) => b[1] - a[1]).map(([c, n]) => [c, n, vRecent[c] || 0])
};
process.stdout.write('var DATA = ' + JSON.stringify(out) + ';\n');
