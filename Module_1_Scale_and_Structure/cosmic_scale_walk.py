# cosmic_scale_walk.py
# Powers of Ten — Cosmic Scale Walk
# Run: python cosmic_scale_walk.py
# Opens automatically in your default browser. No pip installs needed.

import math
import os
import tempfile
import webbrowser

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cosmic Scale Walk — Powers of Ten</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Segoe UI',system-ui,sans-serif;background:#0a0b1a;color:#e8eaf6;min-height:100vh;padding:24px 16px}
  #app{max-width:780px;margin:0 auto}
  .app-header{text-align:center;margin-bottom:28px}
  .app-header h1{font-family:'Courier New',monospace;font-size:13px;letter-spacing:4px;color:#7986cb;text-transform:uppercase;margin-bottom:6px}
  .app-header p{font-size:13px;color:rgba(200,210,255,0.4)}
  .tl-wrap{margin-bottom:24px}
  .tl-label{font-family:'Courier New',monospace;font-size:10px;letter-spacing:2px;color:rgba(200,210,255,0.35);margin-bottom:8px;text-transform:uppercase}
  .tl-track{position:relative;height:6px;background:rgba(255,255,255,0.06);border-radius:3px;margin-bottom:10px}
  .tl-fill{height:100%;border-radius:3px;transition:width .5s ease}
  .tl-dots{display:flex;justify-content:space-between}
  .t-dot{width:30px;height:30px;border-radius:50%;border:2px solid rgba(255,255,255,0.1);background:rgba(255,255,255,0.04);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px;transition:all .2s;flex-shrink:0}
  .t-dot:hover{border-color:rgba(255,255,255,0.3);transform:scale(1.1)}
  .main-card{border-radius:16px;border:1.5px solid;padding:28px;margin-bottom:20px;transition:border-color .4s,background .4s;position:relative}
  .card-idx{position:absolute;top:18px;right:20px;font-family:'Courier New',monospace;font-size:11px;opacity:.3}
  .card-top{display:flex;align-items:flex-start;gap:20px;margin-bottom:20px}
  .obj-icon{font-size:58px;line-height:1;flex-shrink:0}
  .obj-meta{flex:1}
  .obj-name{font-size:22px;font-weight:700;color:#fff;margin-bottom:6px}
  .obj-badge{display:inline-block;font-family:'Courier New',monospace;font-size:12px;padding:4px 12px;border-radius:20px;margin-bottom:10px;border:1px solid}
  .obj-desc{font-size:14px;line-height:1.75;color:rgba(220,230,255,0.82)}
  .facts-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:16px}
  .fact-cell{border-radius:10px;padding:11px 14px;border:1px solid rgba(255,255,255,0.06);background:rgba(0,0,0,.2)}
  .fact-lbl{font-size:10px;letter-spacing:1.2px;text-transform:uppercase;opacity:.45;margin-bottom:3px}
  .fact-val{font-family:'Courier New',monospace;font-size:13px;font-weight:600}
  .pow-box{border-radius:10px;padding:14px 18px;border:1px solid rgba(255,255,255,0.1);background:rgba(0,0,0,.25);text-align:center;margin-bottom:14px}
  .pow-lbl{font-size:10px;letter-spacing:2px;text-transform:uppercase;opacity:.4;margin-bottom:6px}
  .pow-val{font-family:'Courier New',monospace;font-size:28px;font-weight:700;margin-bottom:4px}
  .pow-ctx{font-size:12px;opacity:.45}
  .rel-wrap{margin-bottom:14px}
  .rel-lbl{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;opacity:.35;margin-bottom:6px}
  .rel-track{height:18px;border-radius:4px;background:rgba(255,255,255,0.05);overflow:hidden;margin-bottom:4px}
  .rel-fill{height:100%;border-radius:4px;min-width:3px;transition:width .6s ease}
  .rel-note{font-family:'Courier New',monospace;font-size:10px;opacity:.3}
  .mc-box{border-radius:10px;padding:12px 16px;border:1px solid rgba(239,83,80,.3);background:rgba(239,83,80,.08);margin-bottom:14px}
  .mc-title{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#ef9a9a;margin-bottom:5px}
  .mc-text{font-size:13px;line-height:1.65;color:rgba(255,200,200,.78)}
  .controls{display:flex;align-items:center;justify-content:space-between;gap:12px}
  .btn{font-family:'Segoe UI',system-ui,sans-serif;font-size:14px;font-weight:500;padding:11px 26px;border-radius:10px;border:1.5px solid rgba(255,255,255,.15);background:rgba(255,255,255,.05);color:rgba(220,225,255,.85);cursor:pointer;transition:all .18s}
  .btn:hover:not(:disabled){background:rgba(255,255,255,.1);color:#fff}
  .btn:active:not(:disabled){transform:scale(.97)}
  .btn:disabled{opacity:.22;cursor:not-allowed}
  .btn-next{background:rgba(57,73,171,.25);border-color:rgba(121,134,203,.4);color:#c5cae9}
  .btn-next:hover:not(:disabled){background:rgba(57,73,171,.45);color:#fff}
  .step-ctr{font-family:'Courier New',monospace;font-size:12px;opacity:.3;text-align:center;flex:1}
  .viz-wrap{margin-top:20px;background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:16px}
  .viz-lbl{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;opacity:.35;margin-bottom:12px;text-align:center}
  #scale-svg{width:100%;display:block}
  .kb-hint{text-align:center;font-size:11px;opacity:.25;margin-top:14px;font-family:'Courier New',monospace}
</style>
</head>
<body>
<div id="app">
  <div class="app-header">
    <h1>Cosmic Scale Walk — Powers of Ten</h1>
    <p>Module 1 &middot; Scale &amp; Structure of the Universe &middot; Interactive Reference</p>
  </div>
  <div class="tl-wrap">
    <div class="tl-label">Journey Progress &mdash; Orders of Magnitude (10&sup0; &rarr; 10&sup2;&sup6; m)</div>
    <div class="tl-track"><div class="tl-fill" id="tl-fill"></div></div>
    <div class="tl-dots" id="tl-dots"></div>
  </div>
  <div class="main-card" id="main-card">
    <div class="card-idx" id="card-idx"></div>
    <div class="card-top">
      <div class="obj-icon" id="obj-icon"></div>
      <div class="obj-meta">
        <div class="obj-name" id="obj-name"></div>
        <div class="obj-badge" id="obj-badge"></div>
        <div class="obj-desc" id="obj-desc"></div>
      </div>
    </div>
    <div class="facts-grid" id="facts-grid"></div>
    <div class="pow-box" id="pow-box">
      <div class="pow-lbl">Order of Magnitude (metres)</div>
      <div class="pow-val" id="pow-val"></div>
      <div class="pow-ctx" id="pow-ctx"></div>
    </div>
    <div class="rel-wrap">
      <div class="rel-lbl">Scale relative to observable universe (log)</div>
      <div class="rel-track"><div class="rel-fill" id="rel-fill"></div></div>
      <div class="rel-note" id="rel-note"></div>
    </div>
    <div class="mc-box" id="mc-box" style="display:none">
      <div class="mc-title">&#9888; Common Misconception</div>
      <div class="mc-text" id="mc-text"></div>
    </div>
  </div>
  <div class="controls">
    <button class="btn" id="btn-prev" onclick="navigate(-1)">&larr; Previous</button>
    <div class="step-ctr" id="step-ctr"></div>
    <button class="btn btn-next" id="btn-next" onclick="navigate(1)">Next &rarr;</button>
  </div>
  <div class="viz-wrap">
    <div class="viz-lbl">All 10 scales &mdash; click any icon to jump</div>
    <svg id="scale-svg" viewBox="0 0 700 90" xmlns="http://www.w3.org/2000/svg"></svg>
  </div>
  <div class="kb-hint">Use &larr; &rarr; arrow keys to navigate</div>
</div>

<script>
const STOPS = [
  {
    icon:"🧍", name:"A Human", scale:"~1.7 m", exp:0,
    color:{bg:"#1a2340",border:"#3f51b5",badge_bg:"#1e2a5e",badge_col:"#9fa8da",fill:"#3f51b5",dot:"#7986cb"},
    desc:"Our intuitive reference point. At ~1.7 metres tall, human perception is tuned for this scale — the scale of tools, rooms, and trees. Everything in astronomy begins here and quickly escapes it.",
    facts:[{lbl:"Height",val:"~1.7 m"},{lbl:"Mass",val:"~70 kg"},{lbl:"Light travel time",val:"~5.7 ns"},{lbl:"Scale",val:"10\u2070 m"}],
    powCtx:"1 metre \u2014 our intuitive baseline", mc:null
  },
  {
    icon:"🌍", name:"Planet Earth", scale:"12,742 km diameter", exp:7,
    color:{bg:"#0d2038",border:"#1565c0",badge_bg:"#0d2248",badge_col:"#82b1ff",fill:"#1976d2",dot:"#42a5f5"},
    desc:"Earth has a mean diameter of 12,742 km. If a human were scaled to a marble (1 cm), Earth would be ~75 m away — already beyond everyday intuition.",
    facts:[{lbl:"Diameter",val:"12,742 km"},{lbl:"Circumference",val:"40,075 km"},{lbl:"Light cross time",val:"~42 ms"},{lbl:"Distance unit",val:"km"}],
    powCtx:"10\u2077 m \u2014 seven orders above a human", mc:null
  },
  {
    icon:"🌕", name:"Earth\u2013Moon System", scale:"384,400 km (mean)", exp:8,
    color:{bg:"#1a1a2e",border:"#5c6bc0",badge_bg:"#232350",badge_col:"#b3bcf5",fill:"#5c6bc0",dot:"#9fa8da"},
    desc:"The Moon orbits Earth at a mean distance of 384,400 km — about 30 Earth diameters. Light takes ~1.3 seconds to travel this gap. Apollo missions took ~3 days to cross it.",
    facts:[{lbl:"Mean distance",val:"384,400 km"},{lbl:"Moon diameter",val:"3,474 km"},{lbl:"Light travel time",val:"~1.3 s"},{lbl:"Apollo transit",val:"~3 days"}],
    powCtx:"~4 \u00d7 10\u2078 m", mc:null
  },
  {
    icon:"☀️", name:"Solar System (AU scale)", scale:"1 AU = 149.6 million km", exp:11,
    color:{bg:"#1f1800",border:"#f57f17",badge_bg:"#2e2000",badge_col:"#ffe082",fill:"#f9a825",dot:"#ffd54f"},
    desc:"The Astronomical Unit (AU) is the mean Earth\u2013Sun distance: 149.6 million km. Sunlight takes ~8 min 20 s to reach Earth. The full Solar System (to Neptune) spans ~30 AU.",
    facts:[{lbl:"1 AU",val:"149.6 \u00d7 10\u2076 km"},{lbl:"Sunlight to Earth",val:"~8 min 20 s"},{lbl:"Sun diameter",val:"1.39 \u00d7 10\u2076 km"},{lbl:"Neptune orbit",val:"~30 AU"}],
    powCtx:"~1.5 \u00d7 10\u00b9\u00b9 m \u2014 the Astronomical Unit",
    mc:"The AU is NOT the edge of the Solar System. The Oort Cloud extends to ~100,000 AU \u2014 nearly halfway to the nearest star."
  },
  {
    icon:"☁️", name:"Oort Cloud", scale:"~2,000 \u2013 100,000 AU", exp:15,
    color:{bg:"#001a2c",border:"#00838f",badge_bg:"#002535",badge_col:"#80deea",fill:"#00838f",dot:"#4dd0e1"},
    desc:"The Oort Cloud is a vast spherical shell of icy bodies surrounding the Solar System. Its outer boundary extends to ~100,000 AU (~1.6 light-years) \u2014 the true edge of the Sun's gravitational influence.",
    facts:[{lbl:"Inner boundary",val:"~2,000 AU"},{lbl:"Outer boundary",val:"~100,000 AU"},{lbl:"In light-years",val:"~1.6 ly"},{lbl:"Status",val:"No spacecraft reached"}],
    powCtx:"~10\u00b9\u2075 m \u2014 still within the Solar System",
    mc:"The Solar System is NOT just the 8 planets. Its gravitational domain extends far beyond Neptune into the vast Oort Cloud."
  },
  {
    icon:"⭐", name:"Local stellar neighborhood", scale:"Proxima Centauri: 4.24 ly", exp:16,
    color:{bg:"#1a1400",border:"#e65100",badge_bg:"#261b00",badge_col:"#ffcc80",fill:"#ef6c00",dot:"#ffa726"},
    desc:"The nearest star, Proxima Centauri, lies 4.24 light-years away \u2014 ~268,000 AU. A light-year is ~9.46 \u00d7 10\u00b9\u00b2 km. Voyager 1 at ~17 km/s would take ~75,000 years to arrive.",
    facts:[{lbl:"Proxima Centauri",val:"4.24 ly"},{lbl:"In AU",val:"~268,000 AU"},{lbl:"1 light-year",val:"9.461 \u00d7 10\u00b9\u00b2 km"},{lbl:"1 parsec",val:"3.26 ly"}],
    powCtx:"~4 \u00d7 10\u00b9\u2076 m \u2014 the light-year scale begins",
    mc:"A light-year is a unit of DISTANCE, not time. It is the distance light travels in one Julian year (~9.46 trillion km)."
  },
  {
    icon:"🌌", name:"The Milky Way Galaxy", scale:"~100,000 light-years across", exp:21,
    color:{bg:"#0e002a",border:"#6a1b9a",badge_bg:"#180038",badge_col:"#ce93d8",fill:"#7b1fa2",dot:"#ba68c8"},
    desc:"Our barred-spiral galaxy spans ~100,000 light-years in diameter and contains 100\u2013400 billion stars. The Sun lies ~26,000 light-years from the galactic centre, in the Orion Arm.",
    facts:[{lbl:"Diameter",val:"~100,000 ly"},{lbl:"Disk thickness",val:"~1,000 ly"},{lbl:"Star count",val:"100\u2013400 billion"},{lbl:"Sun's position",val:"~26,000 ly from core"}],
    powCtx:"~10\u00b2\u00b9 m \u2014 the galaxy scale",
    mc:"Galaxies are NOT dense balls of stars. The average distance between stars in the Milky Way is several light-years \u2014 they are almost entirely empty space."
  },
  {
    icon:"🔭", name:"Local Group", scale:"~10 million light-years", exp:22,
    color:{bg:"#002010",border:"#2e7d32",badge_bg:"#001a0a",badge_col:"#a5d6a7",fill:"#388e3c",dot:"#81c784"},
    desc:"The Local Group is a gravitationally bound collection of ~80 galaxies dominated by the Milky Way and Andromeda (M31, ~2.537 Mly away). Andromeda is on a collision course with us \u2014 merger expected in ~4.5 billion years.",
    facts:[{lbl:"Diameter",val:"~10 Mly"},{lbl:"Major members",val:"MW, M31, M33"},{lbl:"Andromeda dist.",val:"~2.537 Mly"},{lbl:"Galaxy count",val:"~80 members"}],
    powCtx:"~10\u00b2\u00b2 m \u2014 galaxy group scale", mc:null
  },
  {
    icon:"🕸", name:"Laniakea Supercluster", scale:"~520 million light-years", exp:24,
    color:{bg:"#1a0020",border:"#ad1457",badge_bg:"#25002e",badge_col:"#f48fb1",fill:"#c2185b",dot:"#f06292"},
    desc:"Laniakea ('immeasurable heaven' in Hawaiian) is our home supercluster. Mapped in 2014 by Tully et al., it spans ~520 million light-years, contains ~100,000 galaxies, and has a mass of ~10\u00b9\u2077 solar masses.",
    facts:[{lbl:"Diameter",val:"~520 Mly"},{lbl:"Mass",val:"~10\u00b9\u2077 M\u2609"},{lbl:"Galaxy count",val:"~100,000"},{lbl:"Named",val:"2014 \u2014 Tully et al."}],
    powCtx:"~5 \u00d7 10\u00b2\u2074 m \u2014 supercluster scale", mc:null
  },
  {
    icon:"🌐", name:"Observable Universe", scale:"~93 billion light-years", exp:26,
    color:{bg:"#001520",border:"#006064",badge_bg:"#002030",badge_col:"#80cbc4",fill:"#00838f",dot:"#4db6ac"},
    desc:"The Observable Universe spans ~93 billion light-years in diameter, centred on Earth \u2014 not because we are special, but because light has had ~13.8 billion years to reach us. The full Universe may be vastly larger, or infinite.",
    facts:[{lbl:"Diameter",val:"~93 billion ly"},{lbl:"Age",val:"~13.8 billion years"},{lbl:"Galaxy count",val:"~2 trillion"},{lbl:"Hubble radius",val:"~46.5 billion ly"}],
    powCtx:"~8.8 \u00d7 10\u00b2\u2076 m \u2014 the cosmic horizon",
    mc:"The Observable Universe is NOT the entire Universe. It is only the region from which light has had time to reach us. The full Universe is likely much larger \u2014 possibly infinite."
  }
];

const SUP = {'0':'\u2070','1':'\u00b9','2':'\u00b2','3':'\u00b3','4':'\u2074','5':'\u2075','6':'\u2076','7':'\u2077','8':'\u2078','9':'\u2079','-':'\u207b'};
function sup(n){ return '10' + String(n).split('').map(c=>SUP[c]||c).join(''); }

let cur = 0;

function buildDots(){
  const wrap = document.getElementById('tl-dots');
  wrap.innerHTML = '';
  STOPS.forEach((s,i)=>{
    const d = document.createElement('div');
    d.className = 't-dot';
    d.id = 'dot-'+i;
    d.title = s.name;
    d.textContent = s.icon;
    d.onclick = ()=>{ cur=i; render(); };
    wrap.appendChild(d);
  });
}

function updateDots(){
  STOPS.forEach((s,i)=>{
    const d = document.getElementById('dot-'+i);
    if(!d) return;
    if(i===cur){
      d.style.borderColor = s.color.dot;
      d.style.boxShadow = '0 0 0 3px '+s.color.dot+'55';
      d.style.background = s.color.badge_bg;
      d.style.transform = 'scale(1.15)';
    } else if(i<cur){
      d.style.borderColor = STOPS[i].color.border;
      d.style.boxShadow = 'none';
      d.style.background = STOPS[i].color.bg;
      d.style.transform = 'scale(1)';
    } else {
      d.style.borderColor = 'rgba(255,255,255,0.1)';
      d.style.boxShadow = 'none';
      d.style.background = 'rgba(255,255,255,0.04)';
      d.style.transform = 'scale(1)';
    }
  });
}

function buildSVG(){
  const svg = document.getElementById('scale-svg');
  const W=700, PAD=30, usable=W-PAD*2;
  let h = '';
  h += '<line x1="'+PAD+'" y1="45" x2="'+(W-PAD)+'" y2="45" stroke="rgba(255,255,255,0.08)" stroke-width="2"/>';
  STOPS.forEach((s,i)=>{
    const pct = s.exp/26;
    const x = Math.round(PAD + pct*usable);
    h += '<circle cx="'+x+'" cy="45" r="14" fill="'+s.color.bg+'" stroke="'+s.color.dot+'" stroke-width="1.5" style="cursor:pointer" onclick="jumpTo('+i+')"/>';
    h += '<text x="'+x+'" y="50" text-anchor="middle" font-size="14" style="cursor:pointer;pointer-events:none">'+s.icon+'</text>';
    const ly = (i%2===0)?22:78;
    h += '<text x="'+x+'" y="'+ly+'" text-anchor="middle" fill="'+s.color.dot+'" font-size="9" font-family="Courier New,monospace" style="cursor:pointer" onclick="jumpTo('+i+')">'+sup(s.exp)+'</text>';
  });
  const cx = Math.round(PAD + (STOPS[cur].exp/26)*usable);
  h += '<circle cx="'+cx+'" cy="45" r="18" fill="none" stroke="'+STOPS[cur].color.dot+'" stroke-width="2.5" stroke-dasharray="5 3"/>';
  svg.innerHTML = h;
}

function jumpTo(i){ cur=i; render(); }
window.jumpTo = jumpTo;

function render(){
  const s = STOPS[cur];
  const c = s.color;

  const card = document.getElementById('main-card');
  card.style.background = c.bg;
  card.style.borderColor = c.border;

  document.getElementById('card-idx').textContent = (cur+1)+' / '+STOPS.length;
  document.getElementById('obj-icon').textContent = s.icon;
  document.getElementById('obj-name').textContent = s.name;

  const badge = document.getElementById('obj-badge');
  badge.textContent = s.scale;
  badge.style.background = c.badge_bg;
  badge.style.color = c.badge_col;
  badge.style.borderColor = c.border;

  document.getElementById('obj-desc').textContent = s.desc;

  const fg = document.getElementById('facts-grid');
  fg.innerHTML = '';
  s.facts.forEach(f=>{
    const cell = document.createElement('div');
    cell.className = 'fact-cell';
    cell.innerHTML = '<div class="fact-lbl">'+f.lbl+'</div><div class="fact-val" style="color:'+c.badge_col+'">'+f.val+'</div>';
    fg.appendChild(cell);
  });

  document.getElementById('pow-box').style.borderColor = c.border;
  document.getElementById('pow-val').textContent = sup(s.exp)+' m';
  document.getElementById('pow-val').style.color = c.badge_col;
  document.getElementById('pow-ctx').textContent = s.powCtx;

  const pct = Math.max(2, Math.round(s.exp/26*100));
  const rf = document.getElementById('rel-fill');
  rf.style.width = pct+'%';
  rf.style.background = c.fill;
  document.getElementById('rel-note').textContent = sup(s.exp)+' m vs '+sup(26)+' m  \u2014  '+(26-s.exp)+' orders of magnitude smaller than the observable universe';

  const mc = document.getElementById('mc-box');
  if(s.mc){ mc.style.display='block'; document.getElementById('mc-text').textContent=s.mc; }
  else { mc.style.display='none'; }

  const tf = document.getElementById('tl-fill');
  tf.style.width = Math.max(2,Math.round(cur/(STOPS.length-1)*100))+'%';
  tf.style.background = c.fill;

  document.getElementById('step-ctr').textContent = 'Step '+(cur+1)+' of '+STOPS.length;

  const bp = document.getElementById('btn-prev');
  const bn = document.getElementById('btn-next');
  bp.disabled = cur===0;
  bn.disabled = cur===STOPS.length-1;
  bn.textContent = cur===STOPS.length-1 ? '\u2014 End of Journey \u2014' : 'Next \u2192';

  updateDots();
  buildSVG();
}

function navigate(dir){
  const n = cur+dir;
  if(n<0||n>=STOPS.length) return;
  cur=n; render();
}
window.navigate = navigate;

document.addEventListener('keydown', e=>{
  if(e.key==='ArrowRight') navigate(1);
  if(e.key==='ArrowLeft') navigate(-1);
});

buildDots();
render();
</script>
</body>
</html>"""


def main():
    tmp = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".html",
        delete=False,
        encoding="utf-8"
    )
    tmp.write(HTML)
    tmp.close()

    path = "file://" + tmp.name.replace("\\", "/")
    print("=" * 60)
    print("  Cosmic Scale Walk — Powers of Ten")
    print("=" * 60)
    print(f"\n  Opening in browser: {tmp.name}\n")
    print("  Controls:")
    print("    Click  -> Previous / Next buttons")
    print("    Click  -> Any icon dot to jump to that scale")
    print("    Keys   -> Left / Right arrow keys")
    print("\n  Stops covered (10 scales):")
    names = [
        "Human            (10^0 m)",
        "Earth            (10^7 m)",
        "Earth-Moon       (10^8 m)",
        "Solar System     (10^11 m)",
        "Oort Cloud       (10^15 m)",
        "Nearest Star     (10^16 m)",
        "Milky Way        (10^21 m)",
        "Local Group      (10^22 m)",
        "Laniakea         (10^24 m)",
        "Observable Univ  (10^26 m)",
    ]
    for n in names:
        print(f"    {n}")
    print("\n  Close the browser tab when done.")
    print("=" * 60)
    webbrowser.open(path)


if __name__ == "__main__":
    main()