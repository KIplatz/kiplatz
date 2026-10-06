"""Skill-Prüfer für KIplatz: prüft eine SKILL.md, bevor du sie teilst.

Aufruf:
    python skill_pruefen.py mein-skill/SKILL.md
    python skill_pruefen.py skills/            (alle Ordner mit einer SKILL.md darin)

Geprüft wird, was das Programm beim Übernehmen verlangt: ein Name, genug Anweisungen, die Länge. Dazu ein paar Tipps für gute Skills.
Die Platzordnung prüft das Programm selbst, sobald du den Skill übernimmst; das macht dieses Werkzeug nicht.
Nur Python ab 3.9, keine weiteren Pakete. Lizenz: MIT (siehe LICENSE-CODE).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HOECHSTENS_ZEICHEN = 20_000        # mehr nimmt das Programm nicht an
MIT_FRAGE_ZEICHEN = 12_000         # so viel reist mit einer Frage mit, wenn ein PC der Community antwortet
NAME_HOECHSTENS = 64
BESCHREIBUNG_HOECHSTENS = 200
ANWEISUNG_MINDESTENS = 20


def name_als_ordner(name: str) -> str:
    """„Rechnung prüfen“ → „rechnung-pruefen“, so wie das Programm den Ordner nennt."""
    n = (name or "").lower().strip()
    for alt, neu in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        n = n.replace(alt, neu)
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")[:NAME_HOECHSTENS]


def zerlegen(text: str) -> tuple[dict, str]:
    """Kopf (name, description) und Anweisungen. Der Kopf zwischen zwei Zeilen „---“ ist freiwillig."""
    kopf: dict = {}
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return kopf, text
    for zeile in m.group(1).split("\n"):
        schluessel, _, wert = zeile.partition(":")
        schluessel = schluessel.strip().lower()
        if schluessel in ("name", "description"):
            kopf[schluessel] = wert.strip().strip("\"'")
    return kopf, m.group(2)


def pruefen(text: str) -> dict:
    """{"fehler": [...], "hinweise": [...], "name": ...} für den Text einer SKILL.md."""
    fehler: list[str] = []
    hinweise: list[str] = []
    text = (text or "").replace("\r\n", "\n")
    if len(text) > HOECHSTENS_ZEICHEN:
        fehler.append(f"Zu lang: {len(text)} Zeichen, das Programm nimmt höchstens {HOECHSTENS_ZEICHEN} an.")
    elif len(text) > MIT_FRAGE_ZEICHEN:
        fehler.append(f"{len(text)} Zeichen: Mit einer Frage an die Community reisen höchstens {MIT_FRAGE_ZEICHEN} mit. Bitte kürzer machen.")
    kopf, anweisungen = zerlegen(text)
    if not kopf:
        hinweise.append("Kein Kopf mit „name:“ und „description:“. Das Programm nimmt dann die erste Überschrift als Namen; mit Kopf ist es klarer.")
    name = kopf.get("name", "")
    if not name:
        h = re.search(r"^#\s+(.+)$", anweisungen, re.M)
        name = h.group(1).strip() if h else ""
    ordner = name_als_ordner(name)
    if not ordner:
        fehler.append("Kein Name: Trag oben „name: mein-skill“ ein.")
    elif ordner != name:
        hinweise.append(f"Der Name wird zu „{ordner}“ (Kleinbuchstaben, Ziffern, Bindestriche). Schreib ihn am besten gleich so.")
    beschreibung = kopf.get("description", "")
    if not beschreibung:
        hinweise.append("Keine Beschreibung: Ein Satz bei „description:“ hilft beim Aussuchen. Sonst nimmt das Programm die erste Zeile.")
    elif len(beschreibung) > BESCHREIBUNG_HOECHSTENS:
        hinweise.append(f"Die Beschreibung hat {len(beschreibung)} Zeichen; angezeigt werden {BESCHREIBUNG_HOECHSTENS}. Ein Satz genügt.")
    rumpf = anweisungen.strip()
    if len(rumpf) < ANWEISUNG_MINDESTENS:
        fehler.append("Fast keine Anweisungen: Schreib darunter, wie KIplatz vorgehen soll.")
    elif not re.search(r"(?i)erfind|nicht raten|frag(e|t)? nach", rumpf):
        hinweise.append("Tipp: Ein Satz wie „Erfinde nichts dazu, frag nach, wenn etwas fehlt“ macht die Antworten verlässlicher.")
    if re.search(r"(?i)<script|```(?:python|bash|powershell|js)", rumpf):
        hinweise.append("Code in einem Skill wird nie ausgeführt; ein Skill ist nur Text.")
    return {"fehler": fehler, "hinweise": hinweise, "name": ordner}


def dateien(ziel: Path) -> list[Path]:
    if ziel.is_dir():
        direkt = ziel / "SKILL.md"
        return [direkt] if direkt.is_file() else sorted(ziel.glob("*/SKILL.md"))
    return [ziel]


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 2
    ziele = dateien(Path(argv[0]))
    if not ziele:
        print("Keine SKILL.md gefunden.")
        return 1
    schlecht = 0
    for datei in ziele:
        try:
            text = datei.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"✗ {datei}: nicht lesbar ({type(exc).__name__})")
            schlecht += 1
            continue
        r = pruefen(text)
        zeichen = "✗" if r["fehler"] else "✓"
        print(f"{zeichen} {datei}" + (f"  ({r['name']})" if r["name"] else ""))
        for f in r["fehler"]:
            print(f"    Fehler: {f}")
        for h in r["hinweise"]:
            print(f"    Hinweis: {h}")
        schlecht += bool(r["fehler"])
    if len(ziele) > 1:
        print(f"\n{len(ziele) - schlecht} von {len(ziele)} in Ordnung.")
    return 1 if schlecht else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
