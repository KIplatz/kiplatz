"""Hardware-Check für KIplatz: Was schafft mein PC?

Aufruf:
    python hardware_check.py          Ergebnis in Sätzen
    python hardware_check.py --json   dasselbe als JSON, etwa für eigene Auswertungen

Liest nur: Arbeitsspeicher, Prozessorkerne, Grafikkarte und ihren Speicher. Ändert nichts, braucht keine Administratorrechte,
schickt nichts ins Internet und zeigt weder Rechnernamen noch Seriennummern. Die Regel, welches Modell passt, ist dieselbe wie im
Programm: das größte Modell, das ganz in den Grafikspeicher passt (Kartengröße minus eine kleine Reserve für Bildschirm und andere
Programme); ohne passende Karte entscheidet der Arbeitsspeicher. Was gerade belegt ist, zeigt der Check nur zur Information.
Nur Python ab 3.9, keine weiteren Pakete. Lizenz: MIT (siehe LICENSE-CODE).
"""
from __future__ import annotations

import ctypes
import json
import os
import platform
import re
import shutil
import subprocess
import sys

# was ein Modell an Grafikspeicher braucht (Datei plus Arbeitsbereich), stärkstes zuerst; dazu die Reserve für Bildschirm und Programme
MODELLE = (("14B", "große Modell", 9000), ("8B", "mittlere Modell", 5900), ("3B", "kleine Modell", 2800))
RESERVE_MIB = 300
RAM_FUER_8B_GIB = 15.5
EINGEBAUT = re.compile(r"(?i)\bintel\b|uhd|iris|vega|radeon\(tm\) graphics|radeon graphics|microsoft basic")
TIMEOUT_S = 8


def _ausfuehren(befehl: list[str]) -> str:
    try:
        r = subprocess.run(befehl, capture_output=True, text=True, timeout=TIMEOUT_S,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return r.stdout if r.returncode == 0 else ""


def arbeitsspeicher_gib() -> float | None:
    if sys.platform == "win32":
        class _Stand(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong), ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        s = _Stand()
        s.dwLength = ctypes.sizeof(_Stand)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s)):
            return round(s.ullTotalPhys / 2**30, 1)
        return None
    if sys.platform.startswith("linux"):
        try:
            with open("/proc/meminfo", encoding="ascii") as f:
                m = re.search(r"MemTotal:\s+(\d+) kB", f.read())
            return round(int(m.group(1)) / 2**20, 1) if m else None
        except OSError:
            return None
    if sys.platform == "darwin":
        roh = _ausfuehren(["sysctl", "-n", "hw.memsize"]).strip()
        return round(int(roh) / 2**30, 1) if roh.isdigit() else None
    return None


def _nvidia() -> list[dict]:
    """Karten von NVIDIA über das Werkzeug, das mit dem Treiber kommt: Name, Speicher gesamt und frei (MiB)."""
    if not shutil.which("nvidia-smi"):
        return []
    karten = []
    for zeile in _ausfuehren(["nvidia-smi", "--query-gpu=name,memory.total,memory.free", "--format=csv,noheader,nounits"]).splitlines():
        teile = [t.strip() for t in zeile.split(",")]
        if len(teile) == 3 and teile[1].isdigit() and teile[2].isdigit():
            karten.append({"name": teile[0], "gesamt_mib": int(teile[1]), "frei_mib": int(teile[2]), "frei_gemessen": True})
    return karten


def _windows_karten() -> list[dict]:
    """Alle Karten unter Windows aus den Angaben des Treibers (liest nur). Der Speicher steht dort als 64-Bit-Zahl; die bekannte
    WMI-Angabe AdapterRAM bricht bei 4 GB ab und taugt darum nicht."""
    skript = ("$k='HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0*';"
              "Get-ItemProperty $k -ErrorAction SilentlyContinue | ForEach-Object { [pscustomobject]@{ name=$_.DriverDesc;"
              " q=$_.'HardwareInformation.qwMemorySize'; m=$_.'HardwareInformation.MemorySize' } } | ConvertTo-Json -Compress")
    roh = _ausfuehren(["powershell", "-NoProfile", "-NonInteractive", "-Command", skript]).strip()
    try:
        daten = json.loads(roh) if roh else []
    except ValueError:
        return []
    karten = []
    for e in daten if isinstance(daten, list) else [daten]:
        if not isinstance(e, dict) or not e.get("name"):
            continue
        groesse = e.get("q") or e.get("m")
        if isinstance(groesse, list):   # manche Treiber legen die Zahl als Bytefolge ab
            groesse = int.from_bytes(bytes(groesse), "little") if all(isinstance(b, int) for b in groesse) else None
        mib = int(groesse) // 2**20 if isinstance(groesse, (int, float)) and groesse > 0 else 0
        karten.append({"name": str(e["name"]), "gesamt_mib": mib, "frei_mib": None, "frei_gemessen": False})
    return karten


def grafikkarten() -> list[dict]:
    karten = _nvidia()
    if sys.platform == "win32":
        namen = {k["name"] for k in karten}
        karten += [k for k in _windows_karten() if k["name"] not in namen]
    for k in karten:
        k["eingebaut"] = bool(EINGEBAUT.search(k["name"]))
    return karten


def empfehlung(karten: list[dict], ram_gib: float | None) -> dict:
    """Dieselbe Regel wie im Programm: stärkste eigene Karte zuerst, größtes Modell, das in den Speicher der Karte passt."""
    reihe = sorted(karten, key=lambda k: (not k["eingebaut"], k["gesamt_mib"]), reverse=True)
    eigene = any(not k["eingebaut"] for k in reihe)
    for k in reihe:
        if k["eingebaut"] and (eigene or (ram_gib or 0) < 8):
            continue
        platz = k["gesamt_mib"] - RESERVE_MIB
        for kennung, wort, braucht in MODELLE:
            if braucht <= platz:
                return {"modell": kennung, "wort": wort, "wo": "grafikkarte", "karte": k["name"], "platz_mib": platz}
    if (ram_gib or 0) >= RAM_FUER_8B_GIB:
        return {"modell": "8B", "wort": "mittlere Modell", "wo": "prozessor", "karte": None, "platz_mib": None}
    return {"modell": "3B", "wort": "kleine Modell", "wo": "prozessor", "karte": None, "platz_mib": None}


def bericht() -> dict:
    ram = arbeitsspeicher_gib()
    karten = grafikkarten()
    return {"system": platform.system(), "kerne": os.cpu_count(), "arbeitsspeicher_gib": ram, "grafikkarten": karten,
            "empfehlung": empfehlung(karten, ram)}


def _gb(mib: int) -> str:
    return f"{mib / 1024:.1f}".replace(".", ",") + " GB"


def in_saetzen(b: dict) -> str:
    z = ["Dein Rechner und KIplatz", ""]
    ram = b["arbeitsspeicher_gib"]
    z.append(f"Prozessor: {b['kerne'] or '?'} Kerne")
    z.append(f"Arbeitsspeicher: {str(ram).replace('.', ',')} GB" if ram else "Arbeitsspeicher: nicht lesbar")
    if not b["grafikkarten"]:
        z.append("Grafikkarte: keine gefunden")
    for k in b["grafikkarten"]:
        art = "eingebaut" if k["eingebaut"] else "eigene Karte"
        speicher = _gb(k["gesamt_mib"]) if k["gesamt_mib"] else "Speicher nicht lesbar"
        frei = f", gerade frei {_gb(k['frei_mib'])}" if k["frei_gemessen"] and k["gesamt_mib"] else ""
        z.append(f"Grafikkarte: {k['name']} ({art}), {speicher}{frei}")
    e = b["empfehlung"]
    z.append("")
    if e["wo"] == "grafikkarte":
        z.append(f"Passt: das {e['wort']} ({e['modell']}), ganz auf der Grafikkarte. Damit kann dein PC auch für die Community arbeiten.")
    else:
        z.append(f"Passt: das {e['wort']} ({e['modell']}) auf dem Prozessor. Das geht, ist aber langsamer als mit einer passenden Grafikkarte.")
    if b["system"] != "Windows":
        z.append("Das Programm gibt es derzeit für Windows. Am Handy und im Browser geht KIplatz unter kiplatz.at/app.")
    z.append("Mitmachen: https://kiplatz.at/rechenkraft-teilen/")
    return "\n".join(z)


def main(argv: list[str]) -> int:
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    b = bericht()
    print(json.dumps(b, ensure_ascii=False, indent=2) if "--json" in argv else in_saetzen(b))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
