"""
=============================================================================
TOPNET OCR — Évaluation Académique du Pipeline V3
=============================================================================
Auteur  : Ben Ghorbel Thara
Projet  : PFE TOPNET — Système Intelligent d'OCR et Détection de Fraude

Métriques produites :
  - Accuracy globale de classification
  - Precision / Recall / F1-score par type de document
  - Matrice de confusion (classification)
  - Temps de traitement moyen par étape
  - Rapport JSON exportable pour le rapport PFE

Usage :
  # Évaluation sur dataset/test (labels déduits du nom de dossier)
  python evaluate_pipeline.py

  # Dossier personnalisé
  python evaluate_pipeline.py --folder "C:/chemin/vers/dossier"

Structure attendue du dossier (labels automatiques) :
  dataset/test/
    cin/        ← tous les fichiers ici ont label "CIN"
    contrat/    ← label "CONTRAT"
    facture/    ← label "FACTURE"
    passeport/  ← label "PASSEPORT"
=============================================================================
"""

import sys, json, time, argparse, requests
from pathlib import Path
from datetime import datetime
from collections import defaultdict

GREEN  = "\033[92m"; RED   = "\033[91m"; YELLOW = "\033[93m"
CYAN   = "\033[96m"; RESET = "\033[0m";  BOLD   = "\033[1m"
BLUE   = "\033[94m"

API  = "http://localhost:8000"
USER = "agent01"
PASS = "Agent2026"
EXTS = {".png", ".jpg", ".jpeg", ".pdf", ".tiff", ".tif", ".bmp", ".webp"}

FOLDER_TO_CLASS = {
    "cin":       "CIN",
    "contrat":   "CONTRAT",
    "facture":   "FACTURE",
    "passeport": "PASSEPORT",
}


def login() -> str:
    r = requests.post(
        f"{API}/api/v2/auth/login-json",
        json={"email": USER, "password": PASS}, timeout=10
    )
    r.raise_for_status()
    return r.json()["access_token"]


def process_file(token: str, path: Path) -> dict:
    t0 = time.time()
    try:
        with open(path, "rb") as f:
            r = requests.post(
                f"{API}/api/v2/process",
                files={"file": (path.name, f)},
                data={"pipeline": "VOIE_A", "target_lang": "fr"},
                headers={"Authorization": f"Bearer {token}"},
                timeout=300,
            )
        elapsed = round(time.time() - t0, 1)
        data = r.json()
    except Exception as e:
        return {"file": path.name, "error": str(e), "time_total": round(time.time()-t0,1)}

    clf     = data.get("step2_classification") or {}
    fraud   = data.get("step3_fraud") or {}
    meta    = data.get("meta") or {}
    timings = meta.get("timings") or {}

    return {
        "file":           path.name,
        "action":         data.get("action", "UNKNOWN"),
        "predicted_type": clf.get("doc_type", "UNKNOWN"),
        "clf_conf":       clf.get("confidence", 0),
        "fraud_score":    fraud.get("score", 0),
        "fraud_rec":      fraud.get("recommendation", ""),
        "reason":         data.get("reason", ""),
        "time_total":     elapsed,
        "time_ocr":       timings.get("ocr", 0),
        "time_clf":       timings.get("classification", 0),
        "time_fraud":     timings.get("fraud", 0),
        "time_extract":   timings.get("extraction", 0),
        "error":          "",
    }


def collect_dataset(folder: Path):
    """
    Parcourt les sous-dossiers de folder.
    Déduit le label attendu depuis le nom du sous-dossier.
    Retourne une liste de (path, expected_class).
    """
    items = []
    subfolders = [d for d in sorted(folder.iterdir()) if d.is_dir()]

    if subfolders:
        for sub in subfolders:
            cls = FOLDER_TO_CLASS.get(sub.name.lower())
            if cls is None:
                print(f"{YELLOW}Dossier ignoré (nom non reconnu): {sub.name}{RESET}")
                continue
            files = [f for f in sorted(sub.iterdir()) if f.suffix.lower() in EXTS]
            for f in files:
                items.append((f, cls))
        return items
    else:
        # Dossier plat — pas de label automatique
        files = [f for f in sorted(folder.iterdir()) if f.suffix.lower() in EXTS]
        return [(f, None) for f in files]


def compute_metrics(results_with_labels):
    """
    Calcule précision, rappel, F1 et matrice de confusion.
    Justification scientifique des métriques :
      - Precision = TP/(TP+FP) : fiabilité quand le système dit "c'est X"
      - Recall    = TP/(TP+FN) : capacité à trouver tous les X
      - F1        = moyenne harmonique precision+recall : équilibre les deux
      - Confusion matrix : montre quelles classes sont confondues entre elles
    """
    labeled = [(r, lbl) for r, lbl in results_with_labels if lbl and not r.get("error")]
    if not labeled:
        return None

    doc_types = sorted(set(lbl for _, lbl in labeled))
    confusion = defaultdict(lambda: defaultdict(int))
    per_item = []

    for r, expected in labeled:
        predicted = r["predicted_type"]
        confusion[expected][predicted] += 1
        per_item.append({
            "file":           r["file"],
            "expected_type":  expected,
            "predicted_type": predicted,
            "correct":        expected == predicted,
            "clf_conf":       r["clf_conf"],
            "action":         r["action"],
        })

    type_metrics = {}
    for t in doc_types:
        tp = sum(1 for d in per_item if d["expected_type"] == t and d["predicted_type"] == t)
        fp = sum(1 for d in per_item if d["expected_type"] != t and d["predicted_type"] == t)
        fn = sum(1 for d in per_item if d["expected_type"] == t and d["predicted_type"] != t)
        tn = sum(1 for d in per_item if d["expected_type"] != t and d["predicted_type"] != t)

        prec   = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1     = 2*prec*recall / (prec+recall) if (prec+recall) > 0 else 0

        type_metrics[t] = {
            "TP": tp, "FP": fp, "FN": fn, "TN": tn,
            "precision": round(prec, 4),
            "recall":    round(recall, 4),
            "f1":        round(f1, 4),
            "support":   tp + fn,
        }

    total   = len(per_item)
    correct = sum(1 for d in per_item if d["correct"])
    accuracy = correct / total if total else 0

    # Macro-average F1 (donne le même poids à chaque classe, indépendamment de la taille)
    # C'est la métrique recommandée pour les datasets déséquilibrés
    macro_f1 = sum(m["f1"] for m in type_metrics.values()) / len(type_metrics) if type_metrics else 0

    return {
        "total":      total,
        "correct":    correct,
        "accuracy":   round(accuracy, 4),
        "macro_f1":   round(macro_f1, 4),
        "per_type":   type_metrics,
        "confusion":  {k: dict(v) for k, v in confusion.items()},
        "per_item":   per_item,
        "doc_types":  doc_types,
    }


def print_report(metrics, timings_avg, n_total, n_errors):
    print(f"\n{BOLD}{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}{CYAN}   TOPNET OCR — Rapport d'Évaluation Académique{RESET}")
    print(f"{BOLD}{CYAN}{'='*70}{RESET}")

    print(f"\n  Documents traités : {n_total}   Erreurs : {RED}{n_errors}{RESET}")
    print(f"  Documents évalués : {metrics['total']}\n")

    # Classification globale
    print(f"{BOLD}{BLUE}▌ CLASSIFICATION — RÉSULTATS GLOBAUX{RESET}")
    acc_color = GREEN if metrics["accuracy"] >= 0.85 else YELLOW if metrics["accuracy"] >= 0.70 else RED
    print(f"  Accuracy globale : {acc_color}{BOLD}{metrics['accuracy']*100:.1f}%{RESET}  "
          f"({metrics['correct']}/{metrics['total']})")
    mf1_color = GREEN if metrics["macro_f1"] >= 0.85 else YELLOW if metrics["macro_f1"] >= 0.70 else RED
    print(f"  Macro F1-score   : {mf1_color}{BOLD}{metrics['macro_f1']*100:.1f}%{RESET}")
    print(f"  (Macro F1 = moyenne non pondérée — équitable pour datasets déséquilibrés)\n")

    # Métriques par type
    print(f"{BOLD}{BLUE}▌ MÉTRIQUES PAR TYPE DE DOCUMENT{RESET}")
    header = f"  {'Type':<12} {'Support':>8} {'Precision':>10} {'Recall':>8} {'F1':>8}"
    print(header)
    print("  " + "─" * 50)
    for t, m in sorted(metrics["per_type"].items()):
        c = GREEN if m["f1"] >= 0.85 else YELLOW if m["f1"] >= 0.65 else RED
        print(f"  {t:<12} {m['support']:>8} {m['precision']*100:>9.1f}%"
              f" {m['recall']*100:>7.1f}% {c}{m['f1']*100:>7.1f}%{RESET}")

    # Matrice de confusion
    print(f"\n{BOLD}{BLUE}▌ MATRICE DE CONFUSION{RESET}")
    print(f"  (Lire : ligne = réel, colonne = prédit)")
    doc_types = metrics["doc_types"]
    confusion  = metrics["confusion"]
    _header_label = "Réel \\ Prédit"
    header_line = f"  {_header_label:<14}" + "".join(f"{t[:6]:>8}" for t in doc_types)
    print(header_line)
    print("  " + "─" * (14 + 8 * len(doc_types)))
    for expected in doc_types:
        row = confusion.get(expected, {})
        line = f"  {expected:<14}"
        for predicted in doc_types:
            val = row.get(predicted, 0)
            if expected == predicted:
                line += f"{GREEN}{val:>8}{RESET}"
            elif val > 0:
                line += f"{RED}{val:>8}{RESET}"
            else:
                line += f"{val:>8}"
        print(line)

    # Erreurs de classification
    errors = [d for d in metrics["per_item"] if not d["correct"]]
    if errors:
        print(f"\n{BOLD}{BLUE}▌ CONFUSIONS DÉTECTÉES ({len(errors)} cas){RESET}")
        for d in errors:
            print(f"  {d['file']:<45} {d['expected_type']:>10} → {RED}{d['predicted_type']}{RESET}")

    # Performances temporelles
    if timings_avg:
        print(f"\n{BOLD}{BLUE}▌ TEMPS DE TRAITEMENT MOYEN PAR ÉTAPE{RESET}")
        for step, avg in sorted(timings_avg.items(), key=lambda x: -x[1]):
            bar = "█" * min(int(avg * 4), 40)
            print(f"  {step:<18} {avg:>6.2f}s  {CYAN}{bar}{RESET}")

    print(f"\n{BOLD}{CYAN}{'='*70}{RESET}\n")


def export_confusion_matrix_image(metrics, output_path: Path):
    """Exporte la matrice de confusion en image PNG pour le rapport."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        doc_types = metrics["doc_types"]
        n = len(doc_types)
        matrix = np.zeros((n, n), dtype=int)
        confusion = metrics["confusion"]
        for i, expected in enumerate(doc_types):
            for j, predicted in enumerate(doc_types):
                matrix[i][j] = confusion.get(expected, {}).get(predicted, 0)

        fig, ax = plt.subplots(figsize=(7, 6))
        im = ax.imshow(matrix, interpolation="nearest", cmap=plt.cm.Blues)
        plt.colorbar(im)

        ax.set(
            xticks=range(n), yticks=range(n),
            xticklabels=doc_types, yticklabels=doc_types,
            title=f"Matrice de Confusion — Pipeline TOPNET OCR\nAccuracy={metrics['accuracy']*100:.1f}%  Macro-F1={metrics['macro_f1']*100:.1f}%",
            ylabel="Type réel", xlabel="Type prédit"
        )
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

        thresh = matrix.max() / 2
        for i in range(n):
            for j in range(n):
                ax.text(j, i, matrix[i][j], ha="center", va="center",
                        color="white" if matrix[i][j] > thresh else "black", fontsize=13)

        fig.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        return True
    except ImportError:
        return False


def main():
    parser = argparse.ArgumentParser(description="TOPNET OCR — Évaluation académique")
    parser.add_argument("--folder", default="dataset/test",
                        help="Dossier de test (sous-dossiers = classes)")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.exists():
        print(f"{RED}Dossier introuvable: {folder}{RESET}")
        sys.exit(1)

    items = collect_dataset(folder)
    if not items:
        print(f"{YELLOW}Aucun fichier trouvé dans {folder}{RESET}")
        sys.exit(0)

    # Compter la distribution
    from collections import Counter
    dist = Counter(lbl for _, lbl in items if lbl)
    print(f"\n{BOLD}{CYAN}=== TOPNET OCR — Évaluation ({len(items)} documents) ==={RESET}")
    print(f"Distribution : " + " | ".join(f"{k}: {v}" for k, v in sorted(dist.items())))

    # Connexion
    try:
        token = login()
        print(f"{GREEN}✓ Connecté ({USER}){RESET}\n")
    except Exception as e:
        print(f"{RED}✗ Login échoué: {e}{RESET}")
        sys.exit(1)

    # Traitement
    results_with_labels = []
    n_errors = 0
    for i, (path, expected_cls) in enumerate(items, 1):
        label_str = f"[{expected_cls}]" if expected_cls else "[?]"
        print(f"  [{i:3}/{len(items)}] ⟳  {path.name:<40} {label_str}", end="", flush=True)
        res = process_file(token, path)
        results_with_labels.append((res, expected_cls))

        if res.get("error"):
            n_errors += 1
            print(f"\r  [{i:3}/{len(items)}] {RED}✗  {path.name:<40} ERREUR: {res['error'][:40]}{RESET}")
        else:
            ok = res["predicted_type"] == expected_cls if expected_cls else True
            c  = GREEN if ok else RED
            mark = "✓" if ok else "✗"
            print(f"\r  [{i:3}/{len(items)}] {c}{mark}{RESET}  {path.name:<40} "
                  f"{label_str:<12} → {c}{res['predicted_type']:<10}{RESET} "
                  f"conf={res['clf_conf']*100:.0f}%  {res['time_total']:.1f}s")

    # Métriques
    metrics = compute_metrics(results_with_labels)
    if not metrics:
        print(f"{YELLOW}Pas assez de labels pour calculer les métriques.{RESET}")
        sys.exit(0)

    # Temps moyens
    labeled_results = [r for r, _ in results_with_labels if not r.get("error")]
    timings_avg = {}
    for step in ("time_ocr", "time_clf", "time_fraud", "time_extract", "time_total"):
        vals = [r[step] for r in labeled_results if r.get(step, 0) > 0]
        if vals:
            timings_avg[step.replace("time_", "").capitalize()] = round(sum(vals)/len(vals), 2)

    print_report(metrics, timings_avg, len(items), n_errors)

    # Export JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "date":    datetime.now().isoformat(),
        "author":  "Ben Ghorbel Thara — PFE TOPNET",
        "model":   "TOPNET OCR Pipeline V3 (TripleClassifier + PaddleOCR + BusinessFraudDetector)",
        "dataset": str(folder),
        "distribution": dict(dist),
        "n_docs":  len(items),
        "n_errors": n_errors,
        "metrics": {k: v for k, v in metrics.items() if k != "per_item"},
        "timings": timings_avg,
    }
    out_json = Path(f"evaluation_report_{timestamp}.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"{GREEN}Rapport JSON → {out_json}{RESET}")

    # Export image matrice de confusion
    out_img = Path(f"confusion_matrix_{timestamp}.png")
    if export_confusion_matrix_image(metrics, out_img):
        print(f"{GREEN}Matrice de confusion PNG → {out_img}{RESET}")
    else:
        print(f"{YELLOW}matplotlib non disponible — image non générée (pip install matplotlib){RESET}")

    print()


if __name__ == "__main__":
    main()
