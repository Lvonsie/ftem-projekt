# -*- coding: utf-8 -*-
"""
Konvertiert ein FTEM-Tool Import-Excel (Sheet "detail") in unser JSON-Format.

Aufruf:  python3 convert_xlsx.py <datei.xlsx> <sportart-id>
Ergebnis: ftem_data_<sportart-id>.json im Projektordner

Regeln:
- Sheet "detail": Spalten = Topic-Key, Topic, Topic-Group, SubTopic-Key, SubTopic,
  SortKey, dann die 10 Stufen F1..M (Spalten 7-16).
- "Alterskategorie" wird NICHT als Thema uebernommen, sondern als "ages"
  (Beschriftung der Stufen-Koepfe) gespeichert.
- Gruppen-Zuordnung: training -> "Sport & Athlet:in";
  Material/equipment -> "Material"; alles andere -> "Strukturen & Umfeld".
- Benachbarte Stufen-Zellen mit identischem Text werden zu einem Segment
  zusammengefasst (zusammengefasste Spalten wie im FTEM-Tool).
- "-" oder leere Zellen gelten als leer.
"""
import sys, os, json, re
import openpyxl

BASE = os.path.dirname(os.path.abspath(__file__))
STAGES = ["F1","F2","F3","T1","T2","T3","T4","E1","E2","M"]

def clean(v):
    if v is None: return ""
    s = str(v).replace("\r\n","\n").replace("\r","\n")
    s = re.sub(r'[ \t]+\n', '\n', s)          # Leerzeichen vor Zeilenumbruch
    s = re.sub(r'\n{3,}', '\n\n', s)          # max. eine Leerzeile
    s = s.strip()
    if s in ("-", "–", "—"): return ""
    return s

def group_of(topic_key, topic, group_key):
    if topic_key == "equipment" or topic.strip() == "Material":
        return "Material"
    if group_key == "training":
        return "Sport & Athlet:in"
    return "Strukturen & Umfeld"

def convert(xlsx_path, sport_id):
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    ws = wb["detail"]
    themes = []          # in Reihenfolge des Excels
    by_title = {}
    ages = {}
    for r in range(2, ws.max_row + 1):
        topic = clean(ws.cell(r, 2).value)
        if not topic:
            continue
        topic_key = clean(ws.cell(r, 1).value)
        group_key = clean(ws.cell(r, 3).value)
        label = clean(ws.cell(r, 5).value)
        cells = [clean(ws.cell(r, c).value) for c in range(7, 17)]
        if topic == "Alterskategorie":
            for i, s in enumerate(STAGES):
                ages[s] = cells[i].replace("\n", " ").strip()
            continue
        if topic not in by_title:
            t = {"title": topic, "group": group_of(topic_key, topic, group_key), "rows": []}
            by_title[topic] = t
            themes.append(t)
        # Segmente: benachbarte identische Zellen zusammenfassen
        segs = []
        for i, v in enumerate(cells):
            if segs and segs[-1]["v"] == v:
                segs[-1]["to"] = i
            else:
                segs.append({"v": v, "from": i, "to": i, "l": []})
        by_title[topic]["rows"].append({"label": label or None, "segs": segs})
    data = {"stages": STAGES, "ages": ages, "themes": themes}
    out = os.path.join(BASE, "ftem_data_" + sport_id + ".json")
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n_rows = sum(len(t["rows"]) for t in themes)
    print("written", os.path.basename(out), "| themes:", len(themes), "| rows:", n_rows, "| ages:", bool(ages))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
