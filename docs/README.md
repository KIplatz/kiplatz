# KIplatz für Entwickler

Neu bei KIplatz? Die [ersten Schritte](hilfe.md) zeigen den Weg vom Herunterladen bis zur ersten Frage.

KIplatz hat eine Schnittstelle am eigenen PC, im Format von OpenAI. Deine Werkzeuge und Skripte fragen damit dieselbe KI wie das Programmfenster, mit demselben Wissen und derselben Platzordnung.

## Die Schnittstelle

| Punkt | Wert |
|---|---|
| Adresse | `http://127.0.0.1:8470/v1`, nur dieser PC |
| Schlüssel | beginnt mit `cai-`, geschickt als `Authorization: Bearer` |
| Endpunkte | `GET /v1/models` und `POST /v1/chat/completions` mit `messages`, `stream`, `max_tokens` |
| Modellname | `unser-modell` |
| Grenzen | 40 Nachrichten, 60 000 Zeichen, 256 kB je Anfrage, höchstens 1 500 Wortstücke als Antwort, keine Bilder |
| Wer antwortet | immer der eigene PC oder der gekoppelte im Heimnetz, nie die Community |

Aus dem Netz ist die Schnittstelle nicht erreichbar. Eine Frage kostet so viele Credits wie eine Frage im Fenster. Als Gespräch gespeichert wird nichts.

## Einschalten

1. Im Programm „Einstellungen“ öffnen, Karte „Andere Programme dürfen KIplatz fragen“.
2. „Programme auf diesem Gerät dürfen KIplatz fragen“ einschalten.
3. „Schlüssel kopieren“ und im eigenen Werkzeug mit der Adresse oben eintragen.

„Neuen Schlüssel machen“ macht den alten sofort ungültig.

## Beispiele

Ersetze `cai-DEIN-SCHLUESSEL` durch deinen eigenen Schlüssel.

**Eingabeaufforderung, eine Zeile**

```
curl.exe http://127.0.0.1:8470/v1/chat/completions -H "Authorization: Bearer cai-DEIN-SCHLUESSEL" -H "Content-Type: application/json" -d "{\"model\": \"unser-modell\", \"messages\": [{\"role\": \"user\", \"content\": \"Wie viel ist 3 mal 9,90 Euro?\"}]}"
```

**Python**

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8470/v1", api_key="cai-DEIN-SCHLUESSEL")
antwort = client.chat.completions.create(
    model="unser-modell",
    messages=[{"role": "user", "content": "Fasse diesen Text in 3 Sätzen zusammen: ..."}],
)
print(antwort.choices[0].message.content)
```

**JavaScript**

```js
const r = await fetch("http://127.0.0.1:8470/v1/chat/completions", {
  method: "POST",
  headers: { "Authorization": "Bearer cai-DEIN-SCHLUESSEL", "Content-Type": "application/json" },
  body: JSON.stringify({ model: "unser-modell", messages: [{ role: "user", content: "Was gehört auf eine Honorarnote?" }] }),
});
console.log((await r.json()).choices[0].message.content);
```

Mit `"stream": true` kommen die Wörter einzeln als Server-Sent Events.

## Die Spielwiese

Mit `--spielwiese` gestartet, benutzt das Programm einen eigenen Datenordner und den Übungsserver, nie die echte Community. Alles dort sind Wegwerfdaten.

Mehr im [Wiki, Kapitel „Für Entwickler“](https://kiplatz.at/wiki/fuer-entwickler/).

Die Code-Beispiele auf dieser Seite stehen unter der [MIT-Lizenz](../LICENSE-CODE), der Text unter [CC BY 4.0](../LICENSE).
