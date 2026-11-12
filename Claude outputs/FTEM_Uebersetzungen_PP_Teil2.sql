-- FTEM Übersetzungen P&P – Teil 2 von 3 (150 Einträge)
begin;
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|0|4|en$c$, $t$SC 1: running drills
SC 2: sprint (30 m & 80 m)
SC 3: 100× single unders, 30× double unders in a row
SC 4: acceleration 10 m and 20 m flying
SC 5: stop-and-go 5-10-5 and 5-0-5
ST: Swiss-Ski Power Test (SSPT) or youth performance tests

[Skills-Check T3](https://snowsports.flink.host/s/mV4adYMV/wMSkh6GC)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|0|4|en$c$, $t$SC 1: Lauf-ABC
SC 2: Sprint (30 m & 80 m)
SC 3: 100× Einfachdurchzüge, 30× Doppeldurchzüge am Stück
SC 4: Antritt 10 m und 20 m fliegend
SC 5: Stop-and-Go 5-10-5 und 5-0-5
ST: Swiss-Ski Power Test (SSPT) oder Nachwuchsleistungstests

[T3 Skills-Check](https://snowsports.flink.host/s/mV4adYMV/wMSkh6GC)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|0|5|fr$c$, $t$SC 1 : ABC de la course
SC 2 : sprint (30 m & 100 m)
SC 3 : 100× sauts simples, 40× doubles sauts d'affilée
SC 4 : perte de temps lors du changement de direction (déficit COD)
SC 5 : série de sprints 3 × 60 m
ST : tests de performance de la relève
[Skills-Check T4](https://snowsports.flink.host/s/mV4adYMV/Y2sDwELc)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|0|5|fr$c$, $t$SC 1: Lauf-ABC
SC 2: Sprint (30 m & 100 m)
SC 3: 100× Einfachdurchzüge, 40× Doppeldurchzüge am Stück
SC 4: Zeitverlust beim Richtungswechsel (COD-Defizit)
SC 5: Sprintserie 3 × 60 m
ST: Nachwuchsleistungstests
[T4 Skills-Check](https://snowsports.flink.host/s/mV4adYMV/Y2sDwELc)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|0|5|it$c$, $t$SC 1: ABC della corsa
SC 2: sprint (30 m & 100 m)
SC 3: 100× salti semplici, 40× salti doppi di fila
SC 4: perdita di tempo nel cambio di direzione (deficit COD)
SC 5: serie di sprint 3 × 60 m
ST: test di prestazione per giovani
[Skills-Check T4](https://snowsports.flink.host/s/mV4adYMV/Y2sDwELc)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|0|5|it$c$, $t$SC 1: Lauf-ABC
SC 2: Sprint (30 m & 100 m)
SC 3: 100× Einfachdurchzüge, 40× Doppeldurchzüge am Stück
SC 4: Zeitverlust beim Richtungswechsel (COD-Defizit)
SC 5: Sprintserie 3 × 60 m
ST: Nachwuchsleistungstests
[T4 Skills-Check](https://snowsports.flink.host/s/mV4adYMV/Y2sDwELc)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|0|5|en$c$, $t$SC 1: running drills
SC 2: sprint (30 m & 100 m)
SC 3: 100× single unders, 40× double unders in a row
SC 4: time lost when changing direction (COD deficit)
SC 5: sprint series 3 × 60 m
ST: youth performance tests
[Skills-Check T4](https://snowsports.flink.host/s/mV4adYMV/Y2sDwELc)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|0|5|en$c$, $t$SC 1: Lauf-ABC
SC 2: Sprint (30 m & 100 m)
SC 3: 100× Einfachdurchzüge, 40× Doppeldurchzüge am Stück
SC 4: Zeitverlust beim Richtungswechsel (COD-Defizit)
SC 5: Sprintserie 3 × 60 m
ST: Nachwuchsleistungstests
[T4 Skills-Check](https://snowsports.flink.host/s/mV4adYMV/Y2sDwELc)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|0|6|fr$c$, $t$SC 1 : sprint 40 m (10/20/30 m) et 20 m lancé
SC 2 : stop-and-go 5-10-5 et perte de temps lors du changement de direction
SC 3 : série de sprints 3 × 60 m (chronométrée)
ST : tests de performance de la relève ou diagnostic de performance Macolin
[Skills-Check E](https://snowsports.flink.host/s/mV4adYMV/Feg3YPuP)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|0|6|fr$c$, $t$SC 1: Sprint 40 m (10/20/30 m) und 20 m fliegend
SC 2: Stop-and-Go 5-10-5 und Zeitverlust beim Richtungswechsel
SC 3: Sprintserie 3 × 60 m (gemessen)
ST: Nachwuchsleistungstests oder Leistungsdiagnostik Magglingen
[E Skills-Check](https://snowsports.flink.host/s/mV4adYMV/Feg3YPuP)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|0|6|it$c$, $t$SC 1: sprint 40 m (10/20/30 m) e 20 m lanciati
SC 2: stop-and-go 5-10-5 e perdita di tempo nel cambio di direzione
SC 3: serie di sprint 3 × 60 m (cronometrata)
ST: test di prestazione per giovani o diagnostica della prestazione Macolin
[Skills-Check E](https://snowsports.flink.host/s/mV4adYMV/Feg3YPuP)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|0|6|it$c$, $t$SC 1: Sprint 40 m (10/20/30 m) und 20 m fliegend
SC 2: Stop-and-Go 5-10-5 und Zeitverlust beim Richtungswechsel
SC 3: Sprintserie 3 × 60 m (gemessen)
ST: Nachwuchsleistungstests oder Leistungsdiagnostik Magglingen
[E Skills-Check](https://snowsports.flink.host/s/mV4adYMV/Feg3YPuP)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|0|6|en$c$, $t$SC 1: sprint 40 m (10/20/30 m) and 20 m flying
SC 2: stop-and-go 5-10-5 and time lost when changing direction
SC 3: sprint series 3 × 60 m (timed)
ST: youth performance tests or performance diagnostics Magglingen
[Skills-Check E](https://snowsports.flink.host/s/mV4adYMV/Feg3YPuP)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|0|6|en$c$, $t$SC 1: Sprint 40 m (10/20/30 m) und 20 m fliegend
SC 2: Stop-and-Go 5-10-5 und Zeitverlust beim Richtungswechsel
SC 3: Sprintserie 3 × 60 m (gemessen)
ST: Nachwuchsleistungstests oder Leistungsdiagnostik Magglingen
[E Skills-Check](https://snowsports.flink.host/s/mV4adYMV/Feg3YPuP)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|0|7|fr$c$, $t$ST : diagnostic de performance Macolin et individuellement en accord avec l'entraîneur·e d'athlétisme

[Skills-Check M](https://snowsports.flink.host/s/mV4adYMV/Feg3YPuP)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|0|7|fr$c$, $t$ST: Leistungsdiagnostik Magglingen und individuell nach Absprache mit dem/der Athletiktrainer:in

[M Skills-Check](https://snowsports.flink.host/s/mV4adYMV/Feg3YPuP)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|0|7|it$c$, $t$ST: diagnostica della prestazione Macolin e individualmente d'intesa con l'allenatore/allenatrice atletico/a

[Skills-Check M](https://snowsports.flink.host/s/mV4adYMV/Feg3YPuP)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|0|7|it$c$, $t$ST: Leistungsdiagnostik Magglingen und individuell nach Absprache mit dem/der Athletiktrainer:in

[M Skills-Check](https://snowsports.flink.host/s/mV4adYMV/Feg3YPuP)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|0|7|en$c$, $t$ST: performance diagnostics Magglingen and individually in agreement with the athletic coach

[Skills-Check M](https://snowsports.flink.host/s/mV4adYMV/Feg3YPuP)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|0|7|en$c$, $t$ST: Leistungsdiagnostik Magglingen und individuell nach Absprache mit dem/der Athletiktrainer:in

[M Skills-Check](https://snowsports.flink.host/s/mV4adYMV/Feg3YPuP)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|0|fr$c$, $t$Vitesse :
Courir vite, attraper et esquiver dans des jeux.
Les enfants doivent avoir du plaisir à être rapides et découvrir de nombreux mouvements différents.
Un esprit de compétition est permis, p. ex. qui arrive en premier ?

Au fil de la saison :
Pas de planification de saison.
Toute l'année pareil, quelques minutes à chaque entraînement, toujours de manière ludique et au début de l'entraînement.

[Contenu F1](https://snowsports.flink.host/s/V9p4Capq/Lj2wygXM)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|0|fr$c$, $t$Schnelligkeit:
In Spielen schnell laufen, fangen und ausweichen.
Die Kinder sollen Freude daran haben, schnell zu
sein, und viele verschiedene Bewegungen
kennenlernen. Ein Wettkampfgedanke ist erlaubt,
z. B. wer ist zuerst?

Über die Saison: 
Keine Saisonplanung. Das ganze Jahr
gleich, in jedem Training ein paar
Minuten, immer spielerisch und zu
Beginn des Trainings.

[Inhalt F1](https://snowsports.flink.host/s/PPsFiXFu/kY1BOb3c)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|0|it$c$, $t$Velocità:
Correre veloce, prendere e schivare nei giochi.
I bambini devono divertirsi a essere veloci e scoprire molti movimenti diversi.
Lo spirito di gara è permesso, p. es. chi arriva primo?

Nel corso della stagione:
Nessuna pianificazione stagionale.
Tutto l'anno uguale, qualche minuto in ogni allenamento, sempre in modo ludico e all'inizio dell'allenamento.

[Contenuto F1](https://snowsports.flink.host/s/PPsFiXFu/kY1BOb3c)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|0|it$c$, $t$Schnelligkeit:
In Spielen schnell laufen, fangen und ausweichen.
Die Kinder sollen Freude daran haben, schnell zu
sein, und viele verschiedene Bewegungen
kennenlernen. Ein Wettkampfgedanke ist erlaubt,
z. B. wer ist zuerst?

Über die Saison: 
Keine Saisonplanung. Das ganze Jahr
gleich, in jedem Training ein paar
Minuten, immer spielerisch und zu
Beginn des Trainings.

[Inhalt F1](https://snowsports.flink.host/s/PPsFiXFu/kY1BOb3c)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|0|en$c$, $t$Speed:
Running fast, catching and dodging in games.
Children should enjoy being fast and get to know many different movements.
A competitive element is allowed, e.g. who is first?

Over the season:
No season planning.
The same all year, a few minutes in every session, always playful and at the start of the session.

[Content F1](https://snowsports.flink.host/s/PPsFiXFu/kY1BOb3c)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|0|en$c$, $t$Schnelligkeit:
In Spielen schnell laufen, fangen und ausweichen.
Die Kinder sollen Freude daran haben, schnell zu
sein, und viele verschiedene Bewegungen
kennenlernen. Ein Wettkampfgedanke ist erlaubt,
z. B. wer ist zuerst?

Über die Saison: 
Keine Saisonplanung. Das ganze Jahr
gleich, in jedem Training ein paar
Minuten, immer spielerisch und zu
Beginn des Trainings.

[Inhalt F1](https://snowsports.flink.host/s/PPsFiXFu/kY1BOb3c)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|1|fr$c$, $t$Vitesse :
Toujours surtout dans des jeux.
S'y ajoutent les premières formes de course simples, en veillant à une posture droite et à des bras actifs.
S'arrêter vite et changer de direction s'exercent dans des jeux d'attrape et de course.

Au fil de la saison :
Pas de planification de saison.
Toute l'année de manière ludique et variée, régulièrement et brièvement aussi en hiver.

[Contenu F2](https://snowsports.flink.host/s/V9p4Capq/Lj2wygXM)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|1|fr$c$, $t$Schnelligkeit: 
Weiterhin vor allem in Spielen. Dazu kommen erste
einfache Laufformen, bei denen auf eine aufrechte
Haltung und aktive Arme geachtet wird. Schnell
anhalten und die Richtung wechseln wird in Fang-
und Laufspielen geübt.


Über die Saison: 
Keine Saisonplanung. Das ganze Jahr
spielerisch und abwechslungsreich,
auch im Winter regelmässig kurz.

[Inhalt F2](https://snowsports.flink.host/s/PPsFiXFu/kY1BOb3c)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|1|it$c$, $t$Velocità:
Sempre soprattutto nei giochi.
Si aggiungono le prime forme di corsa semplici, facendo attenzione a una postura eretta e a braccia attive.
Fermarsi velocemente e cambiare direzione si allenano nei giochi di acchiapparella e di corsa.

Nel corso della stagione:
Nessuna pianificazione stagionale.
Tutto l'anno in modo ludico e vario, regolarmente e brevemente anche in inverno.

[Contenuto F2](https://snowsports.flink.host/s/PPsFiXFu/kY1BOb3c)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|1|it$c$, $t$Schnelligkeit: 
Weiterhin vor allem in Spielen. Dazu kommen erste
einfache Laufformen, bei denen auf eine aufrechte
Haltung und aktive Arme geachtet wird. Schnell
anhalten und die Richtung wechseln wird in Fang-
und Laufspielen geübt.


Über die Saison: 
Keine Saisonplanung. Das ganze Jahr
spielerisch und abwechslungsreich,
auch im Winter regelmässig kurz.

[Inhalt F2](https://snowsports.flink.host/s/PPsFiXFu/kY1BOb3c)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|1|en$c$, $t$Speed:
Still mainly in games.
First simple running drills are added, with attention to an upright posture and active arms.
Stopping quickly and changing direction are practised in tag and running games.

Over the season:
No season planning.
Playful and varied all year, regularly and briefly in winter too.

[Content F2](https://snowsports.flink.host/s/PPsFiXFu/kY1BOb3c)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|1|en$c$, $t$Schnelligkeit: 
Weiterhin vor allem in Spielen. Dazu kommen erste
einfache Laufformen, bei denen auf eine aufrechte
Haltung und aktive Arme geachtet wird. Schnell
anhalten und die Richtung wechseln wird in Fang-
und Laufspielen geübt.


Über die Saison: 
Keine Saisonplanung. Das ganze Jahr
spielerisch und abwechslungsreich,
auch im Winter regelmässig kurz.

[Inhalt F2](https://snowsports.flink.host/s/PPsFiXFu/kY1BOb3c)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|2|fr$c$, $t$Vitesse :
Période favorable pour apprendre des mouvements rapides.
L'école de course (ABC de la course) est introduite de manière systématique, complétée par de courts sprints et de la corde à sauter pour des pieds rapides.
S'arrêter et changer de direction s'exercent dans des jeux d'attrape et de course.

Au fil de la saison :
Pas encore de planification de saison.
Toute l'année, régulièrement et brièvement, idéalement deux fois par semaine au début de l'entraînement.

[Contenu F3](https://snowsports.flink.host/s/V9p4Capq/QiDJUnPN)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|2|fr$c$, $t$Schnelligkeit: 
Günstige Zeit, um schnelle
Bewegungen zu lernen. Die Laufschule
(Lauf-ABC) wird systematisch eingeführt,
dazu kommen kurze Sprints und
Seilspringen für schnelle Füsse. Anhalten
und Richtungswechsel werden in Fang- und
Laufspielen geübt.

Über die Saison:
Noch keine
Saisonplanung. Das ganze Jahr
regelmässig und kurz, am besten zweimal
pro Woche zu Beginn des Trainings.

[Inhalt F3](https://snowsports.flink.host/s/PPsFiXFu/r8idtvTH)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|2|it$c$, $t$Velocità:
Periodo favorevole per imparare movimenti veloci.
La scuola di corsa (ABC della corsa) viene introdotta in modo sistematico, con brevi sprint e salto con la corda per piedi veloci.
Fermarsi e cambiare direzione si allenano nei giochi di acchiapparella e di corsa.

Nel corso della stagione:
Ancora nessuna pianificazione stagionale.
Tutto l'anno regolarmente e brevemente, idealmente due volte alla settimana all'inizio dell'allenamento.

[Contenuto F3](https://snowsports.flink.host/s/PPsFiXFu/r8idtvTH)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|2|it$c$, $t$Schnelligkeit: 
Günstige Zeit, um schnelle
Bewegungen zu lernen. Die Laufschule
(Lauf-ABC) wird systematisch eingeführt,
dazu kommen kurze Sprints und
Seilspringen für schnelle Füsse. Anhalten
und Richtungswechsel werden in Fang- und
Laufspielen geübt.

Über die Saison:
Noch keine
Saisonplanung. Das ganze Jahr
regelmässig und kurz, am besten zweimal
pro Woche zu Beginn des Trainings.

[Inhalt F3](https://snowsports.flink.host/s/PPsFiXFu/r8idtvTH)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|2|en$c$, $t$Speed:
A favourable time to learn fast movements.
Running school (running drills) is introduced systematically, plus short sprints and rope skipping for quick feet.
Stopping and changing direction are practised in tag and running games.

Over the season:
No season planning yet.
Regularly and briefly all year, ideally twice a week at the start of the session.

[Content F3](https://snowsports.flink.host/s/PPsFiXFu/r8idtvTH)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|2|en$c$, $t$Schnelligkeit: 
Günstige Zeit, um schnelle
Bewegungen zu lernen. Die Laufschule
(Lauf-ABC) wird systematisch eingeführt,
dazu kommen kurze Sprints und
Seilspringen für schnelle Füsse. Anhalten
und Richtungswechsel werden in Fang- und
Laufspielen geübt.

Über die Saison:
Noch keine
Saisonplanung. Das ganze Jahr
regelmässig und kurz, am besten zweimal
pro Woche zu Beginn des Trainings.

[Inhalt F3](https://snowsports.flink.host/s/PPsFiXFu/r8idtvTH)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|3|fr$c$, $t$Vitesse :
Début de l'entraînement athlétique de la vitesse.
Les athlètes apprennent à accélérer, freiner et changer de direction de manière consciente.
Lors du freinage, un axe des jambes stable est central ; c'est la même qualité que pour une bonne réception.
La technique passe avant la vitesse, mais chaque course se fait avec un engagement total.

Au fil de la saison :
VP1 et VP2 : technique de course, départs et freinage.
VWP : sprints courts à pleine vitesse.
WP : maintenir en hiver avec des séances courtes.
Environ deux tiers de l'entraînement restent un entraînement de base.

*Remarque : tenir compte de la poussée de croissance. Les filles entrent généralement plus tôt dans la puberté que les garçons

[Contenu T1-2](https://snowsports.flink.host/s/V9p4Capq/LpgcUjVp)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|3|fr$c$, $t$Schnelligkeit: 
Start des athletischen
Schnelligkeitstrainings. Die Athlet:innen
lernen bewusst zu beschleunigen,
abzubremsen und die Richtung zu
wechseln. Beim Abbremsen steht eine
stabile Beinachse im Zentrum, das ist die
gleiche Qualität wie bei einer guten Landung. Technik geht vor Tempo, aber
jeder Lauf erfolgt mit vollem Einsatz.

Über die Saison: 
VP1 und VP2: Lauftechnik, Starts und Abbremsen. 
VWP: kurze Sprints mit vollem Tempo.
WP: im Winter mit kurzen Einheiten
erhalten. Rund zwei Drittel des Trainings
bleiben Grundlagentraining.

*Hinweis: Wachstumsschub beachten. Mädchen kommen meist früher in die Pubertät als Knaben

[Inhalt T1-2](https://snowsports.flink.host/s/PPsFiXFu/UBlddCun)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|3|it$c$, $t$Velocità:
Inizio dell'allenamento atletico della velocità.
Gli/le atleti/e imparano ad accelerare, frenare e cambiare direzione in modo consapevole.
Nella frenata è centrale un asse delle gambe stabile: è la stessa qualità di un buon atterraggio.
La tecnica viene prima della velocità, ma ogni corsa si fa con il massimo impegno.

Nel corso della stagione:
VP1 e VP2: tecnica di corsa, partenze e frenata.
VWP: sprint brevi alla massima velocità.
WP: mantenere in inverno con sedute brevi.
Circa due terzi dell'allenamento restano allenamento di base.

*Nota: tenere conto della fase di crescita. Le ragazze entrano di solito prima nella pubertà rispetto ai ragazzi

[Contenuto T1-2](https://snowsports.flink.host/s/PPsFiXFu/UBlddCun)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|3|it$c$, $t$Schnelligkeit: 
Start des athletischen
Schnelligkeitstrainings. Die Athlet:innen
lernen bewusst zu beschleunigen,
abzubremsen und die Richtung zu
wechseln. Beim Abbremsen steht eine
stabile Beinachse im Zentrum, das ist die
gleiche Qualität wie bei einer guten Landung. Technik geht vor Tempo, aber
jeder Lauf erfolgt mit vollem Einsatz.

Über die Saison: 
VP1 und VP2: Lauftechnik, Starts und Abbremsen. 
VWP: kurze Sprints mit vollem Tempo.
WP: im Winter mit kurzen Einheiten
erhalten. Rund zwei Drittel des Trainings
bleiben Grundlagentraining.

*Hinweis: Wachstumsschub beachten. Mädchen kommen meist früher in die Pubertät als Knaben

[Inhalt T1-2](https://snowsports.flink.host/s/PPsFiXFu/UBlddCun)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|3|en$c$, $t$Speed:
Start of athletic speed training.
Athletes learn to accelerate, brake and change direction deliberately.
When braking, a stable leg axis is central; it is the same quality as in a good landing.
Technique comes before speed, but every run is done at full effort.

Over the season:
VP1 and VP2: running technique, starts and braking.
VWP: short sprints at full speed.
WP: maintain in winter with short sessions.
Around two thirds of training remains basic training.

*Note: take the growth spurt into account. Girls usually reach puberty earlier than boys

[Content T1-2](https://snowsports.flink.host/s/PPsFiXFu/UBlddCun)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|3|en$c$, $t$Schnelligkeit: 
Start des athletischen
Schnelligkeitstrainings. Die Athlet:innen
lernen bewusst zu beschleunigen,
abzubremsen und die Richtung zu
wechseln. Beim Abbremsen steht eine
stabile Beinachse im Zentrum, das ist die
gleiche Qualität wie bei einer guten Landung. Technik geht vor Tempo, aber
jeder Lauf erfolgt mit vollem Einsatz.

Über die Saison: 
VP1 und VP2: Lauftechnik, Starts und Abbremsen. 
VWP: kurze Sprints mit vollem Tempo.
WP: im Winter mit kurzen Einheiten
erhalten. Rund zwei Drittel des Trainings
bleiben Grundlagentraining.

*Hinweis: Wachstumsschub beachten. Mädchen kommen meist früher in die Pubertät als Knaben

[Inhalt T1-2](https://snowsports.flink.host/s/PPsFiXFu/UBlddCun)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|4|fr$c$, $t$Vitesse :
La vitesse augmente, les pieds deviennent plus rapides.
Les changements de direction s'exercent des deux côtés pour qu'aucun côté ne reste plus faible.
La technique continue d'être affinée pour qu'elle tienne aussi à grande vitesse.
Des pieds rapides et relâchés avec un haut du corps calme sont un objectif.

Au fil de la saison :
Planification simplifiée.
VP1 et VP2 : technique, école de course et changements de direction.
VWP : plus vite.
WP : maintenir le niveau avec des séances courtes.

*Remarque : tenir compte de la poussée de croissance. Les filles entrent généralement plus tôt dans la puberté que les garçons. Adapter les charges en cas de douleurs ou de problèmes de coordination.

[Contenu T1-2](https://snowsports.flink.host/s/V9p4Capq/LpgcUjVp)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|4|fr$c$, $t$Schnelligkeit: 
Das Tempo wird höher, die
Füsse schneller. Richtungswechsel werden
nach beiden Seiten geübt, damit keine Seite
schwächer bleibt. Die Technik wird weiter
verfeinert, damit sie auch bei hohem Tempo
hält. Schnelle, lockere Füsse bei ruhigem
Oberkörper sind ein Ziel.

Über die Saison: 
Vereinfachte Planung.
VP1 und VP2: Technik, Laufschule und
Richtungswechsel. 
VWP: schneller. 
WP: Niveau mit kurzen Einheiten halten.

*Hinweis: Wachstumsschub beachten. Mädchen kommen meist früher in die Pubertät als Knaben. Belastungen anpassen, wenn Schmerzen oder Koordinationsprobleme auftreten.

[Inhalt T1-2](https://snowsports.flink.host/s/PPsFiXFu/UBlddCun)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|4|it$c$, $t$Velocità:
Il ritmo aumenta, i piedi diventano più veloci.
I cambi di direzione si allenano da entrambi i lati, affinché nessun lato resti più debole.
La tecnica viene ulteriormente affinata perché tenga anche ad alta velocità.
Piedi veloci e sciolti con il busto stabile sono un obiettivo.

Nel corso della stagione:
Pianificazione semplificata.
VP1 e VP2: tecnica, scuola di corsa e cambi di direzione.
VWP: più veloce.
WP: mantenere il livello con sedute brevi.

*Nota: tenere conto della fase di crescita. Le ragazze entrano di solito prima nella pubertà rispetto ai ragazzi. Adattare i carichi in caso di dolori o problemi di coordinazione.

[Contenuto T1-2](https://snowsports.flink.host/s/PPsFiXFu/UBlddCun)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|4|it$c$, $t$Schnelligkeit: 
Das Tempo wird höher, die
Füsse schneller. Richtungswechsel werden
nach beiden Seiten geübt, damit keine Seite
schwächer bleibt. Die Technik wird weiter
verfeinert, damit sie auch bei hohem Tempo
hält. Schnelle, lockere Füsse bei ruhigem
Oberkörper sind ein Ziel.

Über die Saison: 
Vereinfachte Planung.
VP1 und VP2: Technik, Laufschule und
Richtungswechsel. 
VWP: schneller. 
WP: Niveau mit kurzen Einheiten halten.

*Hinweis: Wachstumsschub beachten. Mädchen kommen meist früher in die Pubertät als Knaben. Belastungen anpassen, wenn Schmerzen oder Koordinationsprobleme auftreten.

[Inhalt T1-2](https://snowsports.flink.host/s/PPsFiXFu/UBlddCun)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|4|en$c$, $t$Speed:
The pace gets higher, the feet faster.
Changes of direction are practised to both sides so that no side stays weaker.
Technique is refined further so that it holds at high speed.
Quick, relaxed feet with a calm upper body are a goal.

Over the season:
Simplified planning.
VP1 and VP2: technique, running school and changes of direction.
VWP: faster.
WP: maintain the level with short sessions.

*Note: take the growth spurt into account. Girls usually reach puberty earlier than boys. Adjust loads if pain or coordination problems occur.

[Content T1-2](https://snowsports.flink.host/s/PPsFiXFu/UBlddCun)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|4|en$c$, $t$Schnelligkeit: 
Das Tempo wird höher, die
Füsse schneller. Richtungswechsel werden
nach beiden Seiten geübt, damit keine Seite
schwächer bleibt. Die Technik wird weiter
verfeinert, damit sie auch bei hohem Tempo
hält. Schnelle, lockere Füsse bei ruhigem
Oberkörper sind ein Ziel.

Über die Saison: 
Vereinfachte Planung.
VP1 und VP2: Technik, Laufschule und
Richtungswechsel. 
VWP: schneller. 
WP: Niveau mit kurzen Einheiten halten.

*Hinweis: Wachstumsschub beachten. Mädchen kommen meist früher in die Pubertät als Knaben. Belastungen anpassen, wenn Schmerzen oder Koordinationsprobleme auftreten.

[Inhalt T1-2](https://snowsports.flink.host/s/PPsFiXFu/UBlddCun)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|5|fr$c$, $t$Vitesse :
Transition vers l'entraînement de performance.
Le départ (les premiers mètres) et la vitesse maximale sont développés séparément, car ce sont des capacités différentes.
Les changements de direction se font en pleine course, le freinage devient plus puissant.
En park & pipe, la vitesse sert de base athlétique pour le pop, l'impulsion et la réception.

Au fil de la saison :
Les quatre phases sont planifiées de manière consciente.
VP1 : technique et longueur de foulée.
VP2 : contact au sol plus court, changements de direction à plus grande vitesse.
VWP : vitesse maximale, Skills-Check.
WP : maintenir le niveau avec des séances courtes et fraîches.

[Contenu T3-4](https://snowsports.flink.host/s/V9p4Capq/3LYg8MFv)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|5|fr$c$, $t$Schnelligkeit: 
Übergang zum Leistungstraining. Antritt (die ersten
Meter) und Höchsttempo werden getrennt
entwickelt, weil sie unterschiedliche Fähigkeiten
sind. Richtungswechsel erfolgen aus vollem Lauf,
das Abbremsen wird kräftiger. Schnelligkeit dient im
Park & Pipe als athletische Basis für Pop,
Absprung und Landung.

Über die Saison: 
Alle vier Phasen werden bewusst
geplant.
VP1: Technik und Schrittlänge.
VP2: kürzerer Bodenkontakt,
Richtungswechsel aus höherem Tempo.
VWP: maximal schnell, Skills Check.
WP: mit kurzen, frischen Einheiten das
Niveau halten.

[Inhalt T3-4](https://snowsports.flink.host/s/PPsFiXFu/0gahlWER)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|5|it$c$, $t$Velocità:
Passaggio all'allenamento di prestazione.
La partenza (i primi metri) e la velocità massima vengono sviluppate separatamente, perché sono capacità diverse.
I cambi di direzione avvengono in piena corsa, la frenata diventa più potente.
Nel park & pipe la velocità serve da base atletica per pop, stacco e atterraggio.

Nel corso della stagione:
Tutte e quattro le fasi vengono pianificate in modo consapevole.
VP1: tecnica e lunghezza del passo.
VP2: contatto al suolo più breve, cambi di direzione a velocità più elevata.
VWP: velocità massima, Skills-Check.
WP: mantenere il livello con sedute brevi e fresche.

[Contenuto T3-4](https://snowsports.flink.host/s/PPsFiXFu/0gahlWER)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|5|it$c$, $t$Schnelligkeit: 
Übergang zum Leistungstraining. Antritt (die ersten
Meter) und Höchsttempo werden getrennt
entwickelt, weil sie unterschiedliche Fähigkeiten
sind. Richtungswechsel erfolgen aus vollem Lauf,
das Abbremsen wird kräftiger. Schnelligkeit dient im
Park & Pipe als athletische Basis für Pop,
Absprung und Landung.

Über die Saison: 
Alle vier Phasen werden bewusst
geplant.
VP1: Technik und Schrittlänge.
VP2: kürzerer Bodenkontakt,
Richtungswechsel aus höherem Tempo.
VWP: maximal schnell, Skills Check.
WP: mit kurzen, frischen Einheiten das
Niveau halten.

[Inhalt T3-4](https://snowsports.flink.host/s/PPsFiXFu/0gahlWER)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|5|en$c$, $t$Speed:
Transition to performance training.
Acceleration (the first metres) and top speed are developed separately because they are different abilities.
Changes of direction are made at full speed, braking becomes more powerful.
In park & pipe, speed serves as the athletic basis for pop, take-off and landing.

Over the season:
All four phases are planned deliberately.
VP1: technique and stride length.
VP2: shorter ground contact, changes of direction at higher speed.
VWP: maximum speed, Skills-Check.
WP: maintain the level with short, fresh sessions.

[Content T3-4](https://snowsports.flink.host/s/PPsFiXFu/0gahlWER)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|5|en$c$, $t$Schnelligkeit: 
Übergang zum Leistungstraining. Antritt (die ersten
Meter) und Höchsttempo werden getrennt
entwickelt, weil sie unterschiedliche Fähigkeiten
sind. Richtungswechsel erfolgen aus vollem Lauf,
das Abbremsen wird kräftiger. Schnelligkeit dient im
Park & Pipe als athletische Basis für Pop,
Absprung und Landung.

Über die Saison: 
Alle vier Phasen werden bewusst
geplant.
VP1: Technik und Schrittlänge.
VP2: kürzerer Bodenkontakt,
Richtungswechsel aus höherem Tempo.
VWP: maximal schnell, Skills Check.
WP: mit kurzen, frischen Einheiten das
Niveau halten.

[Inhalt T3-4](https://snowsports.flink.host/s/PPsFiXFu/0gahlWER)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|6|fr$c$, $t$Vitesse :
Vitesses les plus élevées, aussi de manière ciblée au-delà de la vitesse habituelle.
Plusieurs sprints d'affilée sont courus avec la même qualité, comme en contest où plusieurs runs doivent être aussi bons.
Les athlètes connaissent leurs forces et faiblesses grâce aux tests.

Au fil de la saison :
Planification comme en T3, mais plus ciblée : les priorités en VP1 et VP2 dépendent des résultats des tests (Skills-Checks, tests CNP).
En VWP, la vitesse maximale est poussée au maximum, en WP elle est maintenue.

[Contenu T3-4](https://snowsports.flink.host/s/V9p4Capq/3LYg8MFv)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|6|fr$c$, $t$Schnelligkeit:
Höchste Tempi, gezielt auch über das gewohnte
Tempo hinaus. Mehrere Sprints hintereinander
werden in gleicher Qualität gelaufen, so wie im
Contest mehrere Runs gleich gut sein müssen. Die
Athlet:innen kennen ihre Stärken und Schwächen
aus den Tests.

Über die Saison:
Planung wie in T3, aber gezielter: Die
Schwerpunkte in VP1 und VP2 richten
sich nach den Testresultaten (Skills
Checks, NLZ-Tests). In der VWP wird
das Höchsttempo ausgereizt, in der WP
gehalten.

[Inhalt T3-4](https://snowsports.flink.host/s/PPsFiXFu/0gahlWER)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|6|it$c$, $t$Velocità:
Velocità massime, anche in modo mirato oltre la velocità abituale.
Diversi sprint di fila vengono corsi con la stessa qualità, così come in un contest più run devono essere ugualmente buone.
Gli/le atleti/e conoscono i propri punti forti e deboli grazie ai test.

Nel corso della stagione:
Pianificazione come in T3, ma più mirata: le priorità in VP1 e VP2 dipendono dai risultati dei test (Skills-Check, test CNP).
Nella VWP la velocità massima viene sfruttata al massimo, nella WP mantenuta.

[Contenuto T3-4](https://snowsports.flink.host/s/PPsFiXFu/0gahlWER)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|6|it$c$, $t$Schnelligkeit:
Höchste Tempi, gezielt auch über das gewohnte
Tempo hinaus. Mehrere Sprints hintereinander
werden in gleicher Qualität gelaufen, so wie im
Contest mehrere Runs gleich gut sein müssen. Die
Athlet:innen kennen ihre Stärken und Schwächen
aus den Tests.

Über die Saison:
Planung wie in T3, aber gezielter: Die
Schwerpunkte in VP1 und VP2 richten
sich nach den Testresultaten (Skills
Checks, NLZ-Tests). In der VWP wird
das Höchsttempo ausgereizt, in der WP
gehalten.

[Inhalt T3-4](https://snowsports.flink.host/s/PPsFiXFu/0gahlWER)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|6|en$c$, $t$Speed:
Highest speeds, deliberately also beyond the usual pace.
Several sprints in a row are run at the same quality, just as several runs must be equally good in a contest.
Athletes know their strengths and weaknesses from the tests.

Over the season:
Planning as in T3 but more targeted: the priorities in VP1 and VP2 depend on the test results (Skills-Checks, NTC tests).
In the VWP top speed is pushed to the limit, in the WP it is maintained.

[Content T3-4](https://snowsports.flink.host/s/PPsFiXFu/0gahlWER)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|6|en$c$, $t$Schnelligkeit:
Höchste Tempi, gezielt auch über das gewohnte
Tempo hinaus. Mehrere Sprints hintereinander
werden in gleicher Qualität gelaufen, so wie im
Contest mehrere Runs gleich gut sein müssen. Die
Athlet:innen kennen ihre Stärken und Schwächen
aus den Tests.

Über die Saison:
Planung wie in T3, aber gezielter: Die
Schwerpunkte in VP1 und VP2 richten
sich nach den Testresultaten (Skills
Checks, NLZ-Tests). In der VWP wird
das Höchsttempo ausgereizt, in der WP
gehalten.

[Inhalt T3-4](https://snowsports.flink.host/s/PPsFiXFu/0gahlWER)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|7|fr$c$, $t$Vitesse :
L'entraînement est individualisé et piloté par des tests : où se trouve la réserve, au départ, à la vitesse maximale ou au freinage ?
L'entraînement reste athlétique, le transfert au park et au pipe se fait dans l'entraînement de discipline.

Au fil de la saison :
Planification comme en T4.
Les phases sont orientées vers les temps forts de la saison ; avant les compétitions importantes, un pic est visé de manière ciblée, en hiver le niveau est maintenu.

[Contenu E](https://snowsports.flink.host/s/V9p4Capq/opgY4edq)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|7|fr$c$, $t$Schnelligkeit:
Das Training wird individuell und über Tests
gesteuert: Wo liegt die Reserve, beim Antritt, beim
Höchsttempo oder beim Abbremsen? Das Training
bleibt athletisch, die Übertragung auf Park und Pipe
geschieht im Disziplintraining.

Über die Saison: 
Planung wie in T4. Die Phasen werden
auf die Saisonhöhepunkte ausgerichtet;
vor wichtigen Wettkämpfen wird gezielt
eine Spitze gesetzt, im Winter das
Niveau gehalten.

[Inhalt E](https://snowsports.flink.host/s/PPsFiXFu/MjgEN4Nh)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|7|it$c$, $t$Velocità:
L'allenamento è individuale e guidato dai test: dove si trova la riserva, nella partenza, nella velocità massima o nella frenata?
L'allenamento resta atletico, il trasferimento a park e pipe avviene nell'allenamento della disciplina.

Nel corso della stagione:
Pianificazione come in T4.
Le fasi sono orientate ai momenti clou della stagione; prima delle gare importanti si punta a un picco in modo mirato, in inverno si mantiene il livello.

[Contenuto E](https://snowsports.flink.host/s/PPsFiXFu/MjgEN4Nh)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|7|it$c$, $t$Schnelligkeit:
Das Training wird individuell und über Tests
gesteuert: Wo liegt die Reserve, beim Antritt, beim
Höchsttempo oder beim Abbremsen? Das Training
bleibt athletisch, die Übertragung auf Park und Pipe
geschieht im Disziplintraining.

Über die Saison: 
Planung wie in T4. Die Phasen werden
auf die Saisonhöhepunkte ausgerichtet;
vor wichtigen Wettkämpfen wird gezielt
eine Spitze gesetzt, im Winter das
Niveau gehalten.

[Inhalt E](https://snowsports.flink.host/s/PPsFiXFu/MjgEN4Nh)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|7|en$c$, $t$Speed:
Training is individual and steered by tests: where is the reserve, in acceleration, top speed or braking?
Training remains athletic; the transfer to park and pipe happens in discipline training.

Over the season:
Planning as in T4.
The phases are aligned with the season highlights; before important competitions a peak is set deliberately, in winter the level is maintained.

[Content E](https://snowsports.flink.host/s/PPsFiXFu/MjgEN4Nh)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|7|en$c$, $t$Schnelligkeit:
Das Training wird individuell und über Tests
gesteuert: Wo liegt die Reserve, beim Antritt, beim
Höchsttempo oder beim Abbremsen? Das Training
bleibt athletisch, die Übertragung auf Park und Pipe
geschieht im Disziplintraining.

Über die Saison: 
Planung wie in T4. Die Phasen werden
auf die Saisonhöhepunkte ausgerichtet;
vor wichtigen Wettkämpfen wird gezielt
eine Spitze gesetzt, im Winter das
Niveau gehalten.

[Inhalt E](https://snowsports.flink.host/s/PPsFiXFu/MjgEN4Nh)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|8|fr$c$, $t$Vitesse :
Comme Elite.
La vitesse est entraînée régulièrement, aussi en phase de compétition, afin de maintenir le niveau.

Au fil de la saison :
Planification comme Elite.
Prévoir suffisamment de récupération entre les séances intensives.

[Contenu M](https://snowsports.flink.host/s/V9p4Capq/opgY4edq)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|8|fr$c$, $t$Schnelligkeit:
Wie Elite. Schnelligkeit wird regelmässig trainiert,
auch in der Wettkampfphase, damit das Niveau
erhalten bleibt.

Über die Saison:
Planung wie Elite. Genügend Erholung
zwischen intensiven Einheiten
einplanen.

[Inhalt M](https://snowsports.flink.host/s/PPsFiXFu/MjgEN4Nh)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|8|it$c$, $t$Velocità:
Come Elite.
La velocità viene allenata regolarmente, anche nella fase di gara, per mantenere il livello.

Nel corso della stagione:
Pianificazione come Elite.
Prevedere sufficiente recupero tra le sedute intensive.

[Contenuto M](https://snowsports.flink.host/s/PPsFiXFu/MjgEN4Nh)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|8|it$c$, $t$Schnelligkeit:
Wie Elite. Schnelligkeit wird regelmässig trainiert,
auch in der Wettkampfphase, damit das Niveau
erhalten bleibt.

Über die Saison:
Planung wie Elite. Genügend Erholung
zwischen intensiven Einheiten
einplanen.

[Inhalt M](https://snowsports.flink.host/s/PPsFiXFu/MjgEN4Nh)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$shared|schnelligkeit-pp|1|8|en$c$, $t$Speed:
As Elite.
Speed is trained regularly, also during the competition phase, so that the level is maintained.

Over the season:
Planning as Elite.
Plan enough recovery between intensive sessions.

[Content M](https://snowsports.flink.host/s/PPsFiXFu/MjgEN4Nh)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|shared|schnelligkeit-pp|1|8|en$c$, $t$Schnelligkeit:
Wie Elite. Schnelligkeit wird regelmässig trainiert,
auch in der Wettkampfphase, damit das Niveau
erhalten bleibt.

Über die Saison:
Planung wie Elite. Genügend Erholung
zwischen intensiven Einheiten
einplanen.

[Inhalt M](https://snowsports.flink.host/s/PPsFiXFu/MjgEN4Nh)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|0|F1|fr$c$, $t$MENTAL
• Se concentrer : vivre les quatre formes d'attention de manière ludique, une chose par descente ; dès F3 lire le park, annoncer le run, drop-in call

ON-SNOW
• Skier de manière ludique et sûre sur tous les terrains, rouler en switch, premiers sauts
• Focus externe (kicker, box, réception) plutôt que des consignes corporelles précises
• Dès F3 : set-up turns, tricks sur piste, petits kickers, box et rails simples, première expérience en halfpipe

OFF-SNOW SPÉCIFIQUE AU SPORT
• Trampoline, skate et inline : de manière ludique ; dès F3 premières sessions bag et dry slope, réceptions contrôlées
• Skills-Checks acrobatie et inline : niveau Starter

ATHLÉTISME
• Endurance : entretenir un quotidien actif, développer la tolérance à la charge de manière ample, variée et stimulante, polysportif
• Mobilité/souplesse : mouvements ludiques avec une amplitude maximale ; dès F3 exercices dynamiques et statiques dans l'échauffement
• Force : formes ludiques des mouvements de base (pousser, appuyer, freiner, tirer) ; dès F3 entraînement technique, exercices avec le poids du corps, formes de sauts variées
• Vitesse/agilité : courir vite, attraper et esquiver dans des jeux ; dès F3 école de course (ABC de la course), sprints courts, corde à sauter$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|0|F1|fr$c$, $t$MENTAL
• Sich konzentrieren: die vier Aufmerksamkeitsformen spielerisch erleben, eine Sache pro Fahrt; ab F3 Park lesen, Run ansagen, Drop-in-Call

ON-SNOW
• Spielerisch sicher fahren in jedem Gelände, switch fahren, erste Sprünge
• Fokus auf Äusseres (Kicker, Box, Landung) statt genaue Körperanweisungen
• Ab F3: Set-Up-Turns, Pistentricks, kleine Kicker, Boxen und einfache Rails, erste Halfpipe-Erfahrung

OFF-SNOW SPORTARTSPEZIFISCH
• Trampolin, Skate und Inline: spielerisch; ab F3 erste Bag-Sessions und Dry Slope, kontrollierte Landungen
• Skills-Checks Akrobatik und Inline: Stufe Starter

ATHLETIK
• Ausdauer: aktiven Alltag pflegen, Belastungsverträglichkeit umfangreich, vielseitig und herausfordernd aufbauen, polysportiv
• Mobilität/Beweglichkeit: spielerische Bewegungen mit maximalem Bewegungsumfang; ab F3 dynamische und statische Übungen im Warm-Up
• Kraft: spielerische Formen der Basisbewegungen (Stossen, Stützen, Bremsen, Ziehen); ab F3 Techniktraining, Übungen mit dem eigenen Körpergewicht, variantenreiche Sprungformen
• Schnelligkeit/Agilität: in Spielen schnell laufen, fangen und ausweichen; ab F3 Laufschule (Lauf-ABC), kurze Sprints, Seilspringen$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|0|F1|it$c$, $t$MENTALE
• Concentrarsi: vivere le quattro forme di attenzione in modo ludico, una cosa per discesa; da F3 leggere il park, annunciare la run, drop-in call

ON-SNOW
• Sciare in modo ludico e sicuro su ogni terreno, sciare in switch, primi salti
• Focus esterno (kicker, box, atterraggio) invece di istruzioni corporee precise
• Da F3: set-up turns, trick in pista, piccoli kicker, box e rail semplici, prima esperienza in halfpipe

OFF-SNOW SPECIFICO DELLO SPORT
• Trampolino, skate e inline: in modo ludico; da F3 prime sessioni bag e dry slope, atterraggi controllati
• Skills-Check acrobatica e inline: livello Starter

ATLETICA
• Resistenza: mantenere una quotidianità attiva, sviluppare la tolleranza al carico in modo ampio, variato e stimolante, polisportivo
• Mobilità/flessibilità: movimenti ludici con la massima ampiezza; da F3 esercizi dinamici e statici nel riscaldamento
• Forza: forme ludiche dei movimenti di base (spingere, sostenersi, frenare, tirare); da F3 allenamento tecnico, esercizi con il proprio peso corporeo, forme di salto variate
• Velocità/agilità: correre veloce, prendere e schivare nei giochi; da F3 scuola di corsa (ABC della corsa), sprint brevi, salto con la corda$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|0|F1|it$c$, $t$MENTAL
• Sich konzentrieren: die vier Aufmerksamkeitsformen spielerisch erleben, eine Sache pro Fahrt; ab F3 Park lesen, Run ansagen, Drop-in-Call

ON-SNOW
• Spielerisch sicher fahren in jedem Gelände, switch fahren, erste Sprünge
• Fokus auf Äusseres (Kicker, Box, Landung) statt genaue Körperanweisungen
• Ab F3: Set-Up-Turns, Pistentricks, kleine Kicker, Boxen und einfache Rails, erste Halfpipe-Erfahrung

OFF-SNOW SPORTARTSPEZIFISCH
• Trampolin, Skate und Inline: spielerisch; ab F3 erste Bag-Sessions und Dry Slope, kontrollierte Landungen
• Skills-Checks Akrobatik und Inline: Stufe Starter

ATHLETIK
• Ausdauer: aktiven Alltag pflegen, Belastungsverträglichkeit umfangreich, vielseitig und herausfordernd aufbauen, polysportiv
• Mobilität/Beweglichkeit: spielerische Bewegungen mit maximalem Bewegungsumfang; ab F3 dynamische und statische Übungen im Warm-Up
• Kraft: spielerische Formen der Basisbewegungen (Stossen, Stützen, Bremsen, Ziehen); ab F3 Techniktraining, Übungen mit dem eigenen Körpergewicht, variantenreiche Sprungformen
• Schnelligkeit/Agilität: in Spielen schnell laufen, fangen und ausweichen; ab F3 Laufschule (Lauf-ABC), kurze Sprints, Seilspringen$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|0|F1|en$c$, $t$MENTAL
• Concentrating: experience the four forms of attention playfully, one thing per run; from F3 reading the park, calling the run, drop-in call

ON-SNOW
• Riding safely and playfully on any terrain, riding switch, first jumps
• External focus (kicker, box, landing) instead of detailed body instructions
• From F3: set-up turns, piste tricks, small kickers, boxes and simple rails, first halfpipe experience

OFF-SNOW SPORT-SPECIFIC
• Trampoline, skate and inline: playfully; from F3 first bag sessions and dry slope, controlled landings
• Skills-Checks acrobatics and inline: Starter level

ATHLETICS
• Endurance: keep an active everyday life, build load tolerance in an extensive, varied and challenging way, multi-sport
• Mobility/flexibility: playful movements through the full range of motion; from F3 dynamic and static exercises in the warm-up
• Strength: playful forms of the basic movements (pushing, supporting, braking, pulling); from F3 technique training, body-weight exercises, varied jumping forms
• Speed/agility: running fast, catching and dodging in games; from F3 running school (running drills), short sprints, rope skipping$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|0|F1|en$c$, $t$MENTAL
• Sich konzentrieren: die vier Aufmerksamkeitsformen spielerisch erleben, eine Sache pro Fahrt; ab F3 Park lesen, Run ansagen, Drop-in-Call

ON-SNOW
• Spielerisch sicher fahren in jedem Gelände, switch fahren, erste Sprünge
• Fokus auf Äusseres (Kicker, Box, Landung) statt genaue Körperanweisungen
• Ab F3: Set-Up-Turns, Pistentricks, kleine Kicker, Boxen und einfache Rails, erste Halfpipe-Erfahrung

OFF-SNOW SPORTARTSPEZIFISCH
• Trampolin, Skate und Inline: spielerisch; ab F3 erste Bag-Sessions und Dry Slope, kontrollierte Landungen
• Skills-Checks Akrobatik und Inline: Stufe Starter

ATHLETIK
• Ausdauer: aktiven Alltag pflegen, Belastungsverträglichkeit umfangreich, vielseitig und herausfordernd aufbauen, polysportiv
• Mobilität/Beweglichkeit: spielerische Bewegungen mit maximalem Bewegungsumfang; ab F3 dynamische und statische Übungen im Warm-Up
• Kraft: spielerische Formen der Basisbewegungen (Stossen, Stützen, Bremsen, Ziehen); ab F3 Techniktraining, Übungen mit dem eigenen Körpergewicht, variantenreiche Sprungformen
• Schnelligkeit/Agilität: in Spielen schnell laufen, fangen und ausweichen; ab F3 Laufschule (Lauf-ABC), kurze Sprints, Seilspringen$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|1|F1|fr$c$, $t$Combien s'entraîner ?
Par an : 150–500h de temps d'entraînement

Hiver (octobre–avril)
On-snow : 30–45 jours de neige, Ø 1,5–2 jours par semaine
Off-snow : athlétisme 2h/semaine, entraînement mental 0,5h/semaine
Été (mai–septembre)
On-snow : –
Off-snow : bag 1–10 sessions ; dry slope 2h, trampoline 2h, athlétisme 4h par semaine$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|1|F1|fr$c$, $t$Wie viel trainieren?
Kopieren
Pro Jahr: 150–500h Trainingszeit

Winter (Oktober–April)
On-Snow: 30–45 Schneetage, Ø 1,5–2 Tage pro Woche
Off-Snow: Athletik 2h/Woche, Mentaltraining 0,5h/Woche
Sommer (Mai–September)
On-Snow: –
Off-Snow: Bag 1–10 Sessions; Dry Slope 2h, Trampolin 2h, Athletik 4h pro Woche$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|1|F1|it$c$, $t$Quanto allenarsi?
All'anno: 150–500h di tempo di allenamento

Inverno (ottobre–aprile)
On-snow: 30–45 giorni sulla neve, Ø 1,5–2 giorni a settimana
Off-snow: atletica 2h/settimana, allenamento mentale 0,5h/settimana
Estate (maggio–settembre)
On-snow: –
Off-snow: bag 1–10 sessioni; dry slope 2h, trampolino 2h, atletica 4h a settimana$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|1|F1|it$c$, $t$Wie viel trainieren?
Kopieren
Pro Jahr: 150–500h Trainingszeit

Winter (Oktober–April)
On-Snow: 30–45 Schneetage, Ø 1,5–2 Tage pro Woche
Off-Snow: Athletik 2h/Woche, Mentaltraining 0,5h/Woche
Sommer (Mai–September)
On-Snow: –
Off-Snow: Bag 1–10 Sessions; Dry Slope 2h, Trampolin 2h, Athletik 4h pro Woche$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|1|F1|en$c$, $t$How much training?
Per year: 150–500h training time

Winter (October–April)
On-snow: 30–45 snow days, Ø 1.5–2 days per week
Off-snow: athletics 2h/week, mental training 0.5h/week
Summer (May–September)
On-snow: –
Off-snow: bag 1–10 sessions; dry slope 2h, trampoline 2h, athletics 4h per week$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|1|F1|en$c$, $t$Wie viel trainieren?
Kopieren
Pro Jahr: 150–500h Trainingszeit

Winter (Oktober–April)
On-Snow: 30–45 Schneetage, Ø 1,5–2 Tage pro Woche
Off-Snow: Athletik 2h/Woche, Mentaltraining 0,5h/Woche
Sommer (Mai–September)
On-Snow: –
Off-Snow: Bag 1–10 Sessions; Dry Slope 2h, Trampolin 2h, Athletik 4h pro Woche$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|2|F1|fr$c$, $t$Structure & environnement
Famille
École obligatoire

Cadre
F1–F2 : ski-club, club sportif ; F3 : CRP, ski-club, club sportif

Swiss Olympic Card
aucune

Compétitions
F1–F2 : aucune ; F3 : 2 à 4

Type de compétition
F1 : aucune ; F2–F3 : compétitions dans l'interrégion (Est, Centre, Ouest)

Directives de sélection
–$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|2|F1|fr$c$, $t$Struktur & Umfeld
Kopieren
Familie
Obligatorische Schule

Kader
F1–F2: Skiclub, Sportclub; F3: RLZ, Skiclub, Sportclub

Swiss Olympic Card
keine

Wettkämpfe
F1–F2: keine; F3: 2 bis 4

Wettkampfart
F1: keine; F2–F3: Wettbewerbe in der Interregion (Ost, Mitte, West)

Selektionsrichtlinien
–$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|2|F1|it$c$, $t$Struttura & contesto
Famiglia
Scuola dell'obbligo

Quadri
F1–F2: sci club, club sportivo; F3: CRP, sci club, club sportivo

Swiss Olympic Card
nessuna

Gare
F1–F2: nessuna; F3: da 2 a 4

Tipo di gara
F1: nessuna; F2–F3: competizioni nell'interregione (Est, Centro, Ovest)

Direttive di selezione
–$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|2|F1|it$c$, $t$Struktur & Umfeld
Kopieren
Familie
Obligatorische Schule

Kader
F1–F2: Skiclub, Sportclub; F3: RLZ, Skiclub, Sportclub

Swiss Olympic Card
keine

Wettkämpfe
F1–F2: keine; F3: 2 bis 4

Wettkampfart
F1: keine; F2–F3: Wettbewerbe in der Interregion (Ost, Mitte, West)

Selektionsrichtlinien
–$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|2|F1|en$c$, $t$Structure & environment
Family
Compulsory school

Squad
F1–F2: ski club, sports club; F3: RTC, ski club, sports club

Swiss Olympic Card
none

Competitions
F1–F2: none; F3: 2 to 4

Competition type
F1: none; F2–F3: competitions in the interregion (East, Centre, West)

Selection guidelines
–$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|2|F1|en$c$, $t$Struktur & Umfeld
Kopieren
Familie
Obligatorische Schule

Kader
F1–F2: Skiclub, Sportclub; F3: RLZ, Skiclub, Sportclub

Swiss Olympic Card
keine

Wettkämpfe
F1–F2: keine; F3: 2 bis 4

Wettkampfart
F1: keine; F2–F3: Wettbewerbe in der Interregion (Ost, Mitte, West)

Selektionsrichtlinien
–$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|0|T1|fr$c$, $t$MENTAL
• Fixer les objectifs de la saison
• Visualisation de nouveaux tricks, techniques de respiration, dialogue interne
• Développer la concentration : routines avant le saut, routine de pré-départ simple (respiration, regard, mot-clé)
• Routine de compétition, gestion de la pression

ON-SNOW
• Acquérir les Skills-Checks T1–T2 jumps, rails et halfpipe
• Conditions préalables sur la neige : rouler en switch, set-up turns, tricks sur piste
• Élargir le répertoire de tricks dans tous les sens de rotation
• Composer des runs en slopestyle et en halfpipe et les exercer en simulation de compétition

OFF-SNOW SPÉCIFIQUE AU SPORT
• Bag, trampoline/airtrack et dry slope/inline : basics au début de l'été, progression à la fin de l'été
• Skills-Checks acrobatie et inline : T1 niveau Sportster, T2 niveau Contender

ATHLÉTISME
• Endurance : endurance de base, en VP2 et VWP formes d'intervalles (ludiques), en hiver endurance de base pour la récupération
• Mobilité/souplesse : exercices dynamiques et statiques avant et après l'effort (échauffement, retour au calme, yoga)
• Force : technique à la barre avec le poids du corps et une légère charge additionnelle, contrôle du tronc, formes de sauts avec une réception correcte (axe des jambes) ; ensuite augmenter le potentiel de force et la force explosive, en hiver avec un volume réduit. Window of Opportunity chez les filles (T1) et les garçons (T2)
• Vitesse/agilité : accélérer, freiner et changer de direction consciemment des deux côtés, axe des jambes stable comme lors d'une bonne réception. Tenir compte de la poussée de croissance
• Récupération & prévention : essayer des mesures (programmes de prévention ISPA)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|0|T1|fr$c$, $t$MENTAL
• Saisonziele festlegen
• Visualisierung neuer Tricks, Atemtechniken, Selbstgespräche
• Konzentration aufbauen: Routinen vor dem Sprung, einfache Vorstartroutine (Atemzug, Blick, Schlüsselwort)
• Wettkampfroutine, Umgang mit Druck

ON-SNOW
• Skills-Checks T1–T2 Jumps, Rails und Halfpipe erwerben
• Voraussetzungen auf dem Schnee: switch fahren, Set-Up-Turns, Pistentricks
• Trickrepertoire in alle Drehrichtungen erweitern
• Runs in Slopestyle und Halfpipe zusammensetzen und in Wettkampfsimulationen üben

OFF-SNOW SPORTARTSPEZIFISCH
• Bag, Trampolin/Airtrack und Dry Slope/Inline: Basics im Frühsommer, Progression im Spätsommer
• Skills-Checks Akrobatik und Inline: T1 Stufe Sportster, T2 Stufe Contender

ATHLETIK
• Ausdauer: Grundlagenausdauer, in VP2 und VWP (spielerische) Intervallformen, im Winter Grundlagenausdauer zur Regeneration
• Mobilität/Beweglichkeit: dynamische und statische Übungen vor und nach der Belastung (Warm-Up, Cool-Down, Yoga)
• Kraft: Langhanteltechnik mit Körpergewicht und leichtem Zusatzgewicht, Rumpfkontrolle, Sprungformen mit korrekter Landung (Beinachse); danach Kraftpotenzial und Explosivkraft steigern, im Winter mit reduziertem Volumen. Window of Opportunity bei Mädchen (T1) und Jungen (T2)
• Schnelligkeit/Agilität: bewusst beschleunigen, abbremsen und Richtung wechseln nach beiden Seiten, stabile Beinachse wie bei einer guten Landung. Wachstumsschub beachten
• Regeneration & Prävention: Massnahmen ausprobieren (Präventionsprogramme ISPA)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|0|T1|it$c$, $t$MENTALE
• Definire gli obiettivi stagionali
• Visualizzazione di nuovi trick, tecniche di respirazione, dialogo interno
• Sviluppare la concentrazione: routine prima del salto, semplice routine pre-partenza (respiro, sguardo, parola chiave)
• Routine di gara, gestione della pressione

ON-SNOW
• Acquisire gli Skills-Check T1–T2 jumps, rails e halfpipe
• Presupposti sulla neve: sciare in switch, set-up turns, trick in pista
• Ampliare il repertorio di trick in tutte le direzioni di rotazione
• Comporre run in slopestyle e halfpipe e allenarle in simulazioni di gara

OFF-SNOW SPECIFICO DELLO SPORT
• Bag, trampolino/airtrack e dry slope/inline: basics a inizio estate, progression a fine estate
• Skills-Check acrobatica e inline: T1 livello Sportster, T2 livello Contender

ATLETICA
• Resistenza: resistenza di base, in VP2 e VWP forme intervallate (ludiche), in inverno resistenza di base per il recupero
• Mobilità/flessibilità: esercizi dinamici e statici prima e dopo lo sforzo (riscaldamento, defaticamento, yoga)
• Forza: tecnica al bilanciere con peso corporeo e leggero sovraccarico, controllo del tronco, forme di salto con atterraggio corretto (asse delle gambe); poi aumentare il potenziale di forza e la forza esplosiva, in inverno con volume ridotto. Window of Opportunity nelle ragazze (T1) e nei ragazzi (T2)
• Velocità/agilità: accelerare, frenare e cambiare direzione consapevolmente da entrambi i lati, asse delle gambe stabile come in un buon atterraggio. Tenere conto della fase di crescita
• Rigenerazione & prevenzione: provare misure (programmi di prevenzione ISPA)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|0|T1|it$c$, $t$MENTAL
• Saisonziele festlegen
• Visualisierung neuer Tricks, Atemtechniken, Selbstgespräche
• Konzentration aufbauen: Routinen vor dem Sprung, einfache Vorstartroutine (Atemzug, Blick, Schlüsselwort)
• Wettkampfroutine, Umgang mit Druck

ON-SNOW
• Skills-Checks T1–T2 Jumps, Rails und Halfpipe erwerben
• Voraussetzungen auf dem Schnee: switch fahren, Set-Up-Turns, Pistentricks
• Trickrepertoire in alle Drehrichtungen erweitern
• Runs in Slopestyle und Halfpipe zusammensetzen und in Wettkampfsimulationen üben

OFF-SNOW SPORTARTSPEZIFISCH
• Bag, Trampolin/Airtrack und Dry Slope/Inline: Basics im Frühsommer, Progression im Spätsommer
• Skills-Checks Akrobatik und Inline: T1 Stufe Sportster, T2 Stufe Contender

ATHLETIK
• Ausdauer: Grundlagenausdauer, in VP2 und VWP (spielerische) Intervallformen, im Winter Grundlagenausdauer zur Regeneration
• Mobilität/Beweglichkeit: dynamische und statische Übungen vor und nach der Belastung (Warm-Up, Cool-Down, Yoga)
• Kraft: Langhanteltechnik mit Körpergewicht und leichtem Zusatzgewicht, Rumpfkontrolle, Sprungformen mit korrekter Landung (Beinachse); danach Kraftpotenzial und Explosivkraft steigern, im Winter mit reduziertem Volumen. Window of Opportunity bei Mädchen (T1) und Jungen (T2)
• Schnelligkeit/Agilität: bewusst beschleunigen, abbremsen und Richtung wechseln nach beiden Seiten, stabile Beinachse wie bei einer guten Landung. Wachstumsschub beachten
• Regeneration & Prävention: Massnahmen ausprobieren (Präventionsprogramme ISPA)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|0|T1|en$c$, $t$MENTAL
• Set season goals
• Visualising new tricks, breathing techniques, self-talk
• Building concentration: pre-jump routines, simple pre-start routine (breath, gaze, key word)
• Competition routine, dealing with pressure

ON-SNOW
• Achieve the Skills-Checks T1–T2 jumps, rails and halfpipe
• Prerequisites on snow: riding switch, set-up turns, piste tricks
• Expand the trick repertoire in all spin directions
• Put together slopestyle and halfpipe runs and practise them in competition simulations

OFF-SNOW SPORT-SPECIFIC
• Bag, trampoline/airtrack and dry slope/inline: basics in early summer, progression in late summer
• Skills-Checks acrobatics and inline: T1 Sportster level, T2 Contender level

ATHLETICS
• Endurance: basic endurance, (playful) interval forms in VP2 and VWP, in winter basic endurance for recovery
• Mobility/flexibility: dynamic and static exercises before and after exercise (warm-up, cool-down, yoga)
• Strength: barbell technique with body weight and light additional load, core control, jumping forms with correct landing (leg axis); then increase strength potential and explosive strength, with reduced volume in winter. Window of Opportunity for girls (T1) and boys (T2)
• Speed/agility: accelerate, brake and change direction deliberately to both sides, stable leg axis as in a good landing. Take the growth spurt into account
• Recovery & prevention: try out measures (ISPA prevention programmes)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|0|T1|en$c$, $t$MENTAL
• Saisonziele festlegen
• Visualisierung neuer Tricks, Atemtechniken, Selbstgespräche
• Konzentration aufbauen: Routinen vor dem Sprung, einfache Vorstartroutine (Atemzug, Blick, Schlüsselwort)
• Wettkampfroutine, Umgang mit Druck

ON-SNOW
• Skills-Checks T1–T2 Jumps, Rails und Halfpipe erwerben
• Voraussetzungen auf dem Schnee: switch fahren, Set-Up-Turns, Pistentricks
• Trickrepertoire in alle Drehrichtungen erweitern
• Runs in Slopestyle und Halfpipe zusammensetzen und in Wettkampfsimulationen üben

OFF-SNOW SPORTARTSPEZIFISCH
• Bag, Trampolin/Airtrack und Dry Slope/Inline: Basics im Frühsommer, Progression im Spätsommer
• Skills-Checks Akrobatik und Inline: T1 Stufe Sportster, T2 Stufe Contender

ATHLETIK
• Ausdauer: Grundlagenausdauer, in VP2 und VWP (spielerische) Intervallformen, im Winter Grundlagenausdauer zur Regeneration
• Mobilität/Beweglichkeit: dynamische und statische Übungen vor und nach der Belastung (Warm-Up, Cool-Down, Yoga)
• Kraft: Langhanteltechnik mit Körpergewicht und leichtem Zusatzgewicht, Rumpfkontrolle, Sprungformen mit korrekter Landung (Beinachse); danach Kraftpotenzial und Explosivkraft steigern, im Winter mit reduziertem Volumen. Window of Opportunity bei Mädchen (T1) und Jungen (T2)
• Schnelligkeit/Agilität: bewusst beschleunigen, abbremsen und Richtung wechseln nach beiden Seiten, stabile Beinachse wie bei einer guten Landung. Wachstumsschub beachten
• Regeneration & Prävention: Massnahmen ausprobieren (Präventionsprogramme ISPA)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|0|T3|fr$c$, $t$MENTAL
• Fixer les objectifs de la saison
• Visualisation de nouveaux tricks, techniques de respiration, dialogue interne
• Développer la concentration : routines avant le saut, focus trick après trick sur tout le run
• Routine de compétition, gestion de la pression, reset après une erreur, tactique de run selon le parcours, le vent et le score

ON-SNOW
• Acquérir les Skills-Checks T3–T4 jumps, rails et halfpipe, poser les bases des doubles, promotion selon les forces individuelles
• Transférer les nouveaux tricks du bag sur la neige
• Exercer des runs de slopestyle et de halfpipe en simulation de compétition, les adapter à la concurrence et aux conditions (météo, neige, park)

OFF-SNOW SPÉCIFIQUE AU SPORT
• Bag, trampoline/airtrack et dry slope : basics au début de l'été, progression à la fin de l'été
• Skills-Checks acrobatie et inline : T3 niveau Performer, T4 niveau Rookie

ATHLÉTISME
• Endurance : priorités d'entraînement selon le diagnostic de performance, endurance de base et formes d'intervalles, en hiver pour la récupération
• Mobilité/souplesse : exercices dynamiques et statiques, mobilisation avec rouleau de massage
• Force : exercices de force musculaire à volume élevé, technique à la barre des exercices de puissance musculaire, puis force maximale (coordination intramusculaire) et force explosive avec et sans charge additionnelle ; en hiver intensité élevée avec un volume réduit, programmes de prévention
• Vitesse/agilité : développer séparément le départ et la vitesse maximale, changements de direction en pleine course, séries de sprints de même qualité ; base pour le pop, l'impulsion et la réception
• Test de performance : T3 Powertest/test de performance de la relève, T4 test CNP (Nordboard, jump) en mai et fin septembre
• Récupération & prévention : mettre en place des mesures (programmes de prévention)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|0|T3|fr$c$, $t$MENTAL
• Saisonziele festlegen
• Visualisierung neuer Tricks, Atemtechniken, Selbstgespräche
• Konzentration aufbauen: Routinen vor dem Sprung, Fokus Trick für Trick über den ganzen Run
• Wettkampfroutine, Umgang mit Druck, Reset nach Fehlern, Run-Taktik nach Kurs, Wind und Punktestand

ON-SNOW
• Skills-Checks T3–T4 Jumps, Rails und Halfpipe erwerben, Grundlagen für die Doubles legen, Förderung gemäss individuellen Stärken
• Neue Tricks vom Bag auf den Schnee übertragen
• Slopestyle- und Halfpipe-Runs in Wettkampfsimulationen üben, an Konkurrenz und Bedingungen anpassen (Wetter, Schnee, Park)

OFF-SNOW SPORTARTSPEZIFISCH
• Bag, Trampolin/Airtrack und Dry Slope: Basics im Frühsommer, Progression im Spätsommer
• Skills-Checks Akrobatik und Inline: T3 Stufe Performer, T4 Stufe Rookie

ATHLETIK
• Ausdauer: Trainingsfokus nach Leistungsdiagnostik, Grundlagenausdauer und Intervallformen, im Winter zur Regeneration
• Mobilität/Beweglichkeit: dynamische und statische Übungen, Mobilisation mit Faszienrolle
• Kraft: Muskelkraftübungen mit hohem Umfang, Langhanteltechnik der Muskelleistungsübungen, dann Maximalkraft (intramuskuläre Koordination) und Explosivkraft mit und ohne Zusatzlast; im Winter hohe Intensität bei reduziertem Umfang, Präventionsprogramme
• Schnelligkeit/Agilität: Antritt und Höchsttempo getrennt entwickeln, Richtungswechsel aus vollem Lauf, Sprintserien in gleicher Qualität; Basis für Pop, Absprung und Landung
• Leistungstest: T3 Powertest/Nachwuchsleistungstest, T4 NLZ-Test (Nordboard, Jump) im Mai und Ende September
• Regeneration & Prävention: Massnahmen implementieren (Präventionsprogramme)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|0|T3|it$c$, $t$MENTALE
• Definire gli obiettivi stagionali
• Visualizzazione di nuovi trick, tecniche di respirazione, dialogo interno
• Sviluppare la concentrazione: routine prima del salto, focus trick dopo trick su tutta la run
• Routine di gara, gestione della pressione, reset dopo gli errori, tattica di run secondo il percorso, il vento e il punteggio

ON-SNOW
• Acquisire gli Skills-Check T3–T4 jumps, rails e halfpipe, porre le basi per i double, promozione secondo i punti forti individuali
• Trasferire i nuovi trick dal bag alla neve
• Allenare run di slopestyle e halfpipe in simulazioni di gara, adattarle alla concorrenza e alle condizioni (meteo, neve, park)

OFF-SNOW SPECIFICO DELLO SPORT
• Bag, trampolino/airtrack e dry slope: basics a inizio estate, progression a fine estate
• Skills-Check acrobatica e inline: T3 livello Performer, T4 livello Rookie

ATLETICA
• Resistenza: priorità di allenamento secondo la diagnostica della prestazione, resistenza di base e forme intervallate, in inverno per il recupero
• Mobilità/flessibilità: esercizi dinamici e statici, mobilizzazione con il rullo per fasce
• Forza: esercizi di forza muscolare con volume elevato, tecnica al bilanciere degli esercizi di potenza muscolare, poi forza massima (coordinazione intramuscolare) e forza esplosiva con e senza sovraccarico; in inverno intensità elevata con volume ridotto, programmi di prevenzione
• Velocità/agilità: sviluppare separatamente partenza e velocità massima, cambi di direzione in piena corsa, serie di sprint della stessa qualità; base per pop, stacco e atterraggio
• Test di prestazione: T3 Powertest/test di prestazione per giovani, T4 test CNP (Nordboard, jump) a maggio e a fine settembre
• Rigenerazione & prevenzione: implementare misure (programmi di prevenzione)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|0|T3|it$c$, $t$MENTAL
• Saisonziele festlegen
• Visualisierung neuer Tricks, Atemtechniken, Selbstgespräche
• Konzentration aufbauen: Routinen vor dem Sprung, Fokus Trick für Trick über den ganzen Run
• Wettkampfroutine, Umgang mit Druck, Reset nach Fehlern, Run-Taktik nach Kurs, Wind und Punktestand

ON-SNOW
• Skills-Checks T3–T4 Jumps, Rails und Halfpipe erwerben, Grundlagen für die Doubles legen, Förderung gemäss individuellen Stärken
• Neue Tricks vom Bag auf den Schnee übertragen
• Slopestyle- und Halfpipe-Runs in Wettkampfsimulationen üben, an Konkurrenz und Bedingungen anpassen (Wetter, Schnee, Park)

OFF-SNOW SPORTARTSPEZIFISCH
• Bag, Trampolin/Airtrack und Dry Slope: Basics im Frühsommer, Progression im Spätsommer
• Skills-Checks Akrobatik und Inline: T3 Stufe Performer, T4 Stufe Rookie

ATHLETIK
• Ausdauer: Trainingsfokus nach Leistungsdiagnostik, Grundlagenausdauer und Intervallformen, im Winter zur Regeneration
• Mobilität/Beweglichkeit: dynamische und statische Übungen, Mobilisation mit Faszienrolle
• Kraft: Muskelkraftübungen mit hohem Umfang, Langhanteltechnik der Muskelleistungsübungen, dann Maximalkraft (intramuskuläre Koordination) und Explosivkraft mit und ohne Zusatzlast; im Winter hohe Intensität bei reduziertem Umfang, Präventionsprogramme
• Schnelligkeit/Agilität: Antritt und Höchsttempo getrennt entwickeln, Richtungswechsel aus vollem Lauf, Sprintserien in gleicher Qualität; Basis für Pop, Absprung und Landung
• Leistungstest: T3 Powertest/Nachwuchsleistungstest, T4 NLZ-Test (Nordboard, Jump) im Mai und Ende September
• Regeneration & Prävention: Massnahmen implementieren (Präventionsprogramme)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|0|T3|en$c$, $t$MENTAL
• Set season goals
• Visualising new tricks, breathing techniques, self-talk
• Building concentration: pre-jump routines, focus trick by trick over the whole run
• Competition routine, dealing with pressure, reset after mistakes, run tactics according to course, wind and score

ON-SNOW
• Achieve the Skills-Checks T3–T4 jumps, rails and halfpipe, lay the foundations for doubles, development according to individual strengths
• Transfer new tricks from the bag to snow
• Practise slopestyle and halfpipe runs in competition simulations, adapt them to the competition and conditions (weather, snow, park)

OFF-SNOW SPORT-SPECIFIC
• Bag, trampoline/airtrack and dry slope: basics in early summer, progression in late summer
• Skills-Checks acrobatics and inline: T3 Performer level, T4 Rookie level

ATHLETICS
• Endurance: training focus based on performance diagnostics, basic endurance and interval forms, in winter for recovery
• Mobility/flexibility: dynamic and static exercises, mobilisation with a foam roller
• Strength: high-volume muscular strength exercises, barbell technique for muscular power exercises, then maximal strength (intramuscular coordination) and explosive strength with and without additional load; in winter high intensity with reduced volume, prevention programmes
• Speed/agility: develop acceleration and top speed separately, changes of direction at full speed, sprint series of equal quality; basis for pop, take-off and landing
• Performance test: T3 power test/youth performance test, T4 NTC test (Nordboard, jump) in May and at the end of September
• Recovery & prevention: implement measures (prevention programmes)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|0|T3|en$c$, $t$MENTAL
• Saisonziele festlegen
• Visualisierung neuer Tricks, Atemtechniken, Selbstgespräche
• Konzentration aufbauen: Routinen vor dem Sprung, Fokus Trick für Trick über den ganzen Run
• Wettkampfroutine, Umgang mit Druck, Reset nach Fehlern, Run-Taktik nach Kurs, Wind und Punktestand

ON-SNOW
• Skills-Checks T3–T4 Jumps, Rails und Halfpipe erwerben, Grundlagen für die Doubles legen, Förderung gemäss individuellen Stärken
• Neue Tricks vom Bag auf den Schnee übertragen
• Slopestyle- und Halfpipe-Runs in Wettkampfsimulationen üben, an Konkurrenz und Bedingungen anpassen (Wetter, Schnee, Park)

OFF-SNOW SPORTARTSPEZIFISCH
• Bag, Trampolin/Airtrack und Dry Slope: Basics im Frühsommer, Progression im Spätsommer
• Skills-Checks Akrobatik und Inline: T3 Stufe Performer, T4 Stufe Rookie

ATHLETIK
• Ausdauer: Trainingsfokus nach Leistungsdiagnostik, Grundlagenausdauer und Intervallformen, im Winter zur Regeneration
• Mobilität/Beweglichkeit: dynamische und statische Übungen, Mobilisation mit Faszienrolle
• Kraft: Muskelkraftübungen mit hohem Umfang, Langhanteltechnik der Muskelleistungsübungen, dann Maximalkraft (intramuskuläre Koordination) und Explosivkraft mit und ohne Zusatzlast; im Winter hohe Intensität bei reduziertem Umfang, Präventionsprogramme
• Schnelligkeit/Agilität: Antritt und Höchsttempo getrennt entwickeln, Richtungswechsel aus vollem Lauf, Sprintserien in gleicher Qualität; Basis für Pop, Absprung und Landung
• Leistungstest: T3 Powertest/Nachwuchsleistungstest, T4 NLZ-Test (Nordboard, Jump) im Mai und Ende September
• Regeneration & Prävention: Massnahmen implementieren (Präventionsprogramme)$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|1|T1|fr$c$, $t$Par an : 400–800h de temps d'entraînement

HIVER
• On-snow : 45–80 jours de neige, Ø 1,5–3 jours par semaine
• Off-snow : athlétisme 2–2,5h/semaine, entraînement mental 0,5h/semaine

ÉTÉ
• On-snow : 5 jours de neige
• Off-snow : bag 10–30 sessions ; dry slope 2h, trampoline 2h, athlétisme 5–6,5h, entraînement mental 0,5h par semaine$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|1|T1|fr$c$, $t$Pro Jahr: 400–800h Trainingszeit

WINTER
• On-Snow: 45–80 Schneetage, Ø 1,5–3 Tage pro Woche
• Off-Snow: Athletik 2–2,5h/Woche, Mentaltraining 0,5h/Woche

SOMMER
• On-Snow: 5 Schneetage
• Off-Snow: Bag 10–30 Sessions; Dry Slope 2h, Trampolin 2h, Athletik 5–6,5h, Mentaltraining 0,5h pro Woche$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|1|T1|it$c$, $t$All'anno: 400–800h di tempo di allenamento

INVERNO
• On-snow: 45–80 giorni sulla neve, Ø 1,5–3 giorni a settimana
• Off-snow: atletica 2–2,5h/settimana, allenamento mentale 0,5h/settimana

ESTATE
• On-snow: 5 giorni sulla neve
• Off-snow: bag 10–30 sessioni; dry slope 2h, trampolino 2h, atletica 5–6,5h, allenamento mentale 0,5h a settimana$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|1|T1|it$c$, $t$Pro Jahr: 400–800h Trainingszeit

WINTER
• On-Snow: 45–80 Schneetage, Ø 1,5–3 Tage pro Woche
• Off-Snow: Athletik 2–2,5h/Woche, Mentaltraining 0,5h/Woche

SOMMER
• On-Snow: 5 Schneetage
• Off-Snow: Bag 10–30 Sessions; Dry Slope 2h, Trampolin 2h, Athletik 5–6,5h, Mentaltraining 0,5h pro Woche$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|1|T1|en$c$, $t$Per year: 400–800h training time

WINTER
• On-snow: 45–80 snow days, Ø 1.5–3 days per week
• Off-snow: athletics 2–2.5h/week, mental training 0.5h/week

SUMMER
• On-snow: 5 snow days
• Off-snow: bag 10–30 sessions; dry slope 2h, trampoline 2h, athletics 5–6.5h, mental training 0.5h per week$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|1|T1|en$c$, $t$Pro Jahr: 400–800h Trainingszeit

WINTER
• On-Snow: 45–80 Schneetage, Ø 1,5–3 Tage pro Woche
• Off-Snow: Athletik 2–2,5h/Woche, Mentaltraining 0,5h/Woche

SOMMER
• On-Snow: 5 Schneetage
• Off-Snow: Bag 10–30 Sessions; Dry Slope 2h, Trampolin 2h, Athletik 5–6,5h, Mentaltraining 0,5h pro Woche$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|1|T3|fr$c$, $t$Par an : 700–1000h de temps d'entraînement

HIVER
• On-snow : 80–120 jours de neige, Ø 3–4,5 jours par semaine
• Off-snow : athlétisme 3h/semaine, entraînement mental 1h/semaine

ÉTÉ
• On-snow : 10–20 jours de neige
• Off-snow : bag 30–60 sessions ; dry slope 2h, trampoline 1h, athlétisme 8h, entraînement mental 1h par semaine$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|1|T3|fr$c$, $t$Pro Jahr: 700–1000h Trainingszeit

WINTER
• On-Snow: 80–120 Schneetage, Ø 3–4,5 Tage pro Woche
• Off-Snow: Athletik 3h/Woche, Mentaltraining 1h/Woche

SOMMER
• On-Snow: 10–20 Schneetage
• Off-Snow: Bag 30–60 Sessions; Dry Slope 2h, Trampolin 1h, Athletik 8h, Mentaltraining 1h pro Woche$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|1|T3|it$c$, $t$All'anno: 700–1000h di tempo di allenamento

INVERNO
• On-snow: 80–120 giorni sulla neve, Ø 3–4,5 giorni a settimana
• Off-snow: atletica 3h/settimana, allenamento mentale 1h/settimana

ESTATE
• On-snow: 10–20 giorni sulla neve
• Off-snow: bag 30–60 sessioni; dry slope 2h, trampolino 1h, atletica 8h, allenamento mentale 1h a settimana$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|1|T3|it$c$, $t$Pro Jahr: 700–1000h Trainingszeit

WINTER
• On-Snow: 80–120 Schneetage, Ø 3–4,5 Tage pro Woche
• Off-Snow: Athletik 3h/Woche, Mentaltraining 1h/Woche

SOMMER
• On-Snow: 10–20 Schneetage
• Off-Snow: Bag 30–60 Sessions; Dry Slope 2h, Trampolin 1h, Athletik 8h, Mentaltraining 1h pro Woche$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|1|T3|en$c$, $t$Per year: 700–1000h training time

WINTER
• On-snow: 80–120 snow days, Ø 3–4.5 days per week
• Off-snow: athletics 3h/week, mental training 1h/week

SUMMER
• On-snow: 10–20 snow days
• Off-snow: bag 30–60 sessions; dry slope 2h, trampoline 1h, athletics 8h, mental training 1h per week$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|1|T3|en$c$, $t$Pro Jahr: 700–1000h Trainingszeit

WINTER
• On-Snow: 80–120 Schneetage, Ø 3–4,5 Tage pro Woche
• Off-Snow: Athletik 3h/Woche, Mentaltraining 1h/Woche

SOMMER
• On-Snow: 10–20 Schneetage
• Off-Snow: Bag 30–60 Sessions; Dry Slope 2h, Trampolin 1h, Athletik 8h, Mentaltraining 1h pro Woche$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|2|T1|fr$c$, $t$Famille, entraîneur·es & groupe d'entraînement
Environnement sportif et scolaire

CADRE
CRP, ski-club, club sportif

SWISS OLYMPIC CARD
T1 : Talent Card locale ; T2 : Talent Card locale ou régionale

COMPÉTITIONS
T1 : 4 à 6 ; T2 : style 4 à 6

TYPE DE COMPÉTITION
Compétitions dans l'interrégion (Est, Centre, Ouest) et niveau National-C

DIRECTIVES DE SÉLECTION
Évaluation de l'entraîneur local (assessment), résultats de compétition (tours interrégionaux : BUZZ Tour, Eastside Tour, Tour Freestyle Romand) ; dès T2 en plus Powertest et TCU$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|2|T1|fr$c$, $t$Familie, Trainer:innen & Trainingsgruppe
Sportlich-schulisches Umfeld

KADER
RLZ, Skiclub, Sportclub

SWISS OLYMPIC CARD
T1: Talent Card lokal; T2: Talent Card lokal oder regional

WETTKÄMPFE
T1: 4 bis 6; T2: Style 4 bis 6

WETTKAMPFART
Wettbewerbe in der Interregion (Ost, Mitte, West) und Stufe National-C

SELEKTIONSRICHTLINIEN
Heimtrainereinschätzung (Assessment), Wettkampfresultate (interregionale Touren: BUZZ Tour, Eastside Tour, Tour Freestyle Romand); ab T2 zusätzlich Powertest und TCU$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|2|T1|it$c$, $t$Famiglia, allenatori/allenatrici & gruppo di allenamento
Ambiente sportivo e scolastico

QUADRI
CRP, sci club, club sportivo

SWISS OLYMPIC CARD
T1: Talent Card locale; T2: Talent Card locale o regionale

GARE
T1: da 4 a 6; T2: style da 4 a 6

TIPO DI GARA
Gare nell'interregione (Est, Centro, Ovest) e livello Nazionale-C

DIRETTIVE DI SELEZIONE
Valutazione dell'allenatore locale (assessment), risultati di gara (tour interregionali: BUZZ Tour, Eastside Tour, Tour Freestyle Romand); da T2 inoltre Powertest e TCU$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|2|T1|it$c$, $t$Familie, Trainer:innen & Trainingsgruppe
Sportlich-schulisches Umfeld

KADER
RLZ, Skiclub, Sportclub

SWISS OLYMPIC CARD
T1: Talent Card lokal; T2: Talent Card lokal oder regional

WETTKÄMPFE
T1: 4 bis 6; T2: Style 4 bis 6

WETTKAMPFART
Wettbewerbe in der Interregion (Ost, Mitte, West) und Stufe National-C

SELEKTIONSRICHTLINIEN
Heimtrainereinschätzung (Assessment), Wettkampfresultate (interregionale Touren: BUZZ Tour, Eastside Tour, Tour Freestyle Romand); ab T2 zusätzlich Powertest und TCU$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|2|T1|en$c$, $t$Family, coaches & training group
Sports and school environment

SQUAD
RTC, ski club, sports club

SWISS OLYMPIC CARD
T1: Talent Card local; T2: Talent Card local or regional

COMPETITIONS
T1: 4 to 6; T2: style 4 to 6

COMPETITION TYPE
Competitions in the interregion (East, Central, West) and National-C level

SELECTION GUIDELINES
Home coach assessment, competition results (interregional tours: BUZZ Tour, Eastside Tour, Tour Freestyle Romand); from T2 also power test and TCU$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|2|T1|en$c$, $t$Familie, Trainer:innen & Trainingsgruppe
Sportlich-schulisches Umfeld

KADER
RLZ, Skiclub, Sportclub

SWISS OLYMPIC CARD
T1: Talent Card lokal; T2: Talent Card lokal oder regional

WETTKÄMPFE
T1: 4 bis 6; T2: Style 4 bis 6

WETTKAMPFART
Wettbewerbe in der Interregion (Ost, Mitte, West) und Stufe National-C

SELEKTIONSRICHTLINIEN
Heimtrainereinschätzung (Assessment), Wettkampfresultate (interregionale Touren: BUZZ Tour, Eastside Tour, Tour Freestyle Romand); ab T2 zusätzlich Powertest und TCU$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|2|T3|fr$c$, $t$Famille, entraîneur·es & groupe d'entraînement, CRP
Environnement sportif et scolaire/professionnel, écoles avec solution pour le sport

CADRE
T3 : CRP, CNP ; T4 : CRP, CNP, cadre Swiss-Ski

SWISS OLYMPIC CARD
T3 : Talent Card régionale ou nationale ; T4 : Talent Card nationale

COMPÉTITIONS
T3 : style 8 à 10 ; T4 : ~10

TYPE DE COMPÉTITION
NC/FIS Junior, NB/FIS, NA/Coupe d'Europe, CM juniors, EYOF, YOG

DIRECTIVES DE SÉLECTION
Évaluation de l'entraîneur local (assessment), Powertest, TCU on- et off-snow, liste FIS/WSPL ; T4 en plus Powertest min. 55 points (dès 26/27 60 points), TCU min. 80 %, test CNP$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|2|T3|fr$c$, $t$Familie, Trainer:innen & Trainingsgruppe, RLZ
Sportlich-schulisches/berufliches Umfeld, Schulen mit Sportlösung

KADER
T3: RLZ, NLZ; T4: RLZ, NLZ, Swiss-Ski Kader

SWISS OLYMPIC CARD
T3: Talent Card regional oder national; T4: Talent Card national

WETTKÄMPFE
T3: Style 8 bis 10; T4: ~10

WETTKAMPFART
NC/FIS Junior, NB/FIS, NA/Europa Cup, JWM, EYOF, YOG

SELEKTIONSRICHTLINIEN
Heimtrainereinschätzung (Assessment), Powertest, TCU On- und Off-Snow, FIS/WSPL-Liste; T4 zusätzlich Powertest mind. 55 Punkte (ab 26/27 60 Punkte), TCU mind. 80 %, NLZ-Test$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|2|T3|it$c$, $t$Famiglia, allenatori/allenatrici & gruppo di allenamento, CRP
Ambiente sportivo e scolastico/professionale, scuole con soluzione per lo sport

QUADRI
T3: CRP, CNP; T4: CRP, CNP, quadro Swiss-Ski

SWISS OLYMPIC CARD
T3: Talent Card regionale o nazionale; T4: Talent Card nazionale

GARE
T3: style da 8 a 10; T4: ~10

TIPO DI GARA
NC/FIS Junior, NB/FIS, NA/Coppa Europa, Mondiali juniores, EYOF, YOG

DIRETTIVE DI SELEZIONE
Valutazione dell'allenatore locale (assessment), Powertest, TCU on- e off-snow, lista FIS/WSPL; T4 inoltre Powertest min. 55 punti (da 26/27 60 punti), TCU min. 80 %, test CNP$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|2|T3|it$c$, $t$Familie, Trainer:innen & Trainingsgruppe, RLZ
Sportlich-schulisches/berufliches Umfeld, Schulen mit Sportlösung

KADER
T3: RLZ, NLZ; T4: RLZ, NLZ, Swiss-Ski Kader

SWISS OLYMPIC CARD
T3: Talent Card regional oder national; T4: Talent Card national

WETTKÄMPFE
T3: Style 8 bis 10; T4: ~10

WETTKAMPFART
NC/FIS Junior, NB/FIS, NA/Europa Cup, JWM, EYOF, YOG

SELEKTIONSRICHTLINIEN
Heimtrainereinschätzung (Assessment), Powertest, TCU On- und Off-Snow, FIS/WSPL-Liste; T4 zusätzlich Powertest mind. 55 Punkte (ab 26/27 60 Punkte), TCU mind. 80 %, NLZ-Test$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|2|T3|en$c$, $t$Family, coaches & training group, RTC
Sports and school/work environment, schools with sports arrangements

SQUAD
T3: RTC, NTC; T4: RTC, NTC, Swiss-Ski squad

SWISS OLYMPIC CARD
T3: Talent Card regional or national; T4: Talent Card national

COMPETITIONS
T3: style 8 to 10; T4: ~10

COMPETITION TYPE
NC/FIS Junior, NB/FIS, NA/Europa Cup, Junior World Championships, EYOF, YOG

SELECTION GUIDELINES
Home coach assessment, power test, TCU on- and off-snow, FIS/WSPL list; T4 also power test min. 55 points (from 26/27 60 points), TCU min. 80 %, NTC test$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|2|T3|en$c$, $t$Familie, Trainer:innen & Trainingsgruppe, RLZ
Sportlich-schulisches/berufliches Umfeld, Schulen mit Sportlösung

KADER
T3: RLZ, NLZ; T4: RLZ, NLZ, Swiss-Ski Kader

SWISS OLYMPIC CARD
T3: Talent Card regional oder national; T4: Talent Card national

WETTKÄMPFE
T3: Style 8 bis 10; T4: ~10

WETTKAMPFART
NC/FIS Junior, NB/FIS, NA/Europa Cup, JWM, EYOF, YOG

SELEKTIONSRICHTLINIEN
Heimtrainereinschätzung (Assessment), Powertest, TCU On- und Off-Snow, FIS/WSPL-Liste; T4 zusätzlich Powertest mind. 55 Punkte (ab 26/27 60 Punkte), TCU mind. 80 %, NLZ-Test$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|0|E1|fr$c$, $t$MENTAL
• Appliquer une routine d'activation mentale établie avant la compétition, utiliser les techniques de respiration et le dialogue interne sous pression, après un échec diriger le focus sur la tâche suivante, atteindre l'état de performance optimal

ON-SNOW
• Profil d'exigences Coupe du monde : big air, slopestyle et halfpipe selon les résultats des podiums
• Adapter les runs à la concurrence et aux conditions
• Entre les compétitions : consolider et élargir les runs

OFF-SNOW SPÉCIFIQUE AU SPORT
• Bag : nouveaux tricks de compétition

ATHLÉTISME
• Endurance : priorités d'entraînement selon le diagnostic de performance
• Mobilité/souplesse : comme routine quotidienne, mobilisation avec rouleau de massage
• Force : force explosive et maximale, en hiver intensité élevée avec un volume réduit, programmes de prévention
• Vitesse/agilité : pilotée individuellement par des tests, pic avant les compétitions importantes
• Test de performance : test CNP ou DP Macolin
• Récupération & prévention : piloter individuellement$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|0|E1|fr$c$, $t$MENTAL
• Vor dem Wettkampf eine etablierte mentale Aktivierungsroutine anwenden, bei Druck Atemtechniken und Selbstgespräche einsetzen, nach Rückschlägen den Fokus auf die nächste Aufgabe lenken, optimalen Leistungszustand abrufen

ON-SNOW
• Anforderungsprofil Weltcup: Big Air, Slopestyle und Halfpipe gemäss Podestresultaten
• Runs an Konkurrenz und Bedingungen anpassen
• Zwischen den Wettkämpfen: Runs festigen und erweitern

OFF-SNOW SPORTARTSPEZIFISCH
• Bag: neue Wettkampftricks

ATHLETIK
• Ausdauer: Trainingsfokus nach Leistungsdiagnostik
• Mobilität/Beweglichkeit: als Tagesroutine, Mobilisation mit Faszienrolle
• Kraft: Explosiv- und Maximalkraft, im Winter hohe Intensität bei reduziertem Umfang, Präventionsprogramme
• Schnelligkeit/Agilität: individuell über Tests gesteuert, Spitze vor wichtigen Wettkämpfen
• Leistungstest: NLZ-Test oder LD Magglingen
• Regeneration & Prävention: individuell steuern$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|0|E1|it$c$, $t$MENTALE
• Applicare una routine di attivazione mentale consolidata prima della gara, usare tecniche di respirazione e dialogo interno sotto pressione, dopo una battuta d'arresto spostare il focus sul compito successivo, raggiungere lo stato di prestazione ottimale

ON-SNOW
• Profilo dei requisiti Coppa del mondo: big air, slopestyle e halfpipe secondo i risultati dei podi
• Adattare le run alla concorrenza e alle condizioni
• Tra le gare: consolidare e ampliare le run

OFF-SNOW SPECIFICO DELLO SPORT
• Bag: nuovi trick di gara

ATLETICA
• Resistenza: priorità di allenamento secondo la diagnostica della prestazione
• Mobilità/flessibilità: come routine quotidiana, mobilizzazione con il rullo per fasce
• Forza: forza esplosiva e massima, in inverno intensità elevata con volume ridotto, programmi di prevenzione
• Velocità/agilità: guidata individualmente dai test, picco prima delle gare importanti
• Test di prestazione: test CNP o DP Macolin
• Rigenerazione & prevenzione: gestire individualmente$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|0|E1|it$c$, $t$MENTAL
• Vor dem Wettkampf eine etablierte mentale Aktivierungsroutine anwenden, bei Druck Atemtechniken und Selbstgespräche einsetzen, nach Rückschlägen den Fokus auf die nächste Aufgabe lenken, optimalen Leistungszustand abrufen

ON-SNOW
• Anforderungsprofil Weltcup: Big Air, Slopestyle und Halfpipe gemäss Podestresultaten
• Runs an Konkurrenz und Bedingungen anpassen
• Zwischen den Wettkämpfen: Runs festigen und erweitern

OFF-SNOW SPORTARTSPEZIFISCH
• Bag: neue Wettkampftricks

ATHLETIK
• Ausdauer: Trainingsfokus nach Leistungsdiagnostik
• Mobilität/Beweglichkeit: als Tagesroutine, Mobilisation mit Faszienrolle
• Kraft: Explosiv- und Maximalkraft, im Winter hohe Intensität bei reduziertem Umfang, Präventionsprogramme
• Schnelligkeit/Agilität: individuell über Tests gesteuert, Spitze vor wichtigen Wettkämpfen
• Leistungstest: NLZ-Test oder LD Magglingen
• Regeneration & Prävention: individuell steuern$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|0|E1|en$c$, $t$MENTAL
• Use an established mental activation routine before competition, use breathing techniques and self-talk under pressure, refocus on the next task after setbacks, access the optimal performance state

ON-SNOW
• World Cup requirement profile: big air, slopestyle and halfpipe based on podium results
• Adapt runs to the competition and conditions
• Between competitions: consolidate and expand runs

OFF-SNOW SPORT-SPECIFIC
• Bag: new competition tricks

ATHLETICS
• Endurance: training focus based on performance diagnostics
• Mobility/flexibility: as a daily routine, mobilisation with a foam roller
• Strength: explosive and maximal strength, in winter high intensity with reduced volume, prevention programmes
• Speed/agility: individually steered by tests, peak before important competitions
• Performance test: NTC test or PD Magglingen
• Recovery & prevention: manage individually$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|0|E1|en$c$, $t$MENTAL
• Vor dem Wettkampf eine etablierte mentale Aktivierungsroutine anwenden, bei Druck Atemtechniken und Selbstgespräche einsetzen, nach Rückschlägen den Fokus auf die nächste Aufgabe lenken, optimalen Leistungszustand abrufen

ON-SNOW
• Anforderungsprofil Weltcup: Big Air, Slopestyle und Halfpipe gemäss Podestresultaten
• Runs an Konkurrenz und Bedingungen anpassen
• Zwischen den Wettkämpfen: Runs festigen und erweitern

OFF-SNOW SPORTARTSPEZIFISCH
• Bag: neue Wettkampftricks

ATHLETIK
• Ausdauer: Trainingsfokus nach Leistungsdiagnostik
• Mobilität/Beweglichkeit: als Tagesroutine, Mobilisation mit Faszienrolle
• Kraft: Explosiv- und Maximalkraft, im Winter hohe Intensität bei reduziertem Umfang, Präventionsprogramme
• Schnelligkeit/Agilität: individuell über Tests gesteuert, Spitze vor wichtigen Wettkämpfen
• Leistungstest: NLZ-Test oder LD Magglingen
• Regeneration & Prävention: individuell steuern$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|1|E1|fr$c$, $t$Par an : >1000h de temps d'entraînement

HIVER
• On-snow : 100–120 jours de neige, Ø 3–4,5 jours par semaine
• Off-snow : athlétisme 3h/semaine, entraînement mental 1h/semaine

ÉTÉ
• On-snow : 10–20 jours de neige
• Off-snow : bag 50–60 sessions ; athlétisme 8h, entraînement mental 1h par semaine$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|1|E1|fr$c$, $t$Pro Jahr: >1000h Trainingszeit

WINTER
• On-Snow: 100–120 Schneetage, Ø 3–4,5 Tage pro Woche
• Off-Snow: Athletik 3h/Woche, Mentaltraining 1h/Woche

SOMMER
• On-Snow: 10–20 Schneetage
• Off-Snow: Bag 50–60 Sessions; Athletik 8h, Mentaltraining 1h pro Woche$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|1|E1|it$c$, $t$All'anno: >1000h di tempo di allenamento

INVERNO
• On-snow: 100–120 giorni sulla neve, Ø 3–4,5 giorni a settimana
• Off-snow: atletica 3h/settimana, allenamento mentale 1h/settimana

ESTATE
• On-snow: 10–20 giorni sulla neve
• Off-snow: bag 50–60 sessioni; atletica 8h, allenamento mentale 1h a settimana$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|1|E1|it$c$, $t$Pro Jahr: >1000h Trainingszeit

WINTER
• On-Snow: 100–120 Schneetage, Ø 3–4,5 Tage pro Woche
• Off-Snow: Athletik 3h/Woche, Mentaltraining 1h/Woche

SOMMER
• On-Snow: 10–20 Schneetage
• Off-Snow: Bag 50–60 Sessions; Athletik 8h, Mentaltraining 1h pro Woche$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|1|E1|en$c$, $t$Per year: >1000h training time

WINTER
• On-snow: 100–120 snow days, Ø 3–4.5 days per week
• Off-snow: athletics 3h/week, mental training 1h/week

SUMMER
• On-snow: 10–20 snow days
• Off-snow: bag 50–60 sessions; athletics 8h, mental training 1h per week$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|1|E1|en$c$, $t$Pro Jahr: >1000h Trainingszeit

WINTER
• On-Snow: 100–120 Schneetage, Ø 3–4,5 Tage pro Woche
• Off-Snow: Athletik 3h/Woche, Mentaltraining 1h/Woche

SOMMER
• On-Snow: 10–20 Schneetage
• Off-Snow: Bag 50–60 Sessions; Athletik 8h, Mentaltraining 1h pro Woche$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|2|E1|fr$c$, $t$Famille, entraîneur·es & groupe d'entraînement, Swiss-Ski
Environnement sportif et professionnel

CADRE
Cadre Swiss-Ski

SWISS OLYMPIC CARD
E1 : Elite, bronze, argent ; E2 : Elite, argent ou or

COMPÉTITIONS
~12

TYPE DE COMPÉTITION
World Cup, CM, JO

DIRECTIVES DE SÉLECTION
Voir les directives de sélection sur le site de Swiss-Ski$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|2|E1|fr$c$, $t$Familie, Trainer:innen & Trainingsgruppe, Swiss-Ski
Sportlich-berufliches Umfeld

KADER
Swiss-Ski Kader

SWISS OLYMPIC CARD
E1: Elite, Bronze, Silber; E2: Elite, Silber oder Gold

WETTKÄMPFE
~12

WETTKAMPFART
World Cup, WM, OG

SELEKTIONSRICHTLINIEN
Siehe Selektionsrichtlinien auf der Swiss-Ski-Homepage$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|2|E1|it$c$, $t$Famiglia, allenatori/allenatrici & gruppo di allenamento, Swiss-Ski
Ambiente sportivo e professionale

QUADRI
Quadro Swiss-Ski

SWISS OLYMPIC CARD
E1: Elite, bronzo, argento; E2: Elite, argento o oro

GARE
~12

TIPO DI GARA
World Cup, Mondiali, Giochi olimpici

DIRETTIVE DI SELEZIONE
Vedi le direttive di selezione sul sito di Swiss-Ski$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|2|E1|it$c$, $t$Familie, Trainer:innen & Trainingsgruppe, Swiss-Ski
Sportlich-berufliches Umfeld

KADER
Swiss-Ski Kader

SWISS OLYMPIC CARD
E1: Elite, Bronze, Silber; E2: Elite, Silber oder Gold

WETTKÄMPFE
~12

WETTKAMPFART
World Cup, WM, OG

SELEKTIONSRICHTLINIEN
Siehe Selektionsrichtlinien auf der Swiss-Ski-Homepage$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$home|freeski-park-pipe|2|E1|en$c$, $t$Family, coaches & training group, Swiss-Ski
Sports and work environment

SQUAD
Swiss-Ski squad

SWISS OLYMPIC CARD
E1: Elite, bronze, silver; E2: Elite, silver or gold

COMPETITIONS
~12

COMPETITION TYPE
World Cup, World Championships, OG

SELECTION GUIDELINES
See the selection guidelines on the Swiss-Ski website$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|home|freeski-park-pipe|2|E1|en$c$, $t$Familie, Trainer:innen & Trainingsgruppe, Swiss-Ski
Sportlich-berufliches Umfeld

KADER
Swiss-Ski Kader

SWISS OLYMPIC CARD
E1: Elite, Bronze, Silber; E2: Elite, Silber oder Gold

WETTKÄMPFE
~12

WETTKAMPFART
World Cup, WM, OG

SELEKTIONSRICHTLINIEN
Siehe Selektionsrichtlinien auf der Swiss-Ski-Homepage$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$freeski-park-pipe|10|0|1|fr$c$, $t$Skills-Check acrobatie

((Trampoline · Hommes))
• 6x saut droit en série
• 6x Monkey en série
• 6x 180° avec saut intermédiaire
• Line-Jumps (6 lignes)
• saut carpé
• saut assis
• 3x Bank en série
• Side-Roll (bounced)
• 90° to Back to Sideroll

((Trampoline · Femmes))
• 6x saut droit en série
• 6x Monkey en série
• 6x 180° avec saut intermédiaire
• Line-Jumps (6 lignes)
• saut carpé
• saut assis
• 3x Bank en série
• Side-Roll (bounced)
• 90° to Sideroll

((Airtrack))
• 6x saut droit, bras le long du corps
• 180 L
• 180 R
• roulade avant
• roulade arrière
• roulade latérale G
• roulade latérale D
• chandelle 10"
• équilibre sur la tête 10"$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|freeski-park-pipe|10|0|1|fr$c$, $t$Skills-Check Akrobatik

((Trampolin · Männer))
• 6x Strecksprung in Serie
• 6x Monkey in Serie
• 6x 180° mit Sprung dazwischen
• Line-Jumps (6 Linien)
• Bücksprung
• Sitzsprung
• 3x Bank in Serie
• Side-Roll (bounced)
• 90° to Back to Sideroll

((Trampolin · Frauen))
• 6x Strecksprung in Serie
• 6x Monkey in Serie
• 6x 180° mit Sprung dazwischen
• Line-Jumps (6 Linien)
• Bücksprung
• Sitzsprung
• 3x Bank in Serie
• Side-Roll (bounced)
• 90° to Sideroll

((Airtrack))
• 6x Strecksprung, Arme am Körper
• 180 L
• 180 R
• Rolle vorwärts
• Rolle rückwärts
• Seitrolle L
• Seitrolle R
• Kerze 10"
• Kopfstand 10"$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$freeski-park-pipe|10|0|1|it$c$, $t$Skills-Check acrobatica

((Trampolino · Uomini))
• 6x salto teso in serie
• 6x Monkey in serie
• 6x 180° con salto intermedio
• Line-Jumps (6 linee)
• salto carpiato
• salto seduto
• 3x Bank in serie
• Side-Roll (bounced)
• 90° to Back to Sideroll

((Trampolino · Donne))
• 6x salto teso in serie
• 6x Monkey in serie
• 6x 180° con salto intermedio
• Line-Jumps (6 linee)
• salto carpiato
• salto seduto
• 3x Bank in serie
• Side-Roll (bounced)
• 90° to Sideroll

((Airtrack))
• 6x salto teso, braccia lungo il corpo
• 180 L
• 180 R
• capriola avanti
• capriola indietro
• capriola laterale S
• capriola laterale D
• candela 10"
• verticale sulla testa 10"$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
insert into ftem_overrides (cid, txt) values ($c$rev|freeski-park-pipe|10|0|1|it$c$, $t$Skills-Check Akrobatik

((Trampolin · Männer))
• 6x Strecksprung in Serie
• 6x Monkey in Serie
• 6x 180° mit Sprung dazwischen
• Line-Jumps (6 Linien)
• Bücksprung
• Sitzsprung
• 3x Bank in Serie
• Side-Roll (bounced)
• 90° to Back to Sideroll

((Trampolin · Frauen))
• 6x Strecksprung in Serie
• 6x Monkey in Serie
• 6x 180° mit Sprung dazwischen
• Line-Jumps (6 Linien)
• Bücksprung
• Sitzsprung
• 3x Bank in Serie
• Side-Roll (bounced)
• 90° to Sideroll

((Airtrack))
• 6x Strecksprung, Arme am Körper
• 180 L
• 180 R
• Rolle vorwärts
• Rolle rückwärts
• Seitrolle L
• Seitrolle R
• Kerze 10"
• Kopfstand 10"$t$) on conflict (cid) do update set txt = excluded.txt, updated_at = now();
commit;
