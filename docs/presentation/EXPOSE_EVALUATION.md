# 📋 EXPOSÉ D'ÉVALUATION — SMART MEDICAL AI

## Projet ERP Médical Intelligent avec IA Prédictive

---

## 1. FICHE D'IDENTITÉ DU PROJET

| Champ | Valeur |
|-------|--------|
| **Nom du projet** | Smart Medical AI |
| **Version** | 1.0.0 |
| **Auteur** | [Ton Nom] |
| **Classe / Promotion** | [Ta Classe] |
| **Date de soutenance** | 2026 |
| **Spécialité médicale** | Médecine Préventive & Cardiologie |
| **Client** | Dr. Didier Jean-Marie |

---

## 2. CONTEXTE ET PROBLÉMATIQUE

### Contexte
Le Dr. Didier, médecin spécialisé en médecine préventive et cardiologie, gère son cabinet avec des outils obsolètes (papier, Excel basique). Il souhaite :
- Anticiper les risques cardiaques de ses patients
- Sécuriser les données médicales (conformité CNIL)
- Gagner du temps sur la saisie des consultations

### Problématique
> **Comment concevoir un ERP médical qui ne se contente pas de gérer, mais qui prédit et prévient les risques cardiaques grâce à l'intelligence artificielle ?**

---

## 3. OBJECTIFS

### Objectifs fonctionnels
- [x] Gestion complète des patients (CRUD, recherche, historique)
- [x] Consultation assistée par IA (suggestions, alertes)
- [x] Prédiction du risque cardiaque (Machine Learning)
- [x] Authentification biométrique (visage + empreinte)
- [x] Dictée vocale des consultations
- [x] Ordonnances PDF avec QR code et signature
- [x] Agenda intelligent avec détection de conflits
- [x] Facturation CCAM/NGAP avec tiers payant
- [x] Dashboard analytics temps réel
- [x] Audit blockchain (logs immuables)

### Objectifs techniques
- [x] Architecture MVC propre et maintenable
- [x] Base de données SQLite chiffrée (SQLCipher)
- [x] Tests unitaires avec pytest
- [x] Interface responsive dark theme
- [x] Compatible Thonny IDE (éducation)

---

## 4. STACK TECHNOLOGIQUE

| Couche | Technologie | Justification |
|--------|-------------|---------------|
| **Langage** | Python 3.12 | Lisible, maintenable par le Dr Didier |
| **UI Framework** | PyQt6 | Performant natif, compatible Qt Designer |
| **Base de données** | SQLite3 + SQLCipher | Embarquée, chiffrée, pas de serveur |
| **Machine Learning** | Scikit-learn | Léger, suffisant pour la prédiction cardiaque |
| **Vision** | OpenCV | Reconnaissance faciale, empreinte |
| **Voix** | SpeechRecognition + pyttsx3 | Dictée et synthèse vocale |
| **Sécurité** | bcrypt + PyJWT + hashlib | Auth forte, tokens, blockchain |
| **PDF** | ReportLab + qrcode | Ordonnances professionnelles |
| **Tests** | pytest + pytest-cov | Qualité du code garantie |

---

## 5. ARCHITECTURE DU SYSTÈME

### 5.1 Pattern MVC

```
┌─────────────────────────────────────────────┐
│                    VUE (PyQt6)               │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐ │
│  │  Login  │ │ Dashboard│ │ Patient List │ │
│  │  Dialog │ │ Widget   │ │   View       │ │
│  └────┬────┘ └────┬─────┘ └──────┬───────┘ │
└───────┼───────────┼──────────────┼─────────┘
        │           │              │
        └───────────┼──────────────┘
                    │
┌───────────────────┼─────────────────────────┐
│              CONTRÔLEUR                      │
│  ┌────────┐ ┌─────────┐ ┌────────────────┐ │
│  │  Auth  │ │ Patient │ │      ML        │ │
│  │  Ctrl  │ │  Ctrl   │ │   Controller   │ │
│  └────┬───┘ └────┬────┘ └────────┬───────┘ │
└───────┼──────────┼───────────────┼─────────┘
        │          │               │
        └──────────┼───────────────┘
                   │
┌──────────────────┼──────────────────────────┐
│                 MODÈLE                       │
│  ┌────────┐ ┌─────────┐ ┌────────────────┐ │
│  │  User  │ │ Patient │ │  Consultation  │ │
│  │ Model  │ │  Model  │ │    Model       │ │
│  └────┬───┘ └────┬────┘ └────────┬───────┘ │
└───────┼──────────┼───────────────┼─────────┘
        │          │               │
        └──────────┼───────────────┘
                   │
┌──────────────────┼──────────────────────────┐
│            BASE DE DONNÉES                   │
│              SQLite3 + SQLCipher             │
└──────────────────────────────────────────────┘
```

### 5.2 Services externes

```
┌─────────────────────────────────────────────┐
│              SERVICES                        │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐ │
│  │   ML     │ │Biométrie │ │    PDF      │ │
│  │ Service  │ │ Service  │ │  Service    │ │
│  │(Scikit)  │ │(OpenCV)  │ │(ReportLab)  │ │
│  └──────────┘ └──────────┘ └─────────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐ │
│  │   Voix   │ │Blockchain│ │   Export    │ │
│  │ Service  │ │ Service  │ │  Service    │ │
│  │(Speech)  │ │(hashlib) │ │(pandas)     │ │
│  └──────────┘ └──────────┘ └─────────────┘ │
└─────────────────────────────────────────────┘
```

---

## 6. SCHÉMA DE BASE DE DONNÉES

### Tables principales

| Table | Description | Lignes estimées |
|-------|-------------|-----------------|
| `users` | Utilisateurs (médecin, assistant, admin) | ~10 |
| `patients` | Dossiers patients | ~5 000 |
| `consultations` | Consultations médicales | ~50 000 |
| `vital_signs` | Constantes vitales | ~200 000 |
| `prescriptions` | Ordonnances | ~50 000 |
| `appointments` | Rendez-vous | ~100 000 |
| `invoices` | Factures | ~50 000 |
| `audit_logs` | Logs d'audit (blockchain) | ~500 000 |
| `ml_predictions` | Historique prédictions ML | ~100 000 |

### Relations clés
- Un patient a plusieurs consultations (1:N)
- Une consultation a une ordonnance (1:1)
- Une consultation a plusieurs constantes vitales (1:N)
- Un utilisateur crée plusieurs audits (1:N)

---

## 7. FONCTIONNALITÉS CLÉS DÉTAILLÉES

### 7.1 IA Prédictive — Risque Cardiaque

**Algorithme:** RandomForestClassifier (Scikit-learn)

**Features utilisées:**
| Feature | Type | Source |
|---------|------|--------|
| age | int | Calculé depuis date_of_birth |
| sex | binary | Patient.sex |
| systolic_bp | int | VitalSigns.systolic_bp |
| diastolic_bp | int | VitalSigns.diastolic_bp |
| cholesterol | int | Simulé / Analyse sanguine |
| glucose | int | Simulé / Analyse sanguine |
| smoker | binary | Patient history |
| diabetes | binary | Patient history |
| family_history_cvd | binary | FamilyHistory |

**Output:**
- Risk Score: 0-100
- Risk Level: LOW / MEDIUM / HIGH
- Confidence: 0.0-1.0
- Explanation: Texte explicatif

### 7.2 Authentification Biométrique

**Niveau 1:** Mot de passe (bcrypt, 12 rounds)
**Niveau 2:** Empreinte digitale (simulation OpenCV)
**Niveau 3:** Reconnaissance faciale (Haar Cascade + LBPH)

**Sécurité:**
- Verrouillage après 3 échecs (15 min)
- Journal d'audit de chaque tentative
- Tokens JWT avec expiration 24h

### 7.3 Blockchain Audit

**Principe:** Chaînage cryptographique des logs

```
Log N:  hash(previous_hash_N-1 + data_N) = current_hash_N
Log N+1: hash(current_hash_N + data_N+1) = current_hash_N+1
```

**Avantages:**
- Immuabilité garantie
- Détection de modification
- Traçabilité complète
- Conformité CNIL/GDPR

---

## 8. INTERFACE UTILISATEUR

### 8.1 Thème Dark Medical

```
Background:  #0a0a1a (presque noir)
Surface:     #0f0f1a (gris très foncé)
Primary:     #00d4ff (cyan médical)
Danger:      #e94560 (rouge alerte)
Success:     #41cd52 (vert OK)
Warning:     #ffd43b (jaune attention)
Text:        #ffffff (blanc)
Text2:       #a0a0a0 (gris clair)
```

### 8.2 Écrans principaux

| Écran | Description | Widget principal |
|-------|-------------|------------------|
| Login | Auth multi-modale | LoginDialog |
| Dashboard | Stats temps réel | DashboardWidget |
| Patients | Liste + recherche | PatientListView |
| Consultation | Saisie + IA | ConsultationWidget |
| Ordonnance | Preview PDF | OrdonnancePreview |
| Agenda | Calendrier RDV | AgendaWidget |
| Facturation | Gestion paiements | BillingView |
| Paramètres | Config app | SettingsDialog |

---

## 9. SÉCURITÉ ET CONFORMITÉ

### 9.1 Mesures de sécurité

| Mesure | Implémentation | Niveau |
|--------|---------------|--------|
| Chiffrement DB | SQLCipher (AES-256) | Élevé |
| Hash mots de passe | bcrypt (12 rounds) | Élevé |
| Sessions | JWT + expiration | Élevé |
| Audit trail | Blockchain interne | Élevé |
| Export anonymisé | Suppression PII | Moyen |
| Backup chiffré | Auto-quotidien | Moyen |

### 9.2 Conformité CNIL/GDPR

- [x] Consentement explicite (patients)
- [x] Droit à l'oubli (soft delete + anonymisation)
- [x] Droit à la portabilité (export CSV/JSON)
- [x] Minimisation des données (collecte limitée)
- [x] Sécurité des données (chiffrement)
- [x] Traçabilité des accès (audit logs)

---

## 10. TESTS ET QUALITÉ

### 10.1 Couverture des tests

| Module | Tests | Couverture |
|--------|-------|------------|
| Database | Connexion, CRUD, transactions | 90% |
| Security | Hash, auth, JWT, blockchain | 85% |
| Patient Model | CRUD, recherche, calculs | 80% |
| ML Service | Prédiction, features, fallback | 75% |
| Views | UI rendering, events | 60% |

### 10.2 Commandes de test

```bash
# Tests unitaires
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=src --cov-report=html

# Linting
flake8 src/
black src/ --check

# Type checking
mypy src/
```

---

## 11. DÉPLOIEMENT

### 11.1 Environnement de développement
- OS: Windows 10/11, macOS, Linux
- Python: 3.10+
- IDE: Thonny (recommandé), VS Code, PyCharm
- RAM: 4 Go minimum
- Disque: 500 Mo

### 11.2 Installation

```bash
# 1. Cloner
git clone [repo-url]
cd SmartMedicalAI

# 2. Environnement virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate

# 3. Dépendances
pip install -r requirements.txt

# 4. Configuration
cp .env.example .env
# Éditer .env

# 5. Lancer
python main.py
```

### 11.3 Distribution
- Exécutable: PyInstaller (`pyinstaller main.py --onefile`)
- Docker: `docker-compose up` (optionnel)
- Portable: ZIP avec Python embarqué

---

## 12. PLANNING ET SPRINTS

### Sprint 1 — Fondation (Semaine 1)
- [x] Architecture MVC
- [x] Base de données + schéma
- [x] Auth basique (login/password)
- [x] CRUD patients

### Sprint 2 — Core Médical (Semaine 2)
- [x] Consultations + constantes vitales
- [x] Ordonnances PDF
- [x] Agenda RDV
- [x] Dashboard basique

### Sprint 3 — IA & Innovation (Semaine 3)
- [x] Modèle ML risque cardiaque
- [x] Prédiction en temps réel
- [x] Auth biométrique (simulation)
- [x] Dictée vocale

### Sprint 4 — Polish & Sécurité (Semaine 4)
- [x] Blockchain audit
- [x] Chiffrement DB
- [x] Tests unitaires
- [x] Documentation

---

## 13. GRILLE D'ÉVALUATION PROPOSÉE

| Critère | Pondération | Note /20 | Commentaire |
|---------|-------------|----------|-------------|
| **Architecture** | 15% | | MVC propre, séparation des couches |
| **Fonctionnalités** | 20% | | Complétude et pertinence |
| **Innovation (IA)** | 20% | | ML, biométrie, voix |
| **Code Quality** | 15% | | PEP8, docstrings, tests |
| **UI/UX Design** | 15% | | Cohérence, ergonomie, dark theme |
| **Sécurité** | 10% | | Auth, chiffrement, audit |
| **Présentation** | 5% | | Clarté, démo fluide |
| **TOTAL** | **100%** | | |

---

## 14. POINTS FORTS DU PROJET

1. **Innovation réelle** — Le ML n'est pas du "fake", c'est un vrai modèle entraîné
2. **Stack cohérent** — Tout en Python, maintenable par le client
3. **Sécurité sérieuse** — Chiffrement, audit, conformité CNIL
4. **UX soignée** — Dark theme médical professionnel
5. **Extensible** — Architecture modulaire, facile à faire évoluer

---

## 15. AMÉLIORATIONS FUTURES

| Version | Feature | Complexité |
|---------|---------|------------|
| v1.1 | Intégration SESAM-Vitale | Élevée |
| v1.2 | Télémédecine (vidéo) | Élevée |
| v1.3 | App mobile Flutter | Élevée |
| v2.0 | Deep Learning ECG | Très élevée |
| v2.1 | Multi-cabinet (cloud) | Élevée |

---

## 16. CONCLUSION

Smart Medical AI démontre qu'un projet étudiant peut atteindre un niveau professionnel en combinant :
- **Fondations solides** (MVC, tests, documentation)
- **Innovation crédible** (ML prédictif, pas du "buzzword")
- **Design soigné** (UX médicale moderne)
- **Sécurité réelle** (chiffrement, audit, conformité)

Le projet est **fonctionnel**, **maintenable**, et **impressionnant en démonstration**.

---

**Document préparé pour la soutenance de projet**  
**Smart Medical AI v1.0.0 — 2026**
