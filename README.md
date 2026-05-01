# 🏥 MediERP Professional

**Système ERP Médical Intégré avec IA Prédictive et Authentification Biométrique**

> Une solution complète pour la gestion médicale moderne, optimisée pour la performance et l'expérience utilisateur avec un design "Full Light" professionnel.

---

## ✨ Points Forts
- 🎨 **Design Premium** — Interface "Full Light" épurée, moderne et intuitive.
- 🤖 **IA Prédictive** — Analyse des risques cardiaques via Machine Learning (Scikit-learn).
- 🔐 **Sécurité Biométrique** — Authentification par reconnaissance faciale et vocale.
- 🌐 **Architecture Hybride** — Application Desktop performante (Python) et Interface Web moderne (React).
- ☁️ **Synchronisation Cloud** — Intégration native avec Supabase pour une gestion temps réel.
- 🎤 **Dictée Vocale** — Assistant intelligent pour la saisie des consultations.

---

## 🏗️ Architecture du Système

MediERP repose sur une stack technologique hybride unique combinant la puissance du Desktop et la flexibilité du Web.

### 🔹 Backend & Desktop (Python Stack)
*   **Core**: Gestion du cycle de vie de l'application, sécurité et événements (`src/core`).
*   **UI Desktop**: Interface riche développée en PyQt6 avec styles QSS personnalisés (`src/views`).
*   **Intelligence Artificielle**: Modèles ML pour le diagnostic et services biométriques (`src/services`).
*   **Persistance Locale**: SQLite avec chiffrement pour la confidentialité des données.

### 🔹 Frontend Web (React Stack)
*   **Framework**: Vite + React + TypeScript pour une réactivité maximale.
*   **UI Components**: Design system basé sur Shadcn UI et Tailwind CSS (`src/components/ui`).
*   **Backend-as-a-Service**: Synchronisation et authentification via Supabase (`src/integrations`).

---

## 📂 Structure du Projet

```text
MediERP/
├── src/
│   ├── core/           # Moteur de l'application (Database, Security, Events)
│   ├── views/          # Interface Desktop PyQt6 (.py & .ui)
│   ├── services/       # Services IA (Face Recog, ML, Voice, Speech)
│   ├── models/         # Modèles de données (Patient, User, Base)
│   ├── components/     # Composants React (PatientList, AdminDashboard, etc.)
│   ├── hooks/          # Logic web (usePatients, useMedicaments)
│   └── integrations/   # Connexion Supabase
├── database/           # Schémas SQL et scripts de migration
├── db/                 # Bases de données SQLite locales
├── config/             # Paramètres système et feuilles de style QSS
├── assets/             # Modèles ML (.pkl), Fonts, et Multimédia
├── supabase/           # Configuration et migrations Cloud
└── tests/              # Suite de tests unitaires et d'intégration
```

---

## 🚀 Installation et Lancement

### 🖥️ Application Desktop (Python)
1.  **Prérequis**: Python 3.10+
2.  **Environnement**:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```
3.  **Lancement**:
    ```bash
    python main.py
    ```

### 🌐 Application Web (React)
1.  **Prérequis**: Node.js 18+
2.  **Installation**:
    ```bash
    npm install
    ```
3.  **Lancement**:
    ```bash
    npm run dev
    ```

---

## 📋 Stack Technique Complète

| Domaine | Technologies |
| :--- | :--- |
| **Langages** | Python 3.12, TypeScript, SQL |
| **Desktop GUI** | PyQt6, Qt Designer, QSS |
| **Web Frontend** | React, Vite, Tailwind CSS, Shadcn UI |
| **Data & Cloud** | Supabase, PostgreSQL, SQLite |
| **Machine Learning** | Scikit-learn, OpenCV, NumPy |
| **Sécurité** | Biométrie (FaceID), Bcrypt, JWT |
| **Services** | Dictée vocale, Génération PDF (ReportLab) |

---

## 📄 Licence
Propriété de **Benzarti Ahmed Yassine**. Tous droits réservés.
