# 🏥 Smart Medical AI

**Plateforme intelligente de gestion médicale avec IA prédictive**

> Développé pour le Dr. Didier — Médecine Préventive & Cardiologie

---

## ✨ Fonctionnalités

- 🤖 **IA Prédictive** — Prédiction du risque cardiaque avec Machine Learning
- 🔐 **Auth Biométrique** — Reconnaissance faciale + empreinte digitale
- 🎤 **Dictée Vocale** — Saisie vocale des consultations
- 🔒 **Blockchain Audit** — Logs immuables et traçables
- 📊 **Dashboard Temps Réel** — Statistiques et alertes live
- 💊 **Ordonnances PDF** — Génération avec QR code et signature
- 💰 **Facturation** — Gestion CCAM/NGAP, tiers payant
- 📱 **Responsive** — Interface adaptative dark theme

---

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.10+
- Thonny IDE (recommandé pour les débutants)
- Webcam (optionnel, pour biométrie)

### Installation

```bash
# 1. Cloner le projet
cd SmartMedicalAI

# 2. Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs

# 5. Lancer l'application
python main.py
```

### Identifiants de démo
- **Email:** `didier@smartmedical.ai`
- **Password:** `didier2024`
- **Rôle:** Docteur

---

## 🏗️ Architecture

```
SmartMedicalAI/
├── src/
│   ├── core/           # App, Database, Security, Events
│   ├── models/         # ORM léger (Patient, User, etc.)
│   ├── controllers/    # Logique métier
│   ├── views/          # Interface PyQt6
│   ├── services/       # ML, Biométrie, PDF, Voix
│   └── utils/          # Helpers, Validators
├── database/           # Schéma SQL + Migrations
├── config/             # Settings + Styles Qt
├── assets/             # Modèles ML, Icônes, Fonts
└── tests/              # Tests unitaires
```

---

## 🧪 Tests

```bash
# Exécuter tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=src --cov-report=html
```

---

## 📋 Stack Technique

| Technologie | Usage |
|-------------|-------|
| PyQt6 | Interface graphique |
| Python 3.12 | Langage principal |
| SQLite3 + SQLCipher | Base de données chiffrée |
| Scikit-learn | Machine Learning |
| OpenCV | Vision / Biométrie |
| ReportLab | Génération PDF |
| bcrypt + PyJWT | Sécurité |

---

## 📄 License

MIT License — Projet éducatif

---


