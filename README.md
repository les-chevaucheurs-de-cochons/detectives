# 🕵️‍♂️ Logiciel de Gestion d’Enquêtes Criminelles
### Projet Python – Application Desktop (GUI + CLI)

---

## 📌 Présentation du projet

Ce projet consiste en la réalisation d’une application complète de **gestion et d’analyse d’enquêtes criminelles**, destinée aux enquêteurs et analystes.

L’application permet de :

- 📂 Centraliser toutes les informations liées aux enquêtes
- 🧱 Visualiser les affaires sous forme de **mur d’enquête** (post-it + liens)
- 🔗 Identifier les **relations entre affaires** (suspects, armes, lieux communs)
- 💻 Proposer deux modes d’utilisation complémentaires :
    - une **interface graphique (GUI)** pour la visualisation
    - une **interface en ligne de commande (CLI)** pour l’analyse détaillée

Le projet est développé entièrement en **Python**, avec une base de données locale **SQLite**.

---

## 🎯 Objectifs du projet

### ✔ Objectif principal
Développer un outil permettant de gérer, analyser et visualiser des enquêtes criminelles de manière claire et cohérente.

### ✔ Objectifs secondaires
- Centraliser les données dans une base unique
- Faciliter la corrélation entre différentes affaires
- Réduire les doublons grâce aux relations entre entités
- Offrir une visualisation intuitive des liens
- Permettre une analyse rapide via un CLI interactif

---

## 🖼️ Interface Graphique (GUI)

La GUI représente les enquêtes sous forme de **post-it** disposés sur un **mur d’enquête**.

### Fonctionnalités principales :
- 🧾 Affichage visuel des affaires (post-it)
- 🔗 Lignes reliant les affaires ayant des éléments communs
- 🖱️ Déplacement individuel des post-it
- 🧭 Déplacement du mur (pan)
- 🎨 Couleur des post-it selon le statut (en cours / classée)
- 🔍 Filtrage dynamique des affaires
- ✏️ Édition d’une affaire par double-clic
- 👥 Gestion des suspects, armes et lieux directement dans l’affaire

---

## 💻 Interface en Ligne de Commande (CLI)

Le CLI est un **menu interactif**, destiné à l’analyse détaillée et à la manipulation complète des données.

### Lancement du CLI
```bash
python affaires_cli.py
```

### Menu principal
```
1. Lister toutes les affaires
2. Filtrer les affaires
3. Créer une nouvelle affaire
4. Modifier une affaire
5. Supprimer une affaire
6. Visualiser les liens d'une affaire
0. Quitter
```

---

## 🗄️ Modèle de données

- Affaire
- Suspect
- Arme
- Lieu
- Relations entre entités

Les données sont stockées dans une base **SQLite** locale.

---

## 🔧 Technologies utilisées

- Python 3.10+
- SQLite
- Tkinter
- CLI interactif personnalisé

---

## 📦 Installation & Lancement

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate    # Windows
python main.py
```

---

## 📜 Licence

Projet à but pédagogique.
