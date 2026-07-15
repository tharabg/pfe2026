# 🔌 GUIDE SWAGGER - TopNet OCR APIs
## Tester les APIs depuis l'interface interactive

---

## 🚀 DÉMARRAGE RAPIDE

### Étape 1: Lancer Docker Compose
```bash
docker-compose up -d
# Attendre 30-60 secondes...
```

### Étape 2: Ouvrir Swagger
```
Navigateur: http://localhost:8000/docs
```

Vous verrez une interface interactive avec tous les endpoints.

---

## 🔍 ENDPOINTS À TESTER (Dans l'ordre)

### ✅ TEST 1: `/health` (GET)
**Objectif:** Vérifier que l'API est en ligne

**Étapes dans Swagger:**
1. Localiser `GET /health`
2. Cliquer "Try it out"
3. Cliquer "Execute"

**Résultat attendu:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

**Code:** 200 OK ✅

---

### ✅ TEST 2: `/documents` (GET)
**Objectif:** Lister les documents (sera vide au début)

**Étapes dans Swagger:**
1. Localiser `GET /documents`
2. Cliquer "Try it out"
3. Voir paramètres optionnels:
   - `page` (défaut: 1)
   - `limit` (défaut: 20)
   - `document_type` (CIN, Facture, Contrat)
   - `status` (completed, processing, failed)
4. Cliquer "Execute"

**Résultat attendu (au départ):**
```json
{
  "total": 0,
  "page": 1,
  "limit": 20,
  "documents": []
}
```

**Code:** 200 OK ✅

---

### ✅ TEST 3: `/stats` (GET)
**Objectif:** Voir les statistiques système

**Étapes dans Swagger:**
1. Localiser `GET /stats`
2. Cliquer "Try it out"
3. Cliquer "Execute"

**Résultat attendu (au départ):**
```json
{
  "timestamp": "2026-04-24T18:30:00",
  "total_documents": 0,
  "documents_by_type": {
    "CIN": 0,
    "Facture": 0,
    "Contrat": 0
  },
  "documents_by_status": {
    "completed": 0,
    "processing": 0,
    "failed": 0
  },
  "average_processing_time_ms": 0,
  "average_ocr_confidence": 0,
  "average_classification_confidence": 0,
  "today_processed": 0,
  "error_rate_percent": 0
}
```

**Code:** 200 OK ✅

---

### 🔥 TEST 4: `/upload` (POST) - PRINCIPAL!
**Objectif:** Uploader un document et lancer le pipeline complet

**Étapes dans Swagger:**
1. Localiser `POST /upload`
2. Cliquer "Try it out"
3. Voir les paramètres:
   - `file` (requis): Image JPG/PNG/PDF
   - `target_language` (optionnel): "en", "fr", "ar"
4. **Cliquer sur l'input "file"**
5. **Sélectionner une image** (CIN, Facture, ou Contrat)
6. **Cliquer "Execute"**

**Attendre:** 2-3 secondes (le pipeline traite)

**Résultat attendu:**
```json
{
  "status": "success",
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "document_type": "CIN",
  "classification_confidence": 0.96,
  "extracted_fields": {
    "numero": "12345678",
    "nom": "BEN GHORBEL",
    "prenom": "THARA",
    "date_naissance": "01/01/1995",
    "validite": "31/12/2030"
  },
  "validation_results": {
    "numero": {"status": "OK", "value": "12345678"},
    "nom": {"status": "OK", "value": "BEN GHORBEL"},
    "date_naissance": {"status": "OK", "value": "01/01/1995"}
  },
  "processing_time_ms": 2450
}
```

**Code:** 200 OK ✅

**📝 À noter:** Copier le `document_id` pour utiliser dans tests suivants!

---

### ✅ TEST 5: `/documents/{id}` (GET)
**Objectif:** Récupérer détails d'un document

**Étapes dans Swagger:**
1. Localiser `GET /documents/{id}`
2. Cliquer "Try it out"
3. **Coller le `document_id` du test 4** dans le champ `id`
4. Cliquer "Execute"

**Résultat attendu:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "cin_001_uuid.jpg",
  "document_type": "CIN",
  "document_type_confidence": 0.96,
  "status": "completed",
  "uploaded_at": "2026-04-24T18:30:00",
  "processed_at": "2026-04-24T18:30:02.450",
  "processing_metadata": {
    "preprocessing_time_ms": 450,
    "classification_time_ms": 320,
    "ocr_time_ms": 1200,
    "extraction_time_ms": 200,
    "translation_time_ms": 150
  }
}
```

**Code:** 200 OK ✅

---

### ✅ TEST 6: `/documents/{id}/extraction` (GET)
**Objectif:** Voir les résultats d'extraction complète (OCR + champs)

**Étapes dans Swagger:**
1. Localiser `GET /documents/{id}/extraction`
2. Cliquer "Try it out"
3. **Coller le `document_id` du test 4**
4. Cliquer "Execute"

**Résultat attendu:**
```json
{
  "extraction_id": "uuid-yyy-yyy",
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "raw_text": "Numéro: 12345678\nNom: BEN GHORBEL\nPrénom: THARA\nDate naissance: 01/01/1995\n...",
  "ocr_confidence": 0.92,
  "ocr_backend": "paddleocr",
  "extracted_fields": {
    "numero": "12345678",
    "nom": "BEN GHORBEL",
    "prenom": "THARA",
    "date_naissance": "01/01/1995",
    "validite": "31/12/2030"
  },
  "field_validation": {
    "numero": {"status": "OK", "value": "12345678"},
    "nom": {"status": "OK", "value": "BEN GHORBEL"},
    "date_naissance": {"status": "OK", "value": "01/01/1995"}
  },
  "translations": {
    "transliterated": "Ahmed Ben Ghorbel",
    "translated_en": "Ahmed Ben Ghorbel",
    "translated_fr": "Ahmed Ben Ghorbel"
  }
}
```

**Code:** 200 OK ✅

---

## 📊 RÉSUMÉ FLUX DE TEST

```
1️⃣ GET /health
   ✅ Confirme API alive

2️⃣ GET /documents
   ✅ Confirme BD accessible (résultat vide = normal)

3️⃣ GET /stats
   ✅ Confirme statistiques (tout 0 = normal)

4️⃣ POST /upload ← PRINCIPAL!
   ✅ Pipeline complet
   ✅ Classification (96%)
   ✅ OCR (92%)
   ✅ Extraction champs
   ✅ Validation
   ⚠️ Récupérer document_id

5️⃣ GET /documents/{id}
   ✅ Métadonnées document
   ✅ Timing par étape

6️⃣ GET /documents/{id}/extraction
   ✅ Résultats OCR complets
   ✅ Champs extraits
   ✅ Translations
```

---

## 🎯 RÉSULTATS ATTENDUS

### Classification Accuracy
- ✅ 96% pour CIN
- ✅ 96% pour Facture
- ✅ 98% pour Contrat

### OCR Accuracy
- ✅ 92% moyenne
- ✅ 88% pour arabe (complexe)
- ✅ 95% pour français

### Temps Traitement
- ✅ Moyenne: 2,450ms
- ✅ Min: 800ms
- ✅ Max: 8,200ms (documents longs)

### Champs Extraits
- ✅ CIN: numéro, nom, prénom, date naissance, validité
- ✅ Facture: numéro, date, montant, client, vendeur
- ✅ Contrat: parties, date, type, montant

---

## ⚠️ ERREURS COURANTES & SOLUTIONS

### Erreur: "Cannot connect to http://localhost:8000"
**Cause:** Docker Compose pas démarré
```bash
docker-compose up -d
# Attendre 30 secondes
```

### Erreur: "Port 8000 already in use"
```bash
# Solution
docker-compose down
docker-compose up -d
```

### Erreur: "Database connection refused"
```bash
# Solution
docker-compose logs db
docker-compose restart db
```

### Erreur: "Model not found"
```bash
# Solution
# Vérifier modèles dans ./models/
ls -la models/
```

### Timeout sur /upload
```bash
# Cause: Image très grande
# Solution: Réduire taille image < 50MB
```

---

## 📝 DOCUMENTATION COMPLÈTE

**Voir aussi:**
- `README.md` - Getting started
- `ARCHITECTURE.md` - Design technique
- `figures/02_API_Decisions_Engineer.txt` - Décisions par API
- `JOURNAL.md` - Travail détaillé

---

## 🔗 LIENS UTILES

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Dashboard:** http://localhost:8501
- **MLflow:** http://localhost:5000
- **API Base:** http://localhost:8000

---

**Happy Testing! 🚀**

Date: 24 avril 2026
Stagiaire: Ben Ghorbel Thara
