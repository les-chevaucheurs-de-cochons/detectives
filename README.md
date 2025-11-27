# 🕵️‍♂️ Logiciel de Gestion d’Enquêtes Criminelles (Projet Python)


---

# 📌 Présentation du projet

Ce projet a pour objectif de créer une **application complète de gestion d’enquêtes criminelles**, destinée aux enquêteurs, analystes et équipes d’investigation.

L’idée principale est de proposer un outil permettant de :

- Centraliser toutes les informations d’une enquête (suspects, preuves, lieux, armes…)
- Visualiser les liens entre différentes affaires comme sur un **mur d’enquête**
- Offrir un mode **interface graphique (GUI)** et un mode **ligne de commande (CLI)**
- Faciliter l’analyse, la recherche et l'organisation des dossiers

L’application est développée entièrement en **Python**, avec une base de données locale **SQLite**.

---

# 🎯 Objectifs du projet

### ✔ Objectif principal
Créer une plateforme simple et intuitive permettant de **gérer, analyser et visualiser des enquêtes criminelles**.

### ✔ Objectifs secondaires
- Centraliser les données dans une base unique
- Proposer deux modes d’interaction : GUI et CLI
- Simplifier la gestion des dossiers d’enquête
- Afficher visuellement les corrélations entre affaires
- Accélérer l’analyse et réduire les erreurs

---

# 🖼️ Interface graphique (GUI)

La partie GUI permet d’obtenir une **visualisation claire et intuitive** des affaires sous forme de **post-it**, reliés entre eux par des **lignes représentant les liens** (suspects communs, armes liées, lieux identiques…).

Fonctionnalités prévues :
- Affichage visuel des affaires
- Lignes de connexion entre les entités
- Déplacement, zoom, filtres
- Mode « analyse » pour mettre en évidence les corrélations

---

# 💻 Interface en ligne de commande (CLI)

La partie CLI vise les analystes et utilisateurs avancés.

Exemples de commandes :
- `affaire ajouter "Vol au musée"`
- `suspect lister`
- `lien arme "Colt 45"`
- `affaire afficher 123`

Ce mode permet d’interagir rapidement avec les données sans passer par l’interface graphique.

---

# 🗄️ Structure des données

Le logiciel gère plusieurs types d’entités, chacune liée à d'autres :

- **Affaire** : Titre, date, lieu, statut, description
- **Suspect** : Nom, prénom, âge, relations
- **Preuve** : Type, description, date, lieu
- **Arme** : Type, numéro de série
- **Lieu** : Adresse, type
- **Agent** : Policier ou enquêteur lié à l’affaire
- **Relations** : Connexions entre entités (ex : suspect → affaire, arme → affaire)

Les données sont stockées dans une base **SQLite**, chargée automatiquement au démarrage.

---

# 🔧 Technologies utilisées

- 🐍 **Python 3.10+**
- 🗄 **SQLite** pour la base de données
- 🪟 **Tkinter** pour l’interface graphique
- 💬 **CLI personnalisée** pour les commandes
- 📦 Architecture modulaire (entités, services, interface…)

---

# 📦 Fonctionnalités principales

- Création / modification / suppression d’affaires
- Gestion des suspects, preuves, armes, lieux, agents
- Système de relations automatiques entre entités
- Visualisation graphique des liens (GUI)
- Recherche et filtrage intelligent
- Sauvegarde automatique en base de données
- Double interface : GUI + CLI

---

# 🛠️ Exemple d’utilisation (CLI)

TODO
