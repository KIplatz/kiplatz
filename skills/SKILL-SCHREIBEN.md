# Einen Skill schreiben

Ein Skill bringt KIplatz eine feste Arbeitsweise bei. Du schreibst einmal auf, wie eine Sache gehen soll, und musst sie nie wieder erklären. Programmieren musst du dafür nicht können, ein guter Skill ist in 10 Minuten fertig.

Ein Skill ist ein Ordner mit einer einzigen Datei `SKILL.md`. Das Format ist offen, auch andere KI-Programme lesen es. Was du hier schreibst, funktioniert also auch dort, und umgekehrt.

## Die Vorlage

Kopier das in eine neue Datei `SKILL.md` und füll es aus. Im Programm bekommst du dasselbe Muster mit „Neuen Skill schreiben“.

```markdown
---
name: mein-skill
description: Wofür dieser Skill ist, in einem Satz.
---

# Mein Skill

So soll KIplatz vorgehen, wenn dieser Skill gewählt ist:

1. Zuerst …
2. Dann …

Was nie fehlen darf: …
Was nie hinein darf: …
```

| Teil | Was hineinkommt |
|---|---|
| `name:` | Ein kurzer Name aus Kleinbuchstaben, Ziffern und Bindestrichen, höchstens 64 Zeichen. Aus „Rechnung prüfen“ wird `rechnung-pruefen`. So heißt auch der Ordner. |
| `description:` | Ein Satz, wofür der Skill gut ist. Danach sucht man ihn in der Liste aus. |
| darunter | Die Anweisungen, so wie du sie einem Menschen geben würdest. |

## 5 Tipps für einen guten Skill

- Eine Arbeit pro Skill: „Brief ans Amt“ und „Rechnung prüfen“ sind 2 Skills, nicht einer.
- Sag, was KIplatz vorher fragen soll. Fehlt etwas Wichtiges, etwa ein Datum oder ein Betrag, soll es nachfragen statt raten.
- Beschreib das Ergebnis: wie lang, in welcher Reihenfolge, in welchem Ton, per du oder per Sie.
- Schreib die Grenzen hinein, also was nie fehlen darf und was nie hinein darf. Ein Satz wie „Erfinde nichts dazu“ steht in den meisten unserer Vorlagen.
- Halte ihn kurz. Klare Sätze wirken besser als lange Erklärungen.

Gute Beispiele zum Abschauen liegen in diesem Ordner, etwa [rechnung-pruefen](rechnung-pruefen/SKILL.md) oder [zusammenfassen](zusammenfassen/SKILL.md).

## Grenzen

- Höchstens 12 000 Zeichen. So reist der Skill mit jeder Frage mit, auch wenn ein PC aus der Community antwortet.
- Nur Text. Nichts darin wird ausgeführt, Skripte in einer ZIP-Datei werden übergangen.
- Die [Platzordnung](https://kiplatz.at/hausordnung/) gilt auch für Skills und wird bei jedem geprüft.

Vor dem Teilen prüft der [Skill-Prüfer](../werkzeuge/skill-pruefer/) Name, Länge und Aufbau.

## Ausprobieren

Im Programm unter „Skills“ auf „Neuen Skill schreiben“ klicken oder eine fertige Datei mit „Importieren (ZIP oder SKILL.md)“ hereinholen. Neben dem Eingabefeld steht „Skill: keiner“, dort wählst du ihn für ein Gespräch aus. Passt das Ergebnis nicht, änderst du eine Anweisung und fragst noch einmal. Die ganze Anleitung mit allen Knöpfen steht im [Wiki unter Skills anlegen](https://kiplatz.at/wiki/skills/).

## Mit der Community teilen

1. Stell deinen Skill im [Platzl](https://forum.kiplatz.at/) in die Kategorie Skills. Andere probieren ihn aus und machen ihn mit dir besser.
2. Für alle reichst du ihn in der [Werkstatt](https://werkstatt.kiplatz.at/KIplatz/mitbauen) ein, mit angehängter Datei oder als Änderungsvorschlag. Nach der Prüfung kommt er in jedes Programm.
3. Wer etwas beiträgt, steht auf Wunsch mit Namen auf [Wer mitbaut](https://kiplatz.at/wer-mitbaut/).

Die Skills in diesem Repository stehen unter [CC BY 4.0](../LICENSE). Kommt deiner hierher, dann nur mit deinem Einverständnis, unter derselben Lizenz und mit deinem Namen, wenn du das willst.

---

**In English:** A skill is a folder with one `SKILL.md` file in the open skills format: a name, a one-line description, then plain instructions. Copy the template above, keep it under 12 000 characters, try it in the program under “Skills”, and share it in the [Platzl](https://forum.kiplatz.at/) or the [Werkstatt](https://werkstatt.kiplatz.at/KIplatz/mitbauen).
