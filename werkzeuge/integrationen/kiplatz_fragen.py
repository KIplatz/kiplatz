"""KIplatz aus der Eingabeaufforderung fragen, über die Schnittstelle am eigenen PC.

Aufruf:
    set KIPLATZ_SCHLUESSEL=cai-DEIN-SCHLUESSEL
    python kiplatz_fragen.py "Wie viel ist 3 mal 9,90 Euro?"
    echo Fass diesen Text zusammen: ... | python kiplatz_fragen.py

Den Schlüssel findest du im Programm unter „Einstellungen“, Karte „Andere Programme dürfen KIplatz fragen“. Statt der Umgebungsvariable
geht auch --schluessel cai-DEIN-SCHLUESSEL. Die Antwort kommt Wort für Wort, so wie im Fenster. Nur Python ab 3.9, keine weiteren
Pakete. Lizenz: MIT (siehe LICENSE-CODE).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

ADRESSE = "http://127.0.0.1:8470/v1"
MODELL = "unser-modell"


def fragen(frage: str, schluessel: str, *, adresse: str = ADRESSE, ausgabe=sys.stdout, timeout: float = 300) -> str:
    """Schickt eine Frage, schreibt die Antwort laufend in `ausgabe` und gibt sie ganz zurück."""
    daten = json.dumps({"model": MODELL, "stream": True, "messages": [{"role": "user", "content": frage}]}).encode("utf-8")
    anfrage = urllib.request.Request(adresse.rstrip("/") + "/chat/completions", data=daten, method="POST",
                                     headers={"Authorization": f"Bearer {schluessel}", "Content-Type": "application/json"})
    teile: list[str] = []
    with urllib.request.urlopen(anfrage, timeout=timeout) as antwort:
        for zeile in antwort:
            zeile = zeile.decode("utf-8").strip()
            if not zeile.startswith("data:"):
                continue
            inhalt = zeile[5:].strip()
            if inhalt == "[DONE]":
                break
            try:
                stueck = json.loads(inhalt)["choices"][0].get("delta", {}).get("content") or ""
            except (ValueError, KeyError, IndexError, TypeError):
                continue
            teile.append(stueck)
            ausgabe.write(stueck)
            ausgabe.flush()
    ausgabe.write("\n")
    return "".join(teile)


def _fehlertext(exc: urllib.error.HTTPError) -> str:
    try:
        return json.loads(exc.read().decode("utf-8"))["error"]["message"]
    except (ValueError, KeyError, TypeError, OSError):
        return f"Fehler {exc.code}"


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="KIplatz aus der Eingabeaufforderung fragen.")
    p.add_argument("frage", nargs="*", help="die Frage; ohne Frage wird gelesen, was hereingereicht wird")
    p.add_argument("--schluessel", default=os.environ.get("KIPLATZ_SCHLUESSEL", ""), help="Schlüssel aus dem Programm (sonst KIPLATZ_SCHLUESSEL)")
    p.add_argument("--adresse", default=ADRESSE, help=argparse.SUPPRESS)
    a = p.parse_args(argv)
    frage = " ".join(a.frage).strip() or (sys.stdin.read().strip() if not sys.stdin.isatty() else "")
    if not frage:
        p.print_usage()
        return 2
    if not a.schluessel:
        print("Kein Schlüssel. Im Programm unter „Einstellungen“, Karte „Andere Programme dürfen KIplatz fragen“, auf „Schlüssel kopieren“ klicken.")
        return 2
    try:
        fragen(frage, a.schluessel, adresse=a.adresse)
    except urllib.error.HTTPError as exc:
        print(f"KIplatz sagt: {_fehlertext(exc)}")
        return 1
    except (urllib.error.URLError, OSError):
        print("KIplatz ist nicht erreichbar. Läuft das Programm, und ist „Programme auf diesem Gerät dürfen KIplatz fragen“ eingeschaltet?")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
