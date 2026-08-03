# FTEM KI-Assistent – Einrichtung

Der Chat-Button (Sprechblase mit Funken) im Header jeder Sportart öffnet einen
KI-Assistenten. Er beantwortet Fragen **auf Basis der FTEM-Inhalte der aktuellen
Sportart** und verweist bei Bedarf auf die **verlinkten Dokumente**.

Damit er funktioniert, braucht es einen API-Schlüssel. Dieser liegt **nur auf dem
Server** (Netlify Function `netlify/functions/chat.js`), niemals im Browser.

## 1. Anthropic API-Key besorgen
1. Konto erstellen/anmelden auf https://console.anthropic.com
2. Unter **API Keys** einen neuen Schlüssel erzeugen (beginnt mit `sk-ant-…`).
3. Etwas Guthaben hinterlegen (Billing). Das günstige Modell «Haiku» kostet nur
   Bruchteile eines Rappens pro Frage.

## 2. Schlüssel in Netlify hinterlegen
1. Netlify → **Site configuration → Environment variables**
2. Neue Variable:
   - **Key:** `ANTHROPIC_API_KEY`
   - **Value:** dein `sk-ant-…`
3. Optional, um ein anderes Modell zu nutzen:
   - **Key:** `CHAT_MODEL` – z. B. `claude-3-5-haiku-latest` (Standard) oder ein
     stärkeres Modell wie `claude-3-5-sonnet-latest` (teurer, ausführlicher).
4. **Redeploy** auslösen (Deploys → Trigger deploy), damit die Variable greift.

Die Functions sind bereits in `netlify.toml` konfiguriert – du musst nichts weiter tun.

## 3. Testen
- Seite öffnen → eine Sportart → Chat-Button im Header → Frage stellen.
- Ist kein Key gesetzt, meldet der Assistent freundlich, dass er noch nicht
  konfiguriert ist (die Website bleibt sonst voll funktionsfähig).

## Wie es funktioniert
- Der Browser sammelt die sichtbaren FTEM-Inhalte der aktuellen Sportart
  (Themen, Zeilen, Zellen) und die Liste der verlinkten Dokumente.
- Diese werden an die Netlify Function geschickt, die daraus einen Prompt baut
  und Claude fragt. Der Systemprompt zwingt das Modell, **nur aus dem Kontext**
  zu antworten und sonst auf die Links zu verweisen (keine erfundenen Fakten).
- Die Antwort erscheint im Chat-Panel; erwähnte URLs werden klickbar.

## Datenschutz / Kosten
- Fragen und der übermittelte Inhalt gehen an Anthropic (USA) zur Verarbeitung.
  Für eine Swiss-Ski-Lösung ggf. mit dem Datenschutz abklären. Es werden keine
  personenbezogenen Daten übertragen – nur die öffentlichen FTEM-Inhalte und die
  frei gestellte Frage.
- Kosten entstehen pro Anfrage (bei Haiku sehr gering). Du kannst in der Anthropic
  Console ein Ausgabenlimit setzen.

## Erweiterung (Phase 2)
Aktuell schlägt der Bot die verlinkten Dokumente vor. Wenn er deren **Inhalt**
selbst lesen soll (PDFs, externe Seiten), braucht es einen Crawler/Index – das
ist ein separater Ausbauschritt. Sag Bescheid, wenn du das möchtest.
