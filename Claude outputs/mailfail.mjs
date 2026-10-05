// Kleiner Helfer: schickt eine Warn-Mail mit dem uebergebenen Text.
// Wird von den Workflows benutzt, wenn ein Schritt ausserhalb der
// eigentlichen Skripte fehlschlaegt (z.B. das Speichern des Backups).
import { warnmail } from './_mail.mjs';
const [betreff, ...zeilen] = process.argv.slice(2);
await warnmail(betreff || '⚠️ FTEM-Überwachung: Lauf fehlgeschlagen',
  zeilen.length ? zeilen : ['Ein Automatik-Lauf ist fehlgeschlagen - Details im GitHub-Protokoll.']);
