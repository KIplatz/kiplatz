# Skill-Prüfer

Prüft eine `SKILL.md`, bevor du sie im Platzl zeigst oder in der Werkstatt einreichst.

```
python skill_pruefen.py mein-skill/SKILL.md
python skill_pruefen.py ../../skills/
```

Mit einem Ordner prüft er jede `SKILL.md` darin. Am Ende steht, wie viele in Ordnung sind.

## Was geprüft wird

| Punkt | Fehler oder Hinweis |
|---|---|
| Name fehlt | Fehler |
| Fast keine Anweisungen (unter 20 Zeichen) | Fehler |
| Mehr als 12 000 Zeichen, so viel reist mit einer Frage an die Community mit | Fehler |
| Name nicht in Kleinbuchstaben mit Bindestrichen | Hinweis, mit dem Namen, den das Programm daraus macht |
| Keine oder zu lange Beschreibung | Hinweis |
| Kein Satz wie „Erfinde nichts dazu“ | Tipp |

Die Platzordnung prüft das Programm selbst, sobald du den Skill übernimmst. Wie ein guter Skill aussieht, steht in [Einen Skill schreiben](../../skills/SKILL-SCHREIBEN.md).

Der Prüfer ist eine einzelne Python-Datei ohne weitere Pakete. Rückgabewert 0 heißt alles in Ordnung, 1 heißt mindestens ein Fehler; so lässt er sich auch in eigene Abläufe einbauen.
