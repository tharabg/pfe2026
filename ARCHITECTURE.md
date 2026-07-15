# 🏗️ Architecture du Projet

Documentation complète de l'architecture technique de **TopNet OCR**.

## 📊 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOPNET OCR ARCHITECTURE                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│  FRONTEND LAYER     │
├─────────────────────┤
│ Streamlit Dashboard │ (Port 8501)
│ - Upload documents  │
│ - Visualize results │
│ - View metrics      │
└──────────┬──────────┘
           │
┌──────────▼──────────────────────────────────────────┐
│        API LAYER - FastAPI Backend                   │
├──────────────────────────────────────────────────────┤
│ /upload        - Document upload                     │
│ /classify      - Get document classification         │
│ /extract       - OCR & field extraction              │
│ /translate     - Translation & transliteration       │
│ /documents     - List all documents                  │
│ /results       - Get extraction results              │
│ /health        - Health check                        │
│ /docs          - Swagger documentation               │
└──────────┬───────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────┐
│      PROCESSING LAYER - ML Pipelines                 │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ Preprocessing Module                         │   │
│  │ - Image normalization                        │   │
│  │ - Rotation correction                        │   │
│  │ - Contrast enhancement                       │   │
│  └──────────────────────────────────────────────┘   │
│                    ↓                                 │
│  ┌──────────────────────────────────────────────┐   │
│  │ Classification Module (EfficientNet)         │   │
│  │ - CIN / Facture / Contrat detection          │   │
│  │ - Confidence score (96% accuracy)            │   │
│  └──────────────────────────────────────────────┘   │
│                    ↓                                 │
│  ┌──────────────────────────────────────────────┐   │
│  │ OCR Module (PaddleOCR/EasyOCR/Tesseract)     │   │
│  │ - Text extraction                            │   │
│  │ - Multi-language support (EN, AR, FR)        │   │
│  │ - Confidence estimation                      │   │
│  └──────────────────────────────────────────────┘   │
│                    ↓                                 │
│  ┌──────────────────────────────────────────────┐   │
│  │ Translation & Transliteration Module         │   │
│  │ - Arabic → Latin transliteration             │   │
│  │ - Language translation                       │   │
│  │ - Field structured extraction                │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
└──────────┬───────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────┐
│       DATA LAYER - PostgreSQL Database               │
├──────────────────────────────────────────────────────┤
│                                                      │
│ Tables:                                              │
│ - documents          (metadata, classification)      │
│ - extraction_results (OCR text, fields)              │
│ - translations       (translated content)            │
│ - processing_logs    (audit trail)                   │
│ - model_metrics      (ML performance)                │
│                                                      │
└──────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│      MONITORING & EXPERIMENTS (MLflow, DVC)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Structure des fichiers

```
topnet-ocr/
├── src/                          # Code source principal
│   ├── __init__.py
│   ├── config.py                 # ⚙️  Configuration centralisée
│   ├── preprocessing.py          # 🖼️  Preprocessing d'images
│   ├── classification.py         # 🏷️  Classification (EfficientNet)
│   ├── ocr.py                    # 📝 OCR multilingue
│   ├── translation.py            # 🌐 Traduction & translittération
│   ├── models.py                 # 🗄️  Modèles SQLAlchemy
│   ├── etl_pipeline.py           # 🔄 Pipeline ETL complète
│   └── api.py                    # 🔌 API FastAPI
│
├── scripts/                      # Scripts utilitaires
│   ├── init_db.py               # Initialiser BD
│   ├── prepare_data.py          # Préparer données
│   ├── train_classifier.py      # Entraîner classificateur
│   ├── train_ocr.py             # Entraîner OCR
│   └── evaluate.py              # Évaluer modèles
│
├── dashboard/                    # Frontend Streamlit
│   ├── app.py                   # App principale
│   └── Dockerfile               # Container
│
├── tests/                        # Tests unitaires
│   ├── test_preprocessing.py
│   ├── test_classification.py
│   ├── test_ocr.py
│   └── test_api.py
│
├── data/                         # Données
│   ├── raw/                     # Données brutes
│   ├── processed/               # Données traitées
│   ├── preprocessed/            # Images prétraitées
│   └── uploads/                 # Documents uploadés
│
├── models/                       # Modèles pré-entraînés
│   ├── efficientnet_b0_best.pth
│   ├── classes.json
│   └── document_classifier.pth
│
├── mlruns/                       # MLflow experiments
├── logs/                         # Logs application
│
├── Dockerfile                    # Container API
├── docker-compose.yml            # Orchestration containers
├── requirements.txt              # Dépendances Python
├── environment.yml               # Environment Conda
├── dvc.yaml                      # DVC pipeline
├── params.yaml                   # Paramètres MLOps
│
├── README.md                     # Documentation
├── INSTALLATION.md               # Guide installation
├── CONTRIBUTING.md               # Guide contribution
├── ARCHITECTURE.md               # Ce fichier
├── CHANGELOG.md                  # Historique
└── LICENSE                       # Licence MIT
```

---

## 🔄 Flux de données complet

### Exemple: Upload → Classification → OCR → Stockage

```
1. USER UPLOADS DOCUMENT
   └─→ PDF/Image file
   
2. API RECEIVES & VALIDATES
   └─→ POST /upload
   └─→ File stored in /data/uploads
   └─→ Document record created in DB
   
3. PREPROCESSING
   └─→ Load image with OpenCV
   └─→ Normalize dimensions
   └─→ Enhance contrast
   └─→ Detect rotation & correct
   
4. CLASSIFICATION
   └─→ Pass to EfficientNet model
   └─→ Predict: CIN / Facture / Contrat
   └─→ Get confidence score (96% avg)
   └─→ Store classification in DB
   
5. OCR EXTRACTION
   └─→ Select OCR backend (PaddleOCR default)
   └─→ Extract text from image
   └─→ Get confidence per line
   └─→ Store raw_text in DB
   
6. FIELD EXTRACTION
   └─→ Parse OCR text with rules
   └─→ Extract key fields:
       - For CIN: Numero, Nom, Prenom, DOB, etc.
       - For Facture: Amount, Date, Vendor, etc.
       - For Contrat: Parties, Date, Terms, etc.
   
7. TRANSLATION (if needed)
   └─→ If Arabic detected: Transliterate to Latin
   └─→ Translate text if target_language != source
   
8. STORE RESULTS
   └─→ extraction_results table
   └─→ ocr_confidence, field_validation, etc.
   └─→ LOG all steps for audit trail
   
9. RETURN TO USER
   └─→ JSON response with:
       - document_type
       - extracted_fields
       - confidence_scores
       - processing_time
```

---

## 🧠 Modèles ML utilisés

### 1. Classification (EfficientNet-B0)
- **Framework**: PyTorch
- **Input**: Image (224x224 RGB)
- **Output**: Document class + confidence
- **Accuracy**: 96% on test set
- **Fine-tuning**: 2 phases (head + backbone)

### 2. OCR (PaddleOCR)
- **Framework**: PaddleOCR (default)
- **Languages**: EN, AR, FR, + others
- **Fallback**: EasyOCR, then Tesseract
- **Accuracy**: 92% confidence
- **Multi-orientation**: Auto-detects & rotates

### 3. Translation (LangChain + Ollama)
- **Framework**: LangChain with local LLM
- **Transliteration**: Arabic → Latin
- **Translation**: Multi-language support

---

## 💾 Base de données Schema

### Table: documents
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    document_type VARCHAR(50),           -- CIN / Facture / Contrat
    document_type_confidence FLOAT,
    upload_timestamp TIMESTAMP,
    processing_status VARCHAR(20),       -- pending / processing / completed / failed
    file_path VARCHAR(500),
    preprocessed_path VARCHAR(500),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Table: extraction_results
```sql
CREATE TABLE extraction_results (
    id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(id),
    raw_text TEXT,
    ocr_confidence FLOAT,
    extracted_fields JSONB,            -- {nom, prenom, numero, etc.}
    field_validation JSONB,             -- validation errors per field
    translations JSONB,                 -- {ar_to_latin, translations}
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔐 Security & Performance

### Security
- Input validation on all endpoints
- Sanitization of file uploads
- SQL injection prevention (SQLAlchemy)
- CORS configuration (if needed)
- Logging of all operations (audit trail)

### Performance
- Async API (FastAPI)
- Connection pooling (SQLAlchemy)
- Model caching (in memory)
- Batch processing ready
- Docker container isolation

---

## 🚀 Déploiement

### Production Setup
```bash
# Use docker-compose
docker-compose -f docker-compose.yml up -d

# Or Kubernetes (future)
kubectl apply -f k8s/
```

### Monitoring
- MLflow dashboard: http://localhost:5000
- API health: http://localhost:8000/health
- Logs: `docker-compose logs -f api`

---

## 📚 Références

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [PyTorch Docs](https://pytorch.org/)
- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Streamlit Docs](https://docs.streamlit.io/)

---

**Dernière mise à jour:** 2026-04-24  
**Maintenu par:** Ben Ghorbel Thara  
**Version:** 1.0.0
