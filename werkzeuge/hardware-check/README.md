# Hardware-Check: Was schafft mein PC?

Zeigt Prozessorkerne, Arbeitsspeicher und Grafikkarte und sagt, welches Modell von KIplatz darauf passt: das große (14B), das mittlere (8B) oder das kleine (3B). Die Regel ist dieselbe wie im Programm.

```
python hardware_check.py
```

So sieht das Ergebnis etwa aus:

```
Dein Rechner und KIplatz

Prozessor: 12 Kerne
Arbeitsspeicher: 15,7 GB
Grafikkarte: NVIDIA GeForce RTX 4050 Laptop GPU (eigene Karte), 6,0 GB, gerade frei 2,8 GB
Grafikkarte: Intel(R) UHD Graphics (eingebaut), 2,0 GB

Passt: das kleine Modell (3B), ganz auf der Grafikkarte. Damit kann dein PC auch für die Community arbeiten.
```

Mit `--json` kommt dasselbe als JSON, etwa für eigene Auswertungen.

## So wird entschieden

| Grafikspeicher der Karte, abzüglich 300 MB Reserve | Modell |
|---|---|
| ab 9 000 MB | großes Modell (14B) |
| ab 5 900 MB | mittleres Modell (8B) |
| ab 2 800 MB | kleines Modell (3B) |
| keine passende Karte, ab 15,5 GB Arbeitsspeicher | mittleres Modell auf dem Prozessor |
| sonst | kleines Modell auf dem Prozessor |

Eine eigene Grafikkarte geht vor einer eingebauten. Eine eingebaute zählt nur, wenn es keine eigene gibt und der PC mindestens 8 GB Arbeitsspeicher hat.

## Was der Check liest

Nur Arbeitsspeicher, Prozessorkerne und die Angaben der Grafiktreiber: bei NVIDIA über `nvidia-smi`, das mit dem Treiber kommt, unter Windows zusätzlich die Treiberangaben in der Registrierung (nur lesen). Er ändert nichts, braucht keine Administratorrechte, schickt nichts ins Internet und zeigt weder Rechnernamen noch Seriennummern.

Unter Linux und am Mac funktioniert der Check auch, das Programm von KIplatz gibt es derzeit für Windows. Am Handy und im Browser geht KIplatz unter [kiplatz.at/app](https://kiplatz.at/app/).

**Passt ein Modell?** Dann mach mit: [Programm holen](https://kiplatz.at/rechenkraft-teilen/), und dein PC steht bald in der Bestenliste.
