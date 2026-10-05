// Taegliches Backup der Datenbank-Inhalte ins Repo (Ordner backup/).
// Gesichert werden alle drei Tabellen:
//   ftem_overrides  - von Admins gespeicherte Zell-Texte und Uebersetzungen
//   ftem_feedback   - Rueckmeldungen der Besucher:innen
//   ftem_stats      - Nutzungsstatistik
// Der Commit passiert nur, wenn sich etwas geaendert hat; die komplette
// Historie steckt danach in der Git-Versionsgeschichte (Wiederherstellung
// jedes frueheren Standes jederzeit moeglich).
// Bei Fehlern: Warn-Mail via Resend + roter Lauf auf GitHub.

import { writeFileSync, mkdirSync } from 'node:fs';
import { warnmail } from './_mail.mjs';

// FTEM_SUPA nur fuer lokale Tests mit Mock-Server uebersteuerbar
const SUPA = process.env.FTEM_SUPA || 'https://xphbwnzyebbejsdeqled.supabase.co';
// Oeffentlicher Lese-Schluessel (steht auch im HTML der Seite - kein Geheimnis)
const ANON = 'sb_publishable_UQLqY8OqccllVy9t1FRlFQ_HZr_--D_';

const TABELLEN = [
  ['ftem_overrides', 'cid'],
  ['ftem_feedback', 'id'],
  ['ftem_stats', 'id'],
];

async function alleZeilen(tabelle, ordnen) {
  const zeilen = [];
  for (let offset = 0; ; offset += 1000) {
    const r = await fetch(
      `${SUPA}/rest/v1/${tabelle}?select=*&order=${ordnen}.asc&limit=1000&offset=${offset}`,
      { headers: { apikey: ANON, authorization: `Bearer ${ANON}` },
        signal: AbortSignal.timeout(60000) });
    if (!r.ok) throw new Error(`${tabelle}: HTTP ${r.status}`);
    const teil = await r.json();
    zeilen.push(...teil);
    if (teil.length < 1000) break;
  }
  return zeilen;
}

try {
  mkdirSync('backup', { recursive: true });
  for (const [tabelle, ordnen] of TABELLEN) {
    const zeilen = await alleZeilen(tabelle, ordnen);
    // Stabil formatiert (eine Zeile pro Datensatz) -> kleine, lesbare Git-Diffs
    const txt = '[\n' + zeilen.map(z => JSON.stringify(z)).join(',\n') + '\n]\n';
    writeFileSync(`backup/${tabelle}.json`, txt);
    console.log(`${tabelle}: ${zeilen.length} Datensaetze gesichert`);
    if (tabelle === 'ftem_overrides' && zeilen.length === 0) {
      // Leere Override-Tabelle waere hoechst verdaechtig (Datenverlust?)
      throw new Error('ftem_overrides ist ploetzlich LEER - moeglicher Datenverlust, bitte pruefen!');
    }
  }
} catch (e) {
  console.error('Backup fehlgeschlagen:', e);
  await warnmail('⚠️ FTEM-Seite: tägliches Backup fehlgeschlagen',
    ['Das automatische Datenbank-Backup konnte nicht erstellt werden: ' + ((e && e.message) || e)]);
  process.exit(1);
}
console.log('Backup vollstaendig.');
