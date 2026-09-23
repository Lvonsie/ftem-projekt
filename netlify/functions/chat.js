// FTEM KI-Assistent – serverseitiger Proxy zu Anthropic (Claude).
// Der API-Key liegt NUR hier (Netlify-Umgebungsvariable ANTHROPIC_API_KEY),
// niemals im Browser. Optional: CHAT_MODEL (Standard: claude-3-5-haiku-latest).

// --- Tageslimite pro IP -----------------------------------------------------
// Zaehler liegen in der bestehenden Supabase-Tabelle ftem_overrides
// (cid = "chatq|<hash>", txt = {"day":"YYYY-MM-DD","n":N}). Gespeichert wird
// nur ein Kurz-Hash der IP (keine Klartext-IPs). Die Seiten laden diese Zeilen
// nicht (cid=not.like.chatq|*). Faellt die Pruefung aus, laeuft der Chat weiter.
const QUOTA_URL = 'https://xphbwnzyebbejsdeqled.supabase.co/rest/v1/ftem_overrides';
// Nach der RLS-Umstellung darf nur noch der Server schreiben: service-role-
// Schluessel verwenden, sobald er als Netlify-Variable gesetzt ist.
const QUOTA_KEY = process.env.SUPABASE_SERVICE_KEY || 'sb_publishable_UQLqY8OqccllVy9t1FRlFQ_HZr_--D_';
const CHAT_LIMIT = parseInt(process.env.CHAT_DAILY_LIMIT || '10', 10);       // Fragen/Tag/IP
// Der Admin-Bereich (Modus "translate", KI-Uebersetzungsvorschlaege) hat KEINE Limite.
const LIMIT_MSG = {
  de: 'Tageslimite erreicht: Der FTEM-Coach beantwortet pro Tag maximal ' + CHAT_LIMIT + ' Fragen. Morgen geht es weiter – die Inhalte findest du jederzeit direkt auf dieser Seite.',
  fr: 'Limite quotidienne atteinte : le coach FTEM répond à ' + CHAT_LIMIT + ' questions par jour au maximum. À demain – les contenus restent disponibles directement sur cette page.',
  it: 'Limite giornaliero raggiunto: il coach FTEM risponde al massimo a ' + CHAT_LIMIT + ' domande al giorno. A domani – i contenuti restano disponibili direttamente su questa pagina.',
  en: 'Daily limit reached: the FTEM coach answers up to ' + CHAT_LIMIT + ' questions per day. See you tomorrow – all content remains available right on this page.'
};

async function ipQuota(event, kind, limit) {
  try {
    const crypto = require('crypto');
    const ip = String(event.headers['x-nf-client-connection-ip']
      || event.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
    const day = new Date().toISOString().slice(0, 10);
    const cid = 'chatq|' + crypto.createHash('sha256').update(kind + '|' + ip).digest('hex').slice(0, 20);
    const H = { apikey: QUOTA_KEY, Authorization: 'Bearer ' + QUOTA_KEY };
    let n = 0;
    const r = await fetch(QUOTA_URL + '?select=txt&cid=eq.' + encodeURIComponent(cid), { headers: H });
    if (r.ok) {
      const rows = await r.json();
      if (rows && rows[0] && rows[0].txt) {
        try { const q = JSON.parse(rows[0].txt); if (q.day === day) n = q.n || 0; } catch (_) {}
      }
    }
    if (n >= limit) return true;   // blockiert
    await fetch(QUOTA_URL, { method: 'POST',
      headers: { ...H, 'Content-Type': 'application/json', Prefer: 'resolution=merge-duplicates,return=minimal' },
      body: JSON.stringify([{ cid, txt: JSON.stringify({ day, n: n + 1 }) }]) });
    return false;
  } catch (_) { return false; }    // Limit-Pruefung darf den Chat nie lahmlegen
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return json(405, { error: 'method_not_allowed' });
  }
  const KEY = process.env.ANTHROPIC_API_KEY;
  if (!KEY) {
    return json(503, { error: 'not_configured',
      message: 'Der KI-Assistent ist noch nicht konfiguriert (API-Schlüssel fehlt).' });
  }

  let body;
  try { body = JSON.parse(event.body || '{}'); }
  catch { return json(400, { error: 'bad_request' }); }

  // ---- Modus "translate": KI-Uebersetzungsvorschlag fuer den Admin-Bereich ----
  // Eingabe: target (fr/it/en), de_new (neuer deutscher Text), optional de_old
  // (deutscher Text, gegen den die bisherige Uebersetzung geprueft war),
  // current (bisherige Uebersetzung) und glossary [{de,tr}].
  if (body.mode === 'translate') {
    // Schutz gegen Fremdnutzung: Ist die Netlify-Umgebungsvariable ADMIN_API_KEY
    // gesetzt, akzeptiert der Uebersetzungsmodus nur Anfragen aus dem Admin-Bereich
    // (der schickt das beim Login eingegebene Passwort mit). Ohne gesetzte Variable
    // verhaelt sich alles wie bisher.
    const NEED = process.env.ADMIN_API_KEY || '';
    if (NEED && String(body.key || '') !== NEED) {
      return json(401, { error: 'unauthorized', message: 'Nicht berechtigt (Admin-Anmeldung erforderlich).' });
    }
    const target = String(body.target || '').slice(0, 2);
    const tname = { fr: 'Französisch', it: 'Italienisch', en: 'Englisch' }[target];
    const deNew = String(body.de_new || '').slice(0, 6000).trim();
    const deOld = String(body.de_old || '').slice(0, 6000).trim();
    const cur   = String(body.current || '').slice(0, 6000).trim();
    const gl    = Array.isArray(body.glossary) ? body.glossary.slice(0, 60) : [];
    if (!tname || !deNew) return json(400, { error: 'bad_request' });
    const glList = gl.map(g => `- ${String(g.de || '').slice(0,120)} → ${String(g.tr || '').slice(0,120)}`).join('\n');
    const tsystem =
`Du übersetzt Fachinhalte des Swiss-Ski «Athlet:innen-Wegs» (FTEM, Schneesport) von Deutsch nach ${tname}.
Regeln:
- Halte dich STRIKT an das GLOSSAR (verbindliche Begriffe).
- Behalte Struktur und Formatierung exakt bei: Zeilenumbrüche, Leerzeilen, Aufzählungszeichen (•, -), "Label:"-Zeilen, Kürzel (SC, LT, ST, RS, SL, OLZ, On-Snow, Off-Snow) und Zahlen/Einheiten unverändert.
- Ist eine BISHERIGE ÜBERSETZUNG angegeben: übernimm deren Formulierungen überall, wo der deutsche Text gleich geblieben ist (vergleiche DEUTSCH VORHER mit DEUTSCH NEU), und übersetze nur die geänderten Stellen neu.
- Links in der Form [Text](URL): Text übersetzen, URL unverändert lassen.
- Gib NUR den übersetzten Text aus – keine Erklärungen, keine Anführungszeichen darum.

GLOSSAR (Deutsch → ${tname}):
${glList || '(keines)'}`;
    const tuser = 'DEUTSCH NEU:\n' + deNew
      + (deOld && deOld !== deNew ? '\n\nDEUTSCH VORHER:\n' + deOld : '')
      + (cur ? '\n\nBISHERIGE ÜBERSETZUNG:\n' + cur : '');
    try {
      const r = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: { 'x-api-key': KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
        body: JSON.stringify({
          model: process.env.CHAT_MODEL || 'claude-haiku-4-5-20251001',
          max_tokens: 1600,
          system: tsystem,
          messages: [{ role: 'user', content: tuser }]
        })
      });
      const data = await r.json();
      if (!r.ok) {
        return json(502, { error: 'upstream',
          message: (data && data.error && data.error.message) || 'Fehler beim Sprachmodell.' });
      }
      const answer = (data.content || []).map(c => c.text || '').join('').trim();
      return json(200, { answer });
    } catch (e) {
      return json(500, { error: 'server', message: 'Serverfehler bei der Übersetzung.' });
    }
  }

  const question = String(body.question || '').slice(0, 1500).trim();
  const context  = String(body.context  || '').slice(0, 120000);
  const sport    = String(body.sport    || '').slice(0, 80);
  const lang     = String(body.lang     || 'de').slice(0, 2);
  const links    = Array.isArray(body.links) ? body.links.slice(0, 60) : [];
  const history  = Array.isArray(body.history) ? body.history.slice(-6) : [];
  if (!question) return json(400, { error: 'no_question' });
  if (await ipQuota(event, 'chat', CHAT_LIMIT)) {
    return json(429, { error: 'limit', message: LIMIT_MSG[lang] || LIMIT_MSG.de });
  }

  const linkList = links.map(l => `- ${String(l.t || '').slice(0,160)}: ${String(l.u || '').slice(0,300)}`).join('\n');

  const langName = { de: 'Deutsch', fr: 'Französisch', it: 'Italienisch' }[lang] || 'Deutsch';
  const system =
`Du bist der FTEM-Assistent für den «Athlet:innen-Weg» von Swiss-Ski${sport ? ` (Sportart: ${sport})` : ''}.
Aufgabe: Fragen zum Athlet:innen-Weg beantworten – wie eine hilfreiche, fokussierte Suchmaschine über die FTEM-Inhalte.

Der KONTEXT deckt ALLE Bereiche des Athlet:innen-Wegs ab, u. a.:
- Sport & Athlet:in (Technik, Kraft, Ausdauer, Koordination, Taktik, Psyche, Ernährung, Schlaf, Testing, Periodisierung …)
- Material & Ausrüstung (Ski, Schuhe, Schutz, Bekleidung … pro Stufe)
- Strukturen & Umfeld (Kader, Wettkämpfe, Umfeld, Finanzen, Schule/Ausbildung …)
Behandle ALLE diese Themen als deinen Aufgabenbereich. Erkläre NIEMALS ein Thema als "ausserhalb meines Bereichs", wenn die Information im Kontext steht – such sie stattdessen dort.

Regeln:
- Antworte AUSSCHLIESSLICH auf Basis des unten bereitgestellten KONTEXTS (FTEM-Inhalte). Erfinde nichts.
- Nutze die Stufen-Struktur (F1–F3, T1–T4, E1–E2, M), wenn die Frage eine Stufe nennt.
- Steht die Antwort wirklich nicht im Kontext, sage das ehrlich und schlage – wenn passend – ein oder mehrere der VERLINKTEN DOKUMENTE vor (nenne Titel und vollständige URL).
- Wenn ein verlinktes Dokument die Frage vertiefen könnte, empfiehl es aktiv am Ende der Antwort.
- Fasse dich kurz und klar. Nutze bei Aufzählungen Stichpunkte. Kein Markdown-Fettdruck (**), einfacher Text.
- Antworte in ${langName} (bzw. in der Sprache der Frage).

VERLINKTE DOKUMENTE:
${linkList || '(keine)'}

KONTEXT (FTEM Athlet:innen-Weg${sport ? ' – ' + sport : ''}):
${context || '(kein Kontext übermittelt)'}`;

  const messages = [];
  for (const m of history) {
    if (m && (m.role === 'user' || m.role === 'assistant') && m.content) {
      messages.push({ role: m.role, content: String(m.content).slice(0, 4000) });
    }
  }
  messages.push({ role: 'user', content: question });

  try {
    const r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
      },
      body: JSON.stringify({
        model: process.env.CHAT_MODEL || 'claude-haiku-4-5-20251001',
        max_tokens: 800,
        system,
        messages
      })
    });
    const data = await r.json();
    if (!r.ok) {
      return json(502, { error: 'upstream',
        message: (data && data.error && data.error.message) || 'Fehler beim Sprachmodell.' });
    }
    // Markdown-Fettdruck entfernen: Das Chatfenster zeigt reinen Text, sonst
    // erscheinen die Sternchen woertlich (das Modell haelt sich nicht immer an
    // die Anweisung "kein **").
    const answer = (data.content || []).map(c => c.text || '').join('').trim().replace(/\*\*/g, '');
    // Statistik: 1 Zeile pro beantworteter Frage (serverseitig -> nicht verfaelschbar).
    // Fehlt die Tabelle ftem_stats, passiert still nichts.
    try {
      await fetch(QUOTA_URL.replace('ftem_overrides', 'ftem_stats'), { method: 'POST',
        headers: { apikey: QUOTA_KEY, Authorization: 'Bearer ' + QUOTA_KEY,
          'Content-Type': 'application/json', Prefer: 'return=minimal' },
        body: JSON.stringify({ kind: 'ki_frage', meta: lang }) });
    } catch (_) {}
    return json(200, { answer: answer || 'Dazu habe ich leider keine Antwort gefunden.' });
  } catch (e) {
    return json(500, { error: 'server', message: 'Serverfehler beim KI-Assistenten.' });
  }
};

function json(code, obj) {
  return {
    statusCode: code,
    headers: { 'content-type': 'application/json; charset=utf-8' },
    body: JSON.stringify(obj)
  };
}
