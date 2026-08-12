const CACHE="ftem-fd92dbb1b1";
const CORE=["./", "./index.html", "./fr.html", "./it.html", "./en.html", "./admin.html", "./manifest.webmanifest", "./assets/favicon.svg", "./assets/icon-192.png", "./assets/icon-512.png", "./assets/icon-180.png", "./assets/hero.jpg", "./assets/og-image.jpg", "./assets/swiss-ski-logo.svg", "./assets/sporticons/reserve-moguls.png", "./assets/sporticons/freeski-park-pipe.png", "./assets/sporticons/skicross.png", "./assets/sporticons/biathlon.png", "./assets/sporticons/ski-alpin.png", "./assets/sporticons/skispringen.png", "./assets/sporticons/snowboard-park-pipe.png", "./assets/sporticons/reserve-telemark.png", "./assets/sporticons/langlauf.png", "./assets/sporticons/reserve-aerials.png", "./assets/sporticons/nordische-kombination.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()));});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener("fetch",e=>{const req=e.request;if(req.method!=="GET")return;const url=new URL(req.url);if(url.origin!==location.origin)return;
  const isPage=req.mode==="navigate"||url.pathname.endsWith(".html")||url.pathname.endsWith("/");
  if(isPage){
    // Seiten: immer zuerst frisch vom Netz (kein "alte Version"-Problem mehr), Cache nur offline
    e.respondWith(caches.open(CACHE).then(async c=>{try{const res=await fetch(req);if(res&&res.status===200)c.put(req,res.clone());return res;}catch(_){const cached=await c.match(req);return cached||Response.error();}}));
    return;
  }
  e.respondWith(caches.open(CACHE).then(async c=>{const cached=await c.match(req);const net=fetch(req).then(res=>{if(res&&res.status===200)c.put(req,res.clone());return res;}).catch(()=>cached);return cached||net;}));});
