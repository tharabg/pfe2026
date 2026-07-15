# 📝 Changelog

Tous les changements importants du projet **TopNet OCR** sont documentés ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) et le versioning suit [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-04-24

### ✨ Ajouts (Features)
- ✅ Classification automatique de documents (CIN, Factures, Contrats)
  - Modèle EfficientNet-B0 avec transfer learning
  - Précision 96% sur dataset test
  - Fine-tuning à 2 phases
  - Visualisation Grad-CAM

- ✅ Extraction de texte multilingue (OCR)
  - Support PaddleOCR (default), EasyOCR, Tesseract
  - Langues: Anglais, Arabe, Français + autres
  - Détection automatique d'orientation
  - Confiance 92% moyenne

- ✅ Traduction & Translittération
  - Arabic → Latin transliteration
  - Multi-language translation support
  - Field-level translation

- ✅ Pipeline ETL complète
  - Validation des champs
  - Stockage structuré PostgreSQL
  - Logs d'audit complets

- ✅ Dashboard interactif (Streamlit)
  - Upload de documents
  - Visualisation des résultats
  - Métriques en temps réel

- ✅ API REST (FastAPI)
  - Documentation Swagger auto
  - Async endpoints
  - Validation Pydantic

- ✅ MLOps
  - Tracking MLflow
  - Versioning DVC
  - Monitoring des modèles

### 🔧 Modifications (Changed)
- Architecture microservices complète
- Docker Compose pour orchestration
- Structure modulaire du code
- Configuration centralisée

### 🐛 Corrections (Fixed)
- Incompatibilité modèle/API (Q4)
  - Assurance cohérence architecture train/inférence
  - Gestion correcte du poids des modèles

### 📚 Documentation
- ✅ README.md complet
- ✅ INSTALLATION.md (Docker + Local)
- ✅ ARCHITECTURE.md (design détaillé)
- ✅ CONTRIBUTING.md (guide contribution)
- ✅ CHANGELOG.md (ce fichier)
- ✅ CODE_OF_CONDUCT.md

---

## [0.4.0] - 2026-03-29 (Q4)

### ✨ Ajouts
- Entraînement classificateur EfficientNet
- Grad-CAM visualization
- Courbes d'entraînement (loss, accuracy)

### 🔧 Modifications
- Fine-tuning à 2 phases
- Métriques de confusion matrix

### 🐛 Corrections
- Résolution problème sauvegarde modèle (format incompatible)

---

## [0.3.0] - 2026-03-15 (Q3)

### ✨ Ajouts
- Module OCR intégration
- Pipeline API REST

### 🔧 Modifications
- Architecture preprocessing améliorée

---

## [0.2.0] - 2026-03-01 (Q2)

### ✨ Ajouts
- Module de classification basique
- Premiers tests du dataset synthétique

---

## [0.1.0] - 2026-02-15 (Q1)

### ✨ Ajouts
- Setup initial du projet
- Structure de base
- Configuration et dépendances

---

## 🔮 Roadmap (Futur)

### Phase 2 (Q5-Q6)
- [ ] Amélioration modèle classification (98% accuracy)
- [ ] Support PDF multipage
- [ ] Batch processing
- [ ] UI améliorée

### Phase 3 (Q7-Q8)
- [ ] Déploiement Kubernetes
- [ ] API authentication
- [ ] Rate limiting

### Phase 4 (Q9-Q12)
- [ ] Fine-tuning OCR spécifique domaine
- [ ] Custom models training
- [ ] Mobile app (optionnel)
- [ ] Production deployment

---

## 📋 Comment mettre à jour ce CHANGELOG

Lors de chaque release, ajouter une section:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### ✨ Ajouts
- Nouvelles features

### 🔧 Modifications
- Changements importants

### 🐛 Corrections
- Bugs fixés

### ⚠️ Breaking Changes
- Changements incompatibles avec versions précédentes

### 📚 Documentation
- Docs ajoutées/modifiées

### ⬇️ Dépendances
- Dépendances ajoutées/mises à jour/supprimées
```

---

**Version courante:** 1.0.0  
**Dernière mise à jour:** 2026-04-24  
**Maintenu par:** Ben Ghorbel Thara & TOPNET Team
