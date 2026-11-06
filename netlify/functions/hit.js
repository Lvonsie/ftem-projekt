// FTEM – Zugriff zaehlen mit grober Herkunft (Land, Kanton/Region, Ort).
// Netlify liefert die Herkunft aus der IP-Adresse im Header "x-nf-geo"; die
// IP-Adresse selbst wird NICHT gespeichert. Koordinaten werden auf 0,1 Grad
// gerundet (ca. 10 km), damit kein genauer Standort entsteht.
// Gespeichert wird in ftem_stats: kind = "zugriff", meta = JSON
// {l: Sprache, c: Land (ISO-2), r: Kanton/Region-Code, ci: Ort, la, lo}.
const URL_STATS = 'https://xphbwnzyebbejsdeqled.supabase.co/rest/v1/ftem_stats';
const KEY = process.env.SUPABASE_SERVICE_KEY || 'sb_publishable_UQLqY8OqccllVy9t1FRlFQ_HZr_--D_';
const LANGS = ['de', 'fr', 'it', 'en'];

function geoFrom(event) {
  try {
    const raw = event.headers['x-nf-geo'] || event.headers['X-Nf-Geo'];
    if (!raw) return {};
    const g = JSON.parse(Buffer.from(raw, 'base64').toString('utf8'));
    const o = {};
    if (g.country && g.country.code) o.c = String(g.country.code).slice(0, 2).toUpperCase();
    if (g.subdivision && g.subdivision.code) o.r = String(g.subdivision.code).slice(0, 8);
    if (g.city) o.ci = String(g.city).slice(0, 60);
    const la = Number(g.latitude), lo = Number(g.longitude);
    if (isFinite(la) && isFinite(lo) && (la || lo)) { o.la = Math.round(la * 10) / 10; o.lo = Math.round(lo * 10) / 10; }
    return o;
  } catch (_) { return {}; }
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: '' };
  let body = {};
  try { body = JSON.parse(event.body || '{}'); } catch (_) {}
  const lang = LANGS.indexOf(body.l) >= 0 ? body.l : 'de';
  const meta = Object.assign({ l: lang }, geoFrom(event));
  try {
    const r = await fetch(URL_STATS, {
      method: 'POST',
      headers: { apikey: KEY, Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json', Prefer: 'return=minimal' },
      body: JSON.stringify({ kind: 'zugriff', meta: JSON.stringify(meta) })
    });
    return { statusCode: r.ok ? 204 : 502, body: '' };
  } catch (_) {
    return { statusCode: 502, body: '' };
  }
};
