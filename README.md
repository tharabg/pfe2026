# TopNet OCR - Système Intelligent d'OCR avec Pipeline ETL

Système complet d'OCR multimodal avec architecture microservices, MLOps, et dashboards interactifs pour traiter et extraire les données de documents officiels (CIN, factures, contrats).

## 🎯 Objectifs du Projet

- ✅ Classification automatique de documents (CIN, Factures, Contrats)
- ✅ Extraction de champs structurés via OCR multilingue
- ✅ Translittération et traduction (Arabe ↔ Latin/Langues)
- ✅ Pipeline ETL complète avec PostgreSQL
- ✅ Dashboards interactifs avec Streamlit
- ✅ Architecture microservices avec Docker
- ✅ MLOps avec DVC et MLflow pour gestion des modèles

## 📁 Structure du Projet

```
topnet-ocr/
├── src/                          # Code source principal
│   ├── __init__.py
│   ├── config.py                 # Configuration centralisée
│   ├── preprocessing.py          # Prétraitement d'images
│   ├── classification.py         # Classification (CLIP VLM)
│   ├── ocr.py                    # OCR multilingue
│   ├── translation.py            # Traduction & translittération
│   ├── models.py                 # Modèles SQLAlchemy
│   ├── etl_pipeline.py           # Pipeline ETL complète
│   └── api.py                    # API FastAPI
├── scripts/                      # Scripts d'entraînement & utilitaires
│   ├── prepare_data.py
│   ├── preprocess.py
│   ├── train_classifier.py
│   ├── train_ocr.py
│   └── evaluate.py
├── dashboard/                    # Dashboard Streamlit
│   ├── app.py
│   └── Dockerfile
├── data/                         # Données
│   ├── raw/                      # Données brutes
│   ├── processed/                # Données traitées
│   ├── preprocessed/             # Images prétraitées
│   └── uploads/                  # Documents uploadés
├── models/                       # Modèles pré-entraînés
│   ├── efficientnet_b0_best.pth  # Classifier
│   ├── classes.json              # Classes
│   └── document_classifier.pth
├── tests/                        # Tests unitaires
├── mlruns/                       # MLflow experiments
├── logs/                         # Logs d'application
├── Dockerfile                    # API container
├── docker-compose.yml            # Orchestration containers
├── requirements.txt              # Dépendances Python
├── environment.yml               # Conda environment
├── dvc.yaml                      # DVC pipeline
├── params.yaml                   # Paramètres MLOps
└── README.md                     # Ce fichier
```

## 🏗️ Architecture

### Microservices
```
┌─────────────────┐
│   Streamlit     │ (Port 8501)
│   Dashboard     │
└────────┬────────┘
         │
┌────────▼────────────────────┐
│  FastAPI Backend            │ (Port 8000)
│  - Upload Documents         │
│  - Process Pipeline         │
│  - Store Results            │
└────────┬────────────────────┘
         │
    ┌────▼────┬──────────┬──────────┐
    │          │          │          │
┌───▼──┐  ┌───▼──┐  ┌───▼──┐  ┌───▼──┐
│ Pre  │  │Class │  │ OCR  │  │Trans │
│process│  │ify  │  │      │  │late  │
└──────┘  └──────┘  └──────┘  └──────┘
    │          │          │          │
┌───▼──────────▼──────────▼──────────▼──┐
│    PostgreSQL Database (Port 5432)    │
│    - Documents                         │
│    - Extraction Results                │
│    - Translations                      │
│    - Processing Logs                   │
│    - Model Metrics                     │
└────────────────────────────────────────┘
```

## 🚀 Démarrage Rapide

### Option 1 : Avec Docker Compose (Recommandé)

```bash
# 1. Cloner le repository
git clone <repo-url>
cd topnet-ocr

# 2. Démarrer les services
docker-compose up -d

# 3. Accéder aux services
# API: http://localhost:8000
# Dashboard: http://localhost:8501
# MLflow: http://localhost:5000
```

### Option 2 : Installation Locale

```bash
# 1. Créer environment Conda
conda env create -f environment.yml
conda activate topnet-ocr

# 2. Installer dépendances pip
pip install -r requirements.txt

# 3. Configurer variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# 4. Initialiser la base de données
python scripts/init_db.py

# 5. Démarrer l'API
python -m uvicorn src.api:app --reload --port 8000

# 6. Démarrer le dashboard (dans un autre terminal)
streamlit run dashboard/app.py
```

## 📚 Modèles Utilisés

### Classification de Documents
- **CLIP ViT-Base-Patch32** (Vision Language Model)
  - Classifie les types de documents
  - Multimodal (texte + image)
  - Confiance de ~95%

### OCR (Reconnaissance de Texte)
- **PaddleOCR** (Backend principal)
  - Support multilingue (EN, AR, FR, etc.)
  - Détection d'orientation
  - Confiance de ~92%
- **EasyOCR** (Alternative)
- **Tesseract** (Fallback)

### Traduction & Translittération
- **Mistral** / **Ollama** (LLM local)
  - Traduction et extraction de contexte
  - Translittération Arabe → Latin
  - Suppression des diacritiques

### Extraction de Champs
- **spaCy** (NLP)
  - Reconnaissance d'entités nommées
  - Validation de champs
  - Patterns regex avancés

## 🔄 Pipeline ETL

```
1. UPLOAD
   ↓
2. PREPROCESSING
   - Resize, Deskew, Denoise
   - Contrast Enhancement
   ↓
3. CLASSIFICATION
   - CLIP VLM pour type de doc
   ↓
4. OCR
   - Extraction de texte
   - Détection de zones
   ↓
5. EXTRACTION STRUCTURÉE
   - Identification de champs
   - Validation des données
   ↓
6. TRANSLATION/TRANSLITERATION
   - Conversion Ar→Latin
   - Traduction multi-langue
   ↓
7. STORAGE
   - PostgreSQL
   - Métadonnées complètes
```

## 🤖 MLOps avec DVC et MLflow

### Entraînement des Modèles

```bash
# Exécuter le pipeline complet
dvc repro

# Ou étapes individuelles
dvc repro stages/prepare
dvc repro stages/preprocess
dvc repro stages/train_classifier
dvc repro stages/train_ocr
dvc repro stages/evaluate
```

### Tracking des Expériences

```bash
# Démarrer MLflow UI
mlflow ui

# Accéder à: http://localhost:5000
```

### DVC Remote (Stockage des Modèles)

```bash
# Configurer remote S3 (exemple)
dvc remote add -d myremote s3://my-bucket/topnet-ocr
dvc remote modify myremote profile myprofile

# Push models
dvc push

# Pull models
dvc pull
```

## 📊 API Endpoints

### Upload
```bash
POST /upload
- file: Document file
- target_language: en, ar, fr

POST /batch-upload
- files: Multiple files
- target_language: en, ar, fr
```

### Retrieval
```bash
GET /documents              # List all documents
GET /documents/{id}         # Get document details
GET /documents/{id}/extraction  # Get extraction results
GET /stats                  # System statistics
GET /health                 # Health check
```

### Example
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.jpg" \
  -F "target_language=en"
```

## 🎨 Dashboard Streamlit

Accédez à `http://localhost:8501` pour :

- 📊 **Dashboard** : Vue d'ensemble des statistiques
- 📤 **Upload** : Traitement de documents
- 📈 **Statistics** : Performances des modèles
- 🤖 **Model Metrics** : Détails des modèles IA
- ⚙️ **Settings** : Configuration système

## 🧪 Tests

```bash
# Exécuter tous les tests
pytest tests/

# Tests avec couverture
pytest --cov=src tests/

# Tests spécifiques
pytest tests/test_ocr.py -v
```

## 📝 Configuration

Créer `.env` à la racine :

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

# Models
DOCUMENT_CLASSIFIER_MODEL=efficientnet_b0
OCR_MODEL=paddle
VLM_MODEL=openai/clip-vit-base-patch32
LLM_MODEL=mistral

# MLOps
MLFLOW_TRACKING_URI=file:./mlruns
DVC_REMOTE=s3://my-bucket/topnet-ocr
```

## 🔍 Débogage

```bash
# Logs de l'API
docker logs topnet_ocr_api

# Logs de la DB
docker logs topnet_ocr_db

# Entrer dans le container
docker exec -it topnet_ocr_api /bin/bash

# Voir les modèles entraînés
dvc dag
dvc metrics show
```

## 📦 Dépendances Principales

- **Deep Learning** : PyTorch, Transformers, Accelerate
- **OCR** : PaddleOCR, EasyOCR, Tesseract
- **API** : FastAPI, Uvicorn
- **Database** : PostgreSQL, SQLAlchemy
- **Dashboard** : Streamlit, Plotly
- **MLOps** : DVC, MLflow
- **NLP** : spaCy, Langchain

## 🐛 Troubleshooting

### Problème : "Cannot connect to API"
```bash
# Vérifier que les containers tournent
docker-compose ps

# Redémarrer les services
docker-compose restart api
```

### Problème : "Port already in use"
```bash
# Changer les ports dans docker-compose.yml
# ou

# Libérer le port
lsof -i :8000
kill -9 <PID>
```

### Problème : "GPU not detected"
```bash
# Vérifier CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Pour CPU only, éditer src/config.py
# Changer: device = torch.device("cpu")
```

## 📈 Prochaines Étapes

- [ ] Ajouter fine-tuning sur données réelles
- [ ] Implémenter queue/worker pour traitement async
- [ ] Ajouter support de plus de types de documents
- [ ] Intégrer webhooks pour notifications
- [ ] Monitoring et alertes (Prometheus + Grafana)
- [ ] API Gateway et authentification
- [ ] Tests de charge et optimisation

## 🤝 Contribution

```bash
# Fork et clone
git clone <votre-fork>
cd topnet-ocr

# Créer branche feature
git checkout -b feature/amazing-feature

# Commit changes
git commit -m 'Add amazing feature'

# Push
git push origin feature/amazing-feature

# Créer Pull Request
```

## 📄 License

MIT License - Voir LICENSE file

## 📞 Support

Pour les problèmes ou questions :
- Créer une issue sur GitHub
- Contacter l'équipe TopNet

---

**Version** : 0.1.0  
**Dernière mise à jour** : 2024-04-23  
**Mainteneur** : TopNet Team
