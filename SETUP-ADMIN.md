# Admin-Bereich einrichten (direktes Live-Speichern)

Der Admin-Bereich (`admin.html`, Schloss-Icon unten auf der Startseite) funktioniert **sofort** –
man kann sich mit dem Passwort anmelden und Texte bearbeiten. Damit Änderungen **direkt gespeichert
und für alle live** werden, braucht es einen kleinen kostenlosen Cloud-Speicher: **Supabase**.
Das ist eine einmalige Einrichtung (ca. 10 Minuten).

## Passwort

Aktuell: `ftem26*` – änderbar in `build.py` bei `ADMIN_PW`.
(Hinweis: Das ist ein einfacher Schutz per JavaScript, kein Hochsicherheits-Login. Für einen
internen Kreis von 5–10 Personen ist das ok; das Passwort ist technisch im Seitenquelltext sichtbar.)

## Schritt für Schritt: Supabase verbinden

1. Auf **https://supabase.com** kostenlos registrieren und ein **neues Projekt** anlegen
   (Name frei, Region z. B. „Central EU / Frankfurt", ein Datenbank-Passwort vergeben – das brauchst
   du hier nicht weiter).

2. Links im Menü **SQL Editor** öffnen, folgendes einfügen und **Run** klicken – das legt die
   Tabelle an und erlaubt Lesen/Schreiben mit dem öffentlichen Schlüssel:

   ```sql
   create table if not exists ftem_overrides (
     cid text primary key,
     txt text,
     updated_at timestamptz default now()
   );
   alter table ftem_overrides enable row level security;
   create policy "read"  on ftem_overrides for select using (true);
   create policy "write" on ftem_overrides for insert with check (true);
   create policy "update" on ftem_overrides for update using (true) with check (true);

   -- Glossar (neue Begriffe, die im Admin hinzugefügt werden)
   create table if not exists ftem_glossary (
     de text primary key,
     fr text,
     updated_at timestamptz default now()
   );
   alter table ftem_glossary enable row level security;
   create policy "g_read"   on ftem_glossary for select using (true);
   create policy "g_write"  on ftem_glossary for insert with check (true);
   create policy "g_update" on ftem_glossary for update using (true) with check (true);

   -- Feedback (Rückmeldungen von der Startseite; anonym oder mit Name/Verband/E-Mail)
   create table if not exists ftem_feedback (
     id uuid primary key default gen_random_uuid(),
     created_at timestamptz default now(),
     message text not null,
     anonymous boolean default true,
     name text,
     verband text,
     email text,
     lang text,
     page text,
     done boolean default false
   );
   alter table ftem_feedback enable row level security;
   create policy "f_insert" on ftem_feedback for insert with check (true);
   create policy "f_read"   on ftem_feedback for select using (true);
   create policy "f_update" on ftem_feedback for update using (true) with check (true);
   ```

3. Links **Project Settings → API** öffnen und zwei Werte kopieren:
   - **Project URL** (z. B. `https://abcdxyz.supabase.co`)
   - **anon public** Key (langer Schlüssel unter „Project API keys")

4. In `build.py` ganz oben eintragen:

   ```python
   SUPABASE_URL      = "https://abcdxyz.supabase.co"
   SUPABASE_ANON_KEY = "der-lange-anon-key"
   ```

5. `python3 build.py` ausführen, dann in GitHub Desktop **committen und pushen**.
   Nach dem automatischen Netlify-Rebuild ist alles aktiv.

## So funktioniert es danach

- **Bearbeiten:** Schloss-Icon unten auf der Startseite → Passwort → Texte in den Feldern ändern →
  **„Alle Änderungen speichern"**. Die Änderung landet sofort im Cloud-Speicher.
- **Live:** Beim nächsten Laden (oder Reload) der Seite werden die gespeicherten Texte automatisch
  angezeigt – für alle Besucher:innen.
- Es werden **nur Texte** überschrieben (Tippfehler, Ergänzungen). Struktur, Spalten und Aufbau
  bleiben unverändert.

## Solange Supabase noch nicht eingerichtet ist

Der Admin-Bereich läuft trotzdem: Man kann bearbeiten und die Änderungen als Datei
(`ftem-aenderungen.json`) herunterladen. Erst nach der Supabase-Einrichtung wird direkt live
gespeichert.

## Hinweis zu den Sprachen

Bearbeitet wird der deutsche Grundtext. Eine geänderte Zelle erscheint (bis zu einer separaten
Übersetzung) auf allen Sprachversionen mit dem bearbeiteten deutschen Text.

## Übersetzungen prüfen (Markierung)

Wird eine Zelle im **Deutschen** geändert und gespeichert, erscheint dieselbe Zelle beim Umschalten
auf FR/IT/EN **orange markiert** – als Erinnerung, die Übersetzung zu kontrollieren. Beim Hovern über
das orange „!" wird direkt angezeigt, **was** sich im Deutschen geändert hat (grün = neu, rot
durchgestrichen = entfernt), ohne die Sprache wechseln zu müssen. Nach dem Anpassen und Speichern der
Übersetzung verschwindet die Markierung; ist die Übersetzung trotz der Änderung noch korrekt, klickt
man auf das „!" („als geprüft markieren"). Dieser Prüf-Status wird in der bestehenden
`ftem_overrides`-Tabelle mitgespeichert (Zeilen mit `cid` = `rev|…`) – keine zusätzliche Tabelle nötig.

## Feedback-Eingänge

Das Feedback-Formular auf der Startseite speichert Rückmeldungen direkt in Supabase
(Tabelle `ftem_feedback`) – **kein Mailprogramm** mehr. Besucher:innen können **anonym** senden oder
optional **Name, Verband und E-Mail** angeben.

Im Admin-Bereich gibt es oben den Knopf **„Feedback"** (mit rotem Zähler offener Einträge). Dort sind
alle Rückmeldungen chronologisch gelistet. Jeder Eintrag lässt sich per **„✓ Erledigt"** als bearbeitet
markieren bzw. mit **„↺ Wieder öffnen"** zurücksetzen; mit dem Filter **„nur offene"** blendet man
erledigte aus. Beim **Einloggen** erscheint zudem ein kurzes **Pop-up**, wenn offene (noch nicht
erledigte) Feedbacks vorliegen.

Datenschutz-Hinweis: Wie beim übrigen Cloud-Speicher wird für Lesen/Schreiben der öffentliche
`anon`-Schlüssel verwendet. Feedback-Einträge (inkl. optional angegebener Kontaktdaten) sind damit
technisch über diesen Schlüssel lesbar – bewusst keine hochsensiblen Daten dort ablegen.
