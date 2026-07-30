# FTEM Ski Alpin – Athlet:innen-Weg Übersicht

Interaktive, durchsuchbare HTML-Übersicht des Ski-Alpin **Athlet:innen-Wegs** aus dem
Swiss-Ski FTEM-Tool: 17 Themen über die zehn Entwicklungsstufen **F1–M**
(Foundation → Talent → Elite → Mastery), inkl. der externen Dokument-Links.

Dieser Ordner enthält alles, um das Projekt weiterzuentwickeln.

---

## Inhalt des Ordners

| Datei | Zweck |
|---|---|
| `ftem-ski-alpin-uebersicht.html` | **Das fertige Resultat.** Einfach im Browser öffnen (Doppelklick). Läuft offline, keine Installation nötig. |
| `ftem_data.json` | **Die Datenquelle.** Alle Inhalte (Themen, Zeilen, Stufen-Zellen, Links) als strukturierte Daten. Hier wird der Inhalt bearbeitet. |
| `build.py` | **Der Generator.** Liest `ftem_data.json` und erzeugt daraus `ftem-ski-alpin-uebersicht.html`. Enthält das gesamte Layout (CSS) und die Interaktivität (JavaScript). |
| `README.md` | Diese Datei. |

---

## Schnellstart

**Nur ansehen:** `ftem-ski-alpin-uebersicht.html` doppelklicken.

**Etwas ändern und neu erzeugen:**

1. Voraussetzung: Python 3 (keine zusätzlichen Pakete nötig – nur Standardbibliothek).
2. Inhalt in `ftem_data.json` bearbeiten **oder** Layout/Verhalten in `build.py` anpassen.
3. Im Ordner ausführen:
   ```
   python3 build.py
   ```
4. `ftem-ski-alpin-uebersicht.html` wird neu geschrieben. Im Browser neu laden (Cmd/Ctrl+Shift+R).

---

## Aufbau der Daten (`ftem_data.json`)

```jsonc
{
  "stages": ["F1","F2","F3","T1","T2","T3","T4","E1","E2","M"],   // die 10 Stufen (Spalten)
  "themes": [
    {
      "title": "Kraft & Explosivität",          // Themenname (echtes "&", wird beim Build maskiert)
      "group": "Sport & Athlet:in",             // Gruppe: "Sport & Athlet:in" | "Material" | "Strukturen & Umfeld"
      "rows": [
        {
          "label": "Skills-Check ... Kraft",     // fixe Zeilen-Beschriftung links (oder null)
          "segs": [                               // Segmente = zusammengefasste Spalten
            {
              "v": "SC 1: Kniebeuge ...",         // Text der Zelle (\n = Zeilenumbruch)
              "from": 0,                          // erste Stufe (Index in "stages")
              "to": 1,                            // letzte Stufe (Zelle deckt Spalten from..to ab)
              "l": [                              // externe Links der Zelle (optional)
                { "text": "Skills-Check Kraft F1", "href": "https://snowsports.flink.host/s/..." }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

Wichtig:
- **Stufen-Spalten:** `from`/`to` sind Indizes in `stages` (0 = F1 … 9 = M). Ein Segment mit
  `"from":0,"to":1` ist eine Zelle, die F1 **und** F2 abdeckt (zusammengefasst). Pro Zeile müssen die
  Segmente zusammen genau die Spalten 0–9 abdecken.
- **`label`:** der wiederkehrende Vorspann jeder Zeile wird einmal links als fixe Beschriftung gezeigt
  (statt in jeder Zelle wiederholt). `null` = keine Beschriftung.
- **`l`:** Liste externer Dokumente. Wird als anklickbarer Button (📄) gerendert.

---

## Wie `build.py` Texte strukturiert

Der Zelltext (`v`) wird in `render_block()` automatisch aufbereitet:

- Zeilen mit `•` → Aufzählungsliste.
- Zeilen wie `SC 1: …`, `SC: …`, `ST: …` → Liste mit Badge.
- Kurze erste Zeile + Text darunter → fette Zwischenüberschrift + Absatz.
- `Label: Wert` → bei kurzem Wert inline (fettes Label), bei langem Wert als farbige
  Zwischenüberschrift (`.sh`) + Absatz darunter.

Anpassen lässt sich das in der Funktion `render_block()` in `build.py`.

---

## Funktionen der Seite

- **Volltextsuche** (oben) mit Treffer-Hervorhebung.
- **Sprung-Navigation** zu jedem Thema.
- **Alle öffnen / schließen.**
- **Lange Zellen** sind eingeklappt, per «mehr» ausklappbar.
- **Synchrones Seitwärts-Scrollen:** alle Themen-Tabellen scrollen horizontal gemeinsam.
- **Stufen-Highlight:** Klick auf einen Stufen-Kopf (z. B. „T2") färbt diese Spalte in allen
  Themen dezent in der Stufenfarbe ein (nochmal klicken = aus; mehrere möglich).
- Farbcodierung: Foundation (türkis), Talent (gold), Elite (orange), Mastery (rot).

Layout (CSS) und Verhalten (JS) stehen vollständig als Strings `CSS` und `JS` in `build.py`.

---

## Offene Punkte / Ideen für die Weiterarbeit

- **Podcast/Spotify-Icon:** Rechts neben jedem Titel ist ein grünes Podcast-Icon als reine
  Visualisierung eingebaut (noch **ohne Verknüpfung**). Echte Links können pro Thema ergänzt
  werden – z. B. ein neues Feld `"podcast": "https://..."` je Theme in `ftem_data.json`,
  das `build.py` dann im `<a href>` des Icons einsetzt.
- **Alterskategorien E1/E2/M:** Für diese Stufen war im FTEM-Tool keine Alterskategorie
  hinterlegt – sie sind im Stufen-Kopf entsprechend leer.
- **Externe Links** zeigen auf die Original-Dokumente (meist `snowsports.flink.host`-PDFs);
  deren Inhalte sind nicht eingebettet, sondern verlinkt.
- **Stufen-Filter** (nur eine Phase anzeigen) und ein **Druck-/PDF-Export** wären mögliche
  nächste Erweiterungen.

---

## Herkunft der Daten

Die Inhalte stammen aus dem (login-geschützten) Swiss-Ski FTEM-Dashboard
`my.ftem.swiss-ski.ch/dashboard/alpine-ski` → Ansicht „Athlet:innen-Weg".
Sie wurden einmalig aus der eingeloggten Browser-Ansicht ausgelesen und in `ftem_data.json`
strukturiert. Zum Aktualisieren bei künftigen Änderungen im Tool: die betroffenen Werte
direkt in `ftem_data.json` anpassen und `build.py` neu ausführen.
