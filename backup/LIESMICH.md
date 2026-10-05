# Automatisches Datenbank-Backup

In diesen Ordner legt die GitHub Action **«Daten-Backup»** (`.github/workflows/daten-backup.yml`)
jede Nacht um ca. 03:23/04:23 Schweizer Zeit den aktuellen Stand der Datenbank:

| Datei | Inhalt |
|---|---|
| `ftem_overrides.json` | Alle von Admins gespeicherten Zell-Texte und Übersetzungen (das Wertvollste!) |
| `ftem_feedback.json` | Rückmeldungen der Besucher:innen |
| `ftem_stats.json` | Nutzungsstatistik |

Committet wird nur, wenn sich etwas geändert hat. Dadurch liegt in der
Git-Historie dieses Ordners **jeder frühere Stand** – ein versehentlich
gelöschter oder überschriebener Admin-Text lässt sich jederzeit zurückholen
(in GitHub Desktop: History → Datei anschauen, oder einfach Claude bitten,
einen bestimmten Stand wiederherzustellen).

Schlägt das Backup fehl, geht automatisch eine Warn-Mail an Michael
(Versand über Resend, GitHub-Secret `RESEND_API_KEY`).
