
# Extracteur PDF - Frais de Déplacement

Application web complète pour l'extraction automatique de données depuis des formulaires PDF de frais de déplacement.

## 🚀 Fonctionnalités

- **Upload PDF** - Interface de téléchargement par glisser-déposer
- **Visualisation PDF** - Visualiseur intégré avec zoom et navigation
- **Annotation par zones** - Outil de sélection rectangulaire pour définir les champs
- **Extraction intelligente** - Support PDF natif + OCR de fallback
- **Prévisualisation** - Tableau des données extraites avec statistiques
- **Export** - Génération Excel et CSV formatés

## 📋 Prérequis

### Backend (Python)
- Python 3.11+
- pip (gestionnaire de paquets Python)

### Frontend (React)
- Node.js 16+
- npm (gestionnaire de paquets Node.js)

### Optionnel (pour OCR)
- Tesseract OCR (si disponible sur le système)

## 🛠️ Installation

### 1. Backend Python

```bash
# Naviguer vers le dossier backend
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Démarrer le serveur backend
uvicorn main:app --reload
```

Le backend sera accessible sur http://localhost:8000

### 2. Frontend React

```bash
# Ouvrir un nouveau terminal et naviguer vers le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Démarrer le serveur frontend
npm start
```

Le frontend sera accessible sur http://localhost:3000

## 📖 Guide d'utilisation

### Étape 1: Téléchargement du PDF
1. Glissez-déposez votre fichier PDF ou cliquez pour le sélectionner
2. Le PDF est automatiquement analysé et affiché

### Étape 2: Annotation des zones
1. Cliquez et glissez sur le PDF pour créer des zones rectangulaires
2. Dans le menu contextuel, sélectionnez:
   - Le type de champ: **Nom**, **Prénom**, ou **Montant**
   - Le type de formulaire: **Type 1** ou **Type 2**
3. Répétez pour tous les champs à extraire sur toutes les pages

### Étape 3: Extraction des données
1. Vérifiez vos zones d'annotation dans le panneau de droite
2. Activez l'OCR si nécessaire (pour PDFs scannés)
3. Cliquez sur **"Extraire les données"**

### Étape 4: Export des résultats
1. Vérifiez les données dans le tableau de prévisualisation
2. Exportez au format **Excel** ou **CSV**
3. Le fichier est automatiquement téléchargé

## 🏗️ Architecture

```
├── backend/                 # API Python FastAPI
│   ├── main.py             # Point d'entrée de l'API
│   ├── models/             # Modèles de données Pydantic
│   ├── services/           # Services d'extraction et traitement
│   └── requirements.txt    # Dépendances Python
├── frontend/               # Interface React TypeScript
│   ├── src/
│   │   ├── components/     # Composants React
│   │   ├── types.ts        # Types TypeScript
│   │   └── App.tsx         # Composant principal
│   └── package.json        # Dépendances Node.js
└── README.md
```

## 🔧 Configuration

### Backend
Copiez `.env.example` vers `.env` et ajustez selon votre environnement:
```bash
cp backend/.env.example backend/.env
```

### Frontend
Le frontend utilise un proxy automatique vers le backend. Aucune configuration supplémentaire n'est nécessaire.

## 🚨 Fonctionnement sans droits administrateur

L'application est conçue pour fonctionner entièrement en local sans nécessiter de droits administrateur:

- **Extraction PDF native** - Utilise PyPDF2/pdfplumber (pas besoin d'installation système)
- **OCR optionnel** - Tesseract est détecté automatiquement, l'extraction fonctionne sans
- **Fichiers temporaires** - Stockés dans le dossier temp utilisateur
- **Pas d'installation système** - Tout fonctionne dans l'environnement virtuel Python

## 📊 Types de formulaires supportés

L'application peut gérer deux types de formulaires différents:
- **Type 1** - Premier format de formulaire de frais
- **Type 2** - Second format de formulaire de frais

Chaque type peut avoir des positions différentes pour les champs Nom, Prénom et Montant.

## 🔍 Extraction de données

### Méthodes d'extraction
1. **PDF natif** (par défaut) - Extraction directe du texte PDF
2. **OCR** (optionnel) - Reconnaissance optique pour PDFs scannés

### Données extraites
- **Nom** - Nom de famille de l'agent
- **Prénom** - Prénom de l'agent  
- **Montant** - Montant des frais de déplacement
- **Page** - Numéro de page source
- **Type** - Type de formulaire utilisé

## 📁 Formats d'export

### Excel (.xlsx)
- Formatage automatique des montants en euros
- Colonnes ajustées automatiquement
- Feuille nommée "Frais de déplacement"

### CSV (.csv)
- Séparateur point-virgule (standard français)
- Encodage UTF-8
- Compatible Excel et autres tableurs

## 🐛 Dépannage

### Le PDF ne s'affiche pas
- Vérifiez que le fichier est bien un PDF valide
- Essayez avec un autre fichier PDF

### L'extraction ne fonctionne pas
- Vérifiez que vous avez créé des zones d'annotation
- Assurez-vous que les zones couvrent bien le texte
- Essayez d'activer l'OCR pour les PDFs difficiles

### Erreur de serveur
- Vérifiez que le backend est démarré (http://localhost:8000)
- Consultez les logs dans le terminal du backend

## 📝 Licence

Ce projet est développé pour un usage interne. Tous droits réservés.
