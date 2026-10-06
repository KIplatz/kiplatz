# KIplatz in anderen Programmen

KIplatz hat am eigenen PC eine Schnittstelle im Format von OpenAI. Viele Programme, die OpenAI ansprechen, sprechen damit auch KIplatz an: Adresse und Schlüssel eintragen, Modellname übernehmen, fertig. Die Antworten kommen vom eigenen PC oder vom gekoppelten im Heimnetz, mit demselben Wissen und derselben Platzordnung wie im Fenster.

## Vorher einmal einschalten

1. Im Programm „Einstellungen“ öffnen, Karte „Andere Programme dürfen KIplatz fragen“.
2. „Programme auf diesem Gerät dürfen KIplatz fragen“ einschalten.
3. „Schlüssel kopieren“. Klappt das nicht, den Schlüssel mit einem Doppelklick markieren und mit Strg + C kopieren.

| Was | Wert |
|---|---|
| Adresse (Base URL) | `http://127.0.0.1:8470/v1` |
| Schlüssel (API Key) | dein Schlüssel, beginnt mit `cai-` |
| Modell | `unser-modell` |

Die Schnittstelle nimmt nur Anfragen von diesem PC an, mit der Adresse `127.0.0.1` oder `localhost`. Ein anderes Gerät, auch eines im eigenen Heimnetz, kommt nicht hin, das ist Absicht. Programme in Docker Desktop am selben PC dürfen fragen, wenn du es erlaubst. Wie das geht, steht unten bei Open WebUI. Eine Frage kostet so viele Credits wie eine Frage im Fenster.

## Continue (Programmierhilfe für VS Code und JetBrains)

In der Datei `config.yaml` von Continue ein Modell dazuschreiben:

```yaml
name: Meine Einstellungen
version: 0.0.1
schema: v1

models:
  - name: KIplatz
    provider: openai
    model: unser-modell
    apiBase: http://127.0.0.1:8470/v1
    apiKey: cai-DEIN-SCHLUESSEL
```

## Open WebUI

Läuft Open WebUI direkt auf dem PC: ⚙️ **Admin Settings** → **Connections** → **OpenAI** → ➕ **Add Connection**, bei **URL** `http://127.0.0.1:8470/v1` und bei **API Key** deinen Schlüssel eintragen. Danach steht `unser-modell` in der Liste der Modelle.

Die meisten starten Open WebUI in Docker. Das geht auch, mit Docker Desktop auf demselben PC:

1. In KIplatz unter „Einstellungen“, Karte „Andere Programme dürfen KIplatz fragen“, zusätzlich „Auch Programme in Docker auf diesem PC dürfen fragen“ einschalten. Der Schalter ist aus, bis du ihn einschaltest.
2. Open WebUI so starten, wie es seine Anleitung vorschlägt, und KIplatz gleich mitgeben:

```
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data -e OPENAI_API_BASE_URL=http://host.docker.internal:8470/v1 -e OPENAI_API_KEY=cai-DEIN-SCHLUESSEL -e ENABLE_TITLE_GENERATION=False -e ENABLE_FOLLOW_UP_GENERATION=False -e ENABLE_TAGS_GENERATION=False --name open-webui ghcr.io/open-webui/open-webui:main
```

Die Adresse heißt hier `http://host.docker.internal:8470/v1`, nicht `127.0.0.1`, weil `127.0.0.1` im Behälter den Behälter selbst meint. Läuft Open WebUI schon, trägst du dieselbe Adresse und den Schlüssel unter **Connections** ein.

Die letzten 3 Angaben schalten Titel, Folgefragen und Schlagworte ab. Sonst schickt Open WebUI zu jeder Frage 3 weitere Aufträge, und jeder kostet Credits wie eine Frage. Abschalten geht auch später unter **Admin Settings** → **Interface**.

Geräte aus dem Heimnetz kommen auch mit diesem Schalter nicht hinein, der Schlüssel bleibt Pflicht. Ist der Schalter aus, antwortet KIplatz in Open WebUI mit dem Namen des Schalters, der fehlt. Geprüft haben wir das mit Docker Desktop unter Windows 11. Docker ohne Docker Desktop, etwa direkt in WSL, haben wir nicht ausprobiert.

## Jan

**Settings** → **Model Providers** → **Add Provider**, als Format „OpenAI-compatible“ wählen, bei **Base URL** `http://127.0.0.1:8470/v1` und den Schlüssel eintragen.

## Eingabeaufforderung

Mit dem kleinen Skript `kiplatz_fragen.py` in diesem Ordner (nur Python, keine weiteren Pakete):

```
set KIPLATZ_SCHLUESSEL=cai-DEIN-SCHLUESSEL
python kiplatz_fragen.py "Wie viel ist 3 mal 9,90 Euro?"
```

Weitere Beispiele mit curl, Python und JavaScript stehen in der [Anleitung zur Schnittstelle](../../docs/README.md).

## Deine Anbindung fehlt?

Hast du KIplatz an ein Programm angebunden, das hier fehlt, etwa Home Assistant, Obsidian oder dein eigenes Werkzeug? Erzähl es im [Platzl](https://forum.kiplatz.at/) oder schick die Anleitung in die [Werkstatt](https://werkstatt.kiplatz.at/KIplatz/mitbauen). Gute Anleitungen kommen mit deinem Einverständnis hierher, auf Wunsch mit deinem Namen.

Die Menünamen der fremden Programme stammen aus deren Anleitungen (Stand Oktober 2026) und können sich mit neuen Versionen ändern.
