# 🚀 Guide d'Installation

Guide complet pour installer et démarrer **TopNet OCR**.

## 📋 Prérequis

- **Python 3.10+**
- **Docker & Docker Compose** (recommandé) OU **Conda**
- **4GB+ RAM** (8GB+ recommandé pour ML)
- **GPU optionnel** (NVIDIA avec CUDA pour accélération)

---

## 🐳 Installation avec Docker (Recommandé)

### Avantages:
- ✅ Installation simple et rapide
- ✅ Pas de conflits de dépendances
- ✅ Identical sur tous les systèmes

### Étapes:

```bash
# 1. Cloner le repository
git clone https://github.com/TOPNET/topnet-ocr.git
cd topnet-ocr

# 2. Démarrer les services
docker-compose up -d

# Attendre 30-60 secondes le temps que tout démarre...

# 3. Vérifier le statut
docker-compose ps

# 4. Accéder aux services
# 🌐 API Docs:       http://localhost:8000/docs
# 📊 Dashboard:      http://localhost:8501
# 📈 MLflow UI:      http://localhost:5000
# 💾 DB Admin:       pgAdmin (optionnel)

# 5. Arrêter les services
docker-compose down
```

### Logs et débogage:
```bash
# Voir les logs d'un service
docker-compose logs api
docker-compose logs dashboard
docker-compose logs db

# Logs en temps réel
docker-compose logs -f api
```

---

## 🖥️ Installation Locale

Pour développement ou si vous préférez sans Docker.

### 1️⃣ Créer l'environment Conda

```bash
# Créer environment
conda env create -f environment.yml

# Activer
conda activate topnet-ocr

# Vérifier
python --version  # Doit être 3.10+
```

### 2️⃣ Installer les dépendances Python

```bash
pip install -r requirements.txt

# Vérifier l'installation
python -c "import torch; print(torch.__version__)"
```

### 3️⃣ Configurer les variables d'environnement

```bash
# Copier le template
cp .env.example .env

# Éditer .env avec vos paramètres
nano .env
# OU
code .env  # Si VS Code
```

**Contenu de `.env` par défaut:**
```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=topnet_ocr
DB_USER=postgres
DB_PASSWORD=postgres

# API
API_HOST=0.0.0.0
API_PORT=8000

# ML Models
TORCH_HOME=/path/to/models
OCR_BACKEND=paddle  # ou easyocr, tesseract

# Logging
LOG_LEVEL=INFO
```

### 4️⃣ Initialiser la Base de Données

```bash
# S'assurer que PostgreSQL tourne en local ou via Docker
# Si Docker: docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15

# Initialiser les tables
python scripts/init_db.py

# Vérifier
psql -U postgres -d topnet_ocr -c "\dt"
```

### 5️⃣ Démarrer l'API

```bash
# Terminal 1: API FastAPI
python -m uvicorn src.api:app --reload --port 8000

# Voir les docs
# 🌐 http://localhost:8000/docs
```

### 6️⃣ Démarrer le Dashboard

```bash
# Terminal 2: Streamlit Dashboard
streamlit run dashboard/app.py

# Voir
# 📊 http://localhost:8501
```

---

## ✅ Tests après installation

### 1. Health Check API
```bash
curl http://localhost:8000/health
# Réponse:
# {"status":"healthy","version":"1.0.0"}
```

### 2. Uploader un document (Dashboard)
1. Aller à `http://localhost:8501`
2. Upload un document (CIN, facture, contrat)
3. Voir la classification et OCR

### 3. Tester via API avec curl
```bash
# Upload document
curl -X POST http://localhost:8000/upload \
  -F "file=@sample.pdf"

# Récupérer résultats
curl http://localhost:8000/documents
```

### 4. Lancer les tests unitaires
```bash
# Tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=src

# Un fichier spécifique
pytest tests/test_classification.py -v
```

---

## 🐛 Dépannage

### ❌ Erreur: "ModuleNotFoundError: No module named 'torch'"
```bash
# Solution
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### ❌ Erreur: "Connection refused - PostgreSQL"
```bash
# Vérifier que la BD tourne
docker ps | grep postgres

# Ou démarrer
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15
```

### ❌ Erreur: "Port 8000 already in use"
```bash
# Utiliser un autre port
python -m uvicorn src.api:app --port 8001

# Ou arrêter le service
lsof -ti:8000 | xargs kill -9
```

### ❌ Erreur: "OCR model not found"
```bash
# Télécharger les modèles
python scripts/download_models.py

# Ou spécifier le chemin
export OCR_MODEL_PATH=/path/to/models
```

---

## 🚀 Démarrage Rapide Après Installation

**Pour Docker:**
```bash
docker-compose up -d
# Aller à http://localhost:8501
```

**Pour Local:**
```bash
# Terminal 1
python -m uvicorn src.api:app --reload

# Terminal 2
streamlit run dashboard/app.py
```

---

## 📚 Documentation Supplémentaire

- **Architecture détaillée**: [ARCHITECTURE.md](./ARCHITECTURE.md)
- **Guide de contribution**: [CONTRIBUTING.md](./CONTRIBUTING.md)
- **Changelog**: [CHANGELOG.md](./CHANGELOG.md)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💬 Besoin d'aide?

- 📖 Lire le [README.md](./README.md)
- 🐛 Créer une [Issue GitHub](https://github.com/TOPNET/topnet-ocr/issues)
- 📧 Contact: [email protected]

---

**Installation complétée!** 🎉 Commençons à utiliser TopNet OCR!
