# 🤝 Guide de Contribution

Merci de l'intérêt porté à **TopNet OCR**! Ce document explique comment contribuer au projet.

## 📋 Code of Conduct

Ce projet et ses participants respectent le [Code de Conduite](./CODE_OF_CONDUCT.md). En participant, vous acceptez ces conditions.

## 🚀 Comment contribuer

### 1️⃣ Signaler un bug
- Créez une **Issue GitHub** avec:
  - **Titre clair** du problème
  - **Description détaillée** avec étapes de reproduction
  - **Logs** ou **screenshots** si possible
  - **Environnement** (OS, Python, versions)

### 2️⃣ Proposer une amélioration
- Créez une **Issue** intitulée `[FEATURE]` avec:
  - Motivation et cas d'usage
  - Implémentation proposée (si possible)
  - Impact sur le projet

### 3️⃣ Soumettre du code
1. **Fork** le repository
2. **Créez une branche** (ex: `feature/ocr-improvement` ou `fix/classification-bug`)
3. **Committez vos changements** (messages clairs en français)
4. **Testez** votre code:
   ```bash
   pytest tests/ -v --cov=src
   ```
5. **Push** et créez une **Pull Request**

### PR: Checklist
- ✅ Tests passent (`pytest`)
- ✅ Code formaté (`black`)
- ✅ Linting OK (`flake8`)
- ✅ Types vérifiés (`mypy`)
- ✅ Docstrings présentes
- ✅ Changelog.md mis à jour

## 🛠️ Setup de développement

```bash
# 1. Fork & Clone
git clone https://github.com/YOUR_USERNAME/topnet-ocr.git
cd topnet-ocr

# 2. Créer environment
conda env create -f environment.yml
conda activate topnet-ocr

# 3. Installer en mode dev
pip install -e ".[dev]"

# 4. Tester
pytest tests/

# 5. Formater le code
black src/ tests/ scripts/
flake8 src/ tests/
```

## 📝 Style de code

- **Langage**: Python 3.10+
- **Formatter**: `black` (line length: 100)
- **Linter**: `flake8`
- **Type hints**: `mypy` obligatoire
- **Docstrings**: Format Google ou NumPy

Exemple:
```python
def classify_document(image_path: str, confidence_threshold: float = 0.9) -> dict:
    """
    Classifie un document comme CIN, Facture ou Contrat.
    
    Args:
        image_path: Chemin vers l'image du document
        confidence_threshold: Score minimum de confiance (0-1)
        
    Returns:
        dict avec keys:
            - 'document_type': str (CIN/Facture/Contrat)
            - 'confidence': float (0-1)
            - 'processing_time': float (secondes)
    """
    pass
```

## 🧪 Tests

Tous les changements doivent avoir des tests:
```bash
# Lancer tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=src --cov-report=html

# Tester un fichier spécifique
pytest tests/test_classification.py -v
```

## 📚 Documentation

- **Code**: Commentaires et docstrings
- **API**: FastAPI génère Swagger auto
- **Architecture**: Voir [ARCHITECTURE.md](./ARCHITECTURE.md)
- **Installation**: Voir [INSTALLATION.md](./INSTALLATION.md)

## 🔄 Processus de review

1. Un mainteneur reviewe votre PR
2. Demande de changements si nécessaire
3. Tests automatisés doivent passer
4. Merge après approbation

## ❓ Questions?

- **Issues**: Pour les bugs et features
- **Discussions**: Pour les questions générales
- **Email**: Contact via TOPNET

---

**Merci pour votre contribution!** 🎉
