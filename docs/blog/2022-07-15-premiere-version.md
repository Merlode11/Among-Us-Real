---
slug: lancement-among-us-real
title: "Lancement de Among Us Real !"
authors: [merlode]
tags: [release, fonctionnalité, sms, configuration, interface, joueurs, tâches, among-us, irl]
date: 2022-07-15
---

## 🎉 Première version publiée !

Aujourd’hui marque un grand jour pour le projet **Among Us Real** : la toute première version a été publiée ! Ce projet, né de l’envie de jouer à un Among Us grandeur nature avec ses amis, propose une expérience immersive et personnalisée… dans la vraie vie !

<!-- truncate -->
---

### 🚀 Qu’y a-t-il dans cette première version ?

Ce commit initial pose toutes les bases du jeu, avec un système complet et automatisé de gestion de partie :

- **Gestion des joueurs** (nom, prénom, téléphone)
- **Attribution automatique des rôles** (imposteurs, ingénieurs, scientifiques, coéquipiers)
- **Distribution aléatoire des tâches** (cognitives, dextérité, physiques)
- **Interface graphique (Tkinter)** pour gérer et suivre la partie.
- **Interaction par SMS** grâce à l’intégration AirMore (envoi/réception de messages).
- **Fichiers de configuration** (`config.json`, `tasks.json`, `players-exemple.json`) pour personnaliser chaque partie.
- **Validation des tâches** en direct et suivi de la progression de chaque joueur

---

### 💡 Fonctionnement

L’organisateur lance le script Python principal (`main.py`), configure les joueurs, puis le jeu attribue automatiquement les rôles et les tâches à chacun. Les joueurs reçoivent leurs instructions par SMS et peuvent, tout au long de la partie :
- Consulter leurs tâches,
- Demander des indices,
- Valider leurs réalisations,
- Signaler des événements (découverte d’un cadavre, etc.).

L’interface propose un suivi en temps réel de la progression et permet à l’organisateur de gérer les événements de la partie.

---

### 📦 Les fichiers clés ajoutés

- `main.py` : cœur du jeu, gestion de la partie.
- `tasks.json` : base de données des tâches à accomplir.
- `players-exemple.json` : exemple de joueurs.
- `config.json` : personnalisation des rôles et paramètres.
- `smsManager.py` : module d’envoi/réception de SMS.
- `requirements.txt` : dépendances Python requises

---

### 🛠️ Pour tester

1. Clonez le projet depuis [le dépôt GitHub](https://github.com/Merlode11/Among-Us-Real)
2. Installez les dépendances Python (`pip install -r requirements.txt`)
3. Ajoutez vos joueurs et vos tâches dans les fichiers JSON
4. Lancez `main.py` et… amusez-vous !

---

Merci à toutes celles et ceux qui testeront cette première version. N’hésitez pas à proposer des idées d’amélioration ou à remonter des bugs sur le dépôt GitHub 🚀

---

<small>
Commit initial : [`2846f57`](https://github.com/Merlode11/Among-Us-Real/commit/2846f57ff940ca5747353424b3f69659d5670f2f)
</small>