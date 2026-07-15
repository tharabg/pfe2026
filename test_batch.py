"""
Test batch rapide du pipeline V4 — sans frontend.
Usage:
    python test_batch.py                        # teste data/test_images/
    python test_batch.py chemin/vers/dossier    # teste un dossier spécifique
    python test_batch.py image.png              # teste un seul fichier
"""
import sys
import time
import json
import requests
from pathlib import Path

API   = "http://localhost:8000"
USER  = "agent01"
PASS  = "Agent2026"

EXTS  = {".png", ".jpg", ".jpeg", ".pdf", ".tiff", ".bmp"}

# ── couleurs terminal ──────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


def login() -> str:
    r = requests.post(
        f"{API}/api/v2/auth/login",
        data={"username": USER, "password": PASS},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def test_one(token: str, path: Path) -> dict:
    t0 = time.time()
    with open(path, "rb") as f:
        r = requests.post(
            f"{API}/api/v4/process",
            files={"file": (path.name, f, "image/png")},
            data={"transliterate_arabic": "false", "target_lang": "fr"},
            headers={"Authorization": f"Bearer {token}"},
            timeout=300,
        )
    elapsed = round(time.time() - t0, 1)
    try:
        data = r.json()
    except Exception:
        return {"file": path.name, "error": r.text[:100], "time": elapsed}

    clf   = data.get("step2_classification") or {}
    fraud = data.get("step1_fraud") or {}
    return {
        "file":    path.name,
        "action":  data.get("action", "?"),
        "type":    clf.get("doc_type", "N/A"),
        "conf":    clf.get("confidence", 0),
        "fraud":   fraud.get("score", 0),
        "ela":     fraud.get("ela_score", 0),
        "risk":    (fraud.get("vlm_check") or {}).get("risk_level", "?"),
        "reason":  data.get("reason", ""),
        "time":    elapsed,
        "error":   data.get("detail", ""),
    }


def color_action(action: str) -> str:
    if action == "ACCEPTED":
        return f"{GREEN}{BOLD}ACCEPTÉ {RESET}"
    if action == "REJECTED":
        return f"{RED}{BOLD}REJETÉ  {RESET}"
    return f"{YELLOW}{action:<8}{RESET}"


def color_risk(risk: str) -> str:
    m = {"LOW": GREEN, "MEDIUM": YELLOW, "HIGH": RED}
    return f"{m.get(risk, '')}{risk:<6}{RESET}"


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/test_images")

    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = sorted(f for f in target.iterdir() if f.suffix.lower() in EXTS)
    else:
        print(f"{RED}Chemin introuvable: {target}{RESET}")
        sys.exit(1)

    if not files:
        print(f"{YELLOW}Aucun fichier image trouvé dans {target}{RESET}")
        sys.exit(0)

    print(f"\n{BOLD}{CYAN}=== TOPNET OCR — Test Batch ({len(files)} fichier(s)) ==={RESET}\n")

    try:
        token = login()
        print(f"{GREEN}✓ Connecté en tant que {USER}{RESET}\n")
    except Exception as e:
        print(f"{RED}✗ Login échoué: {e}{RESET}")
        sys.exit(1)

    header = (
        f"{'Fichier':<40} {'Décision':<10} {'Type':<12} "
        f"{'Conf':>5} {'Fraude':>7} {'ELA':>5} {'Risque':<8} "
        f"{'Temps':>7}  Raison"
    )
    sep = "─" * 120
    print(header)
    print(sep)

    results = []
    for path in files:
        print(f"  ⟳  {path.name:<37}", end="", flush=True)
        res = test_one(token, path)
        results.append(res)

        if res.get("error"):
            print(f"\r{RED}✗  {path.name:<37} ERREUR: {res['error']}{RESET}")
            continue

        line = (
            f"\r{res['file']:<40} "
            f"{color_action(res['action']):<10} "
            f"{res['type']:<12} "
            f"{res['conf']*100:>4.0f}% "
            f"{res['fraud']*100:>6.0f}% "
            f"{res['ela']*100:>4.0f}% "
            f"{color_risk(res['risk']):<8} "
            f"{res['time']:>6.1f}s  "
            f"{res['reason']}"
        )
        print(line)

    print(sep)

    # ── Résumé ──
    ok  = sum(1 for r in results if r.get("action") == "ACCEPTED")
    ko  = sum(1 for r in results if r.get("action") == "REJECTED")
    err = sum(1 for r in results if r.get("error"))
    avg = round(sum(r.get("time", 0) for r in results) / len(results), 1) if results else 0

    print(
        f"\n{BOLD}Résumé:{RESET}  "
        f"{GREEN}Acceptés: {ok}{RESET}  "
        f"{RED}Rejetés: {ko}{RESET}  "
        f"{YELLOW}Erreurs: {err}{RESET}  "
        f"|  Temps moyen: {avg}s/doc\n"
    )

    # ── Sauvegarde JSON optionnelle ──
    out = Path("test_results.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Résultats sauvegardés → {out}\n")


if __name__ == "__main__":
    main()
