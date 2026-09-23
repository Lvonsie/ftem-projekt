// FTEM Admin-Speichern – serverseitig geschuetzter Schreibzugriff auf die
// Text-Tabelle (Supabase ftem_overrides).
//
// Hintergrund: Der oeffentliche (anon) Supabase-Schluessel steht in jeder Seite.
// Damit niemand Fremdes Texte ueberschreiben kann, verliert er die Schreibrechte
// (RLS-Policies, nur noch SELECT). Gespeichert wird stattdessen hier: Der
// Admin-Bereich schickt das beim Login eingegebene Passwort mit, diese Funktion
// prueft es gegen die Netlify-Umgebungsvariable ADMIN_API_KEY und schreibt dann
// mit dem geheimen "service role"-Schluessel (SUPABASE_SERVICE_KEY, nur auf dem
// Server). Solange SUPABASE_SERVICE_KEY noch nicht gesetzt ist, wird der anon-
// Schluessel verwendet - so funktioniert der Umbau auch VOR der RLS-Umstellung.
const SUPA_URL = 'https://xphbwnzyebbejsdeqled.supabase.co/rest/v1/ftem_overrides';
const ANON_KEY = 'sb_publishable_UQLqY8OqccllVy9t1FRlFQ_HZr_--D_';

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return json(405, { error: 'method_not_allowed' });
  const NEED = process.env.ADMIN_API_KEY || '';
  if (!NEED) {
    return json(503, { error: 'not_configured',
      message: 'Speichern ist noch nicht konfiguriert (ADMIN_API_KEY fehlt in Netlify).' });
  }
  let body;
  try { body = JSON.parse(event.body || '{}'); }
  catch { return json(400, { error: 'bad_request' }); }
  if (String(body.key || '') !== NEED) {
    return json(401, { error: 'unauthorized', message: 'Nicht berechtigt (Admin-Anmeldung erforderlich).' });
  }

  const rows = Array.isArray(body.rows) ? body.rows : [];
  const del  = Array.isArray(body.del)  ? body.del  : [];
  if (!rows.length && !del.length) return json(400, { error: 'empty' });
  if (rows.length > 400 || del.length > 100) return json(400, { error: 'too_many' });
  for (const r of rows) {
    if (!r || typeof r.cid !== 'string' || !r.cid || r.cid.length > 300
        || typeof r.txt !== 'string' || r.txt.length > 40000) {
      return json(400, { error: 'bad_row' });
    }
  }
  for (const c of del) {
    if (typeof c !== 'string' || !c || c.length > 300) return json(400, { error: 'bad_row' });
  }

  const KEY = process.env.SUPABASE_SERVICE_KEY || ANON_KEY;
  const H = { apikey: KEY, Authorization: 'Bearer ' + KEY };
  try {
    if (rows.length) {
      const r = await fetch(SUPA_URL, { method: 'POST',
        headers: { ...H, 'Content-Type': 'application/json', Prefer: 'resolution=merge-duplicates,return=minimal' },
        body: JSON.stringify(rows.map(x => ({ cid: x.cid, txt: x.txt }))) });
      if (!r.ok) return json(502, { error: 'upstream', message: 'Supabase-Fehler beim Speichern (HTTP ' + r.status + ').' });
    }
    for (const c of del) {
      const r = await fetch(SUPA_URL + '?cid=eq.' + encodeURIComponent(c), { method: 'DELETE', headers: H });
      if (!r.ok) return json(502, { error: 'upstream', message: 'Supabase-Fehler beim Löschen (HTTP ' + r.status + ').' });
    }
    return json(200, { ok: true, saved: rows.length, deleted: del.length });
  } catch (e) {
    return json(500, { error: 'server', message: 'Serverfehler beim Speichern.' });
  }
};

function json(code, obj) {
  return { statusCode: code,
    headers: { 'content-type': 'application/json; charset=utf-8' },
    body: JSON.stringify(obj) };
}
