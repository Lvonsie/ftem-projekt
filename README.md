# FTEM – Athlet:innen-Weg (Swiss-Ski)

Interaktive, durchsuchbare Übersicht der **Athlet:innen-Wege** aus dem Swiss-Ski FTEM-Tool:
Startseite mit Sportart-Auswahl (9 Sportarten), pro Sportart die Themen über die zehn
Entwicklungsstufen **F1–M**, in drei Sprachen (DE/FR/IT).

---

## ⚠️ Das Wichtigste zuerst: Was wird bearbeitet, was wird generiert?

**Es gibt genau eine Quelle der Wahrheit – die HTML-Dateien werden IMMER generiert und nie von Hand bearbeitet.**

| | Dateien | Bearbeiten? |
|---|---|---|
| **Quellen** (hier arbeiten) | `build.py`, `ftem_data_<sportart>.json`, `ftem_sports.json`, `translations.json`, `icons/` | ✅ ja |
| **Ausgaben** (generiert) | `index.html` (DE), `fr.html`, `it.html` | ❌ nie von Hand! |

Jede Änderung direkt in einer HTML-Datei geht beim nächsten `python3 build.py` **verloren**.
Deshalb gilt: Quelle ändern → `python3 build.py` ausführen → alle drei HTML werden neu geschrieben →
alles zusammen committen. So laufen keine zwei Stände nebeneinander.

---

## Die Quell-Dateien im Detail

| Datei | Zweck |
|---|---|
| `build.py` | **Der Generator.** Enthält Layout (CSS), Interaktivität (JS) und den ganzen Seitenaufbau. Liest alle JSON-Dateien und schreibt `index.html`, `fr.html`, `it.html`. |
| `ftem_sports.json` | **Die Sportarten-Liste** (Reihenfolge, Namen, Kürzel, Icon-Pfad). Neue Sportart = hier ein Eintrag. |
| `ftem_data_<sportart>.json` | **Inhalte pro Sportart** (Themen, Zeilen, Stufen-Zellen, Alterskategorien), z. B. `ftem_data_ski-alpin.json`. Solange die Datei fehlt, zeigt die Sportart «Inhalte folgen». |
| `translations.json` | **Übersetzungen FR/IT** als einfache Text-Paare (deutscher Text → Übersetzung). Nicht übersetzte Texte erscheinen auf Deutsch. |
| `convert_xlsx.py` | **Excel-Import:** wandelt ein FTEM-Tool-Import-Excel in eine `ftem_data_<sportart>.json` um. Aufruf: `python3 convert_xlsx.py datei.xlsx sportart-id` |
| `icons/` | Sportarten-Icons (rote Piktogramme). Zuordnung über das Feld `"icon"` in `ftem_sports.json`; `reserve-*.jpg` sind noch nicht zugeteilt. |

## Die generierten Dateien

- `index.html` – Deutsch (zugleich Einstieg der Website / Netlify-Wurzel)
- `fr.html` – Französisch, `it.html` – Italienisch
- Alles in **einer Datei pro Sprache**: Startseite + alle Sportarten, Wechsel per Klick (`#ski-alpin` usw.),
  Browser-Zurück funktioniert, Sprachwechsel behält die gewählte Sportart.

---

## Typische Arbeitsabläufe

**Inhalt ändern (z. B. Text in einer Zelle):**
1. In `ftem_data.json` (bzw. `ftem_data_<sportart>.json`) anpassen
2. `python3 build.py`
3. Committen (JSON **und** die drei HTML zusammen)

**Neue Sportart mit Inhalt füllen:**
1. `ftem_data_<sportart>.json` anlegen (Format von `ftem_data.json` übernehmen)
2. `python3 build.py` – die Karte auf der Startseite wird automatisch aktiv

**Übersetzung ergänzen/korrigieren:**
1. In `translations.json` unter `"fr"` bzw. `"it"` das Paar `"Deutscher Text": "Übersetzung"` ergänzen
2. `python3 build.py`

**Layout/Design ändern (Farben, Abstände, Verhalten):**
1. In `build.py` im `CSS`- oder `JS`-String anpassen
2. `python3 build.py`

**Voraussetzung:** Python 3, keine Zusatzpakete. Ansehen: `index.html` doppelklicken (läuft offline).

---

## Funktionen der Seite

- Startseite mit **Sportart-Auswahl** (Karten; grau = noch ohne Inhalt), Sprachumschalter **DE | FR | IT**
- Pro Sportart: **Volltextsuche** mit Hervorhebung, **Sprung-Navigation**, Alle öffnen/schliessen,
  «mehr»-Ausklappen langer Zellen, **synchrones Seitwärts-Scrollen**, **Stufen-Highlight**
  (Klick auf Stufen-Kopf färbt die Spalte), «← Sportarten»-Button zurück zur Auswahl
- Farbcodierung: Foundation (türkis), Talent (gold), Elite (orange), Mastery (rot) –
  auch im **FTEM**-Schriftzug

---

## Aufbau der Inhalts-Daten (`ftem_data*.json`)

```jsonc
{
  "stages": ["F1","F2","F3","T1","T2","T3","T4","E1","E2","M"],
  "themes": [
    {
      "title": "Kraft & Explosivität",
      "group": "Sport & Athlet:in",        // Gruppe: "Sport & Athlet:in" | "Material" | "Strukturen & Umfeld"
      "rows": [
        {
          "label": "Skills-Check Kraft",    // fixe Zeilen-Beschriftung links (oder null)
          "segs": [                          // Segmente = zusammengefasste Stufen-Spalten
            {
              "v": "SC 1: Kniebeuge …",      // Zelltext (\n = Zeilenumbruch)
              "from": 0, "to": 1,            // Stufen-Indizes (0 = F1 … 9 = M), müssen pro Zeile 0–9 lückenlos abdecken
              "l": [ { "text": "Skills-Check Kraft F1", "href": "https://…" } ]   // externe Links (optional)
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Herkunft der Daten

Inhalte aus dem (login-geschützten) Swiss-Ski FTEM-Dashboard `my.ftem.swiss-ski.ch`.
Bei Änderungen im Tool: betroffene Werte in der jeweiligen `ftem_data*.json` anpassen
und `python3 build.py` ausführen.
