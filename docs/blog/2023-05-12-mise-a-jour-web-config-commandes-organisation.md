---
slug: mise-a-jour-web-config-commandes-organisation
title: Grande mise à jour ! Mode Web, configuration des parties et réorganisation du logiciel
authors: merlode
tags: [web, interface, configuration, commandes, architecture, nouveauté, organisation]
date: 2023-05-12
---

## 📝 Introduction

Entre le 1er septembre 2022 et le 12 mai 2023, **Among Us Real** a connu une évolution majeure, transformant radicalement votre façon de jouer et d’organiser vos parties IRL !  
Cette période a vu l’arrivée d’une **interface Web moderne**, de nouveaux modules de configuration puissants, la refonte des commandes et une réorganisation profonde du code pour une expérience plus fluide et accessible.

Revenons en détail sur l’ensemble de ces nouveautés.
<!-- truncate -->
---

## 1️⃣ Nouveau : Mode de jeu Web

### 💻 Jouez et organisez vos parties depuis votre navigateur !

La grande nouveauté de cette mise à jour est l’introduction d’un **mode de jeu Web**.  
Grâce à une interface ergonomique, accessible depuis n’importe quel appareil connecté, vous pouvez :

- Rejoindre une partie grâce à un simple code ou QR code
- Recevoir vos rôles, tâches et instructions en temps réel, sans SMS ni messagerie tierce
- Interagir durant la partie (voter, valider une tâche, signaler une découverte…) via des boutons ou formulaires intuitifs

#### ⚙️ Points techniques

- L’interface Web repose principalement sur HTML, CSS et JavaScript et communique avec le backend Python via une API REST.
- Les pages sont responsives et adaptées à la fois aux mobiles et aux ordinateurs.
- Le système de notifications en temps réel s’appuie sur WebSocket ou long-polling selon la configuration serveur.

---

## 2️⃣ Modules de configuration des parties

### 🛠️ Personnalisez entièrement votre expérience !

Un **nouveau module de configuration** avancé fait son apparition :

- **Choix des modes de jeu** (Web, SMS, *ou autre bientôt…*)
- **Définition du nombre de joueurs, d’imposteurs, de tâches…**
- Activation ou non de modules spéciaux (votant anonyme, confirmation de mort, etc.)
- Gestion des options de communication et des paramètres de sécurité

Tout se fait désormais via une page de configuration claire, avec sauvegarde automatique des préférences et possibilité de charger des configurations pré-enregistrées.

#### 📁 Nouveaux fichiers/modules

- Nouvelle API backend dédiée à la gestion de la configuration
- Refonte du schéma de configuration dans le backend Python pour supporter les nouvelles options

---

## 3️⃣ Mise à jour et enrichissement des commandes

### 🧩 Plus de possibilités, plus de simplicité

Les commandes du jeu ont été **entièrement repensées** pour :

- Être accessibles depuis l’interface Web (boutons, menus, formulaires)
- Rester compatibles avec les autres modes (SMS, *bientôt*…)
- Proposer de nouvelles fonctionnalités :
  - Validation rapide des tâches
  - Signalement d’événements in-game
  - Accès en un clic à l’aide et aux règles
  - Gestion dynamique des votes et des meetings

#### 🖱️ Exemples de commandes Web

- **Valider une tâche** : bouton “Tâche accomplie”
- **Signaler un corps** : bouton “Signaler”
- **Voter** : liste déroulante avec les pseudos des joueurs
- **Demander de l’aide** : bouton “Aide” ouvrant un popup explicative

---

## 4️⃣ Nouvelle organisation et amélioration structurelle

### 🏗️ Un logiciel plus clair, plus modulaire et plus maintenable

Pour accompagner toutes ces nouveautés, le code du projet a été profondément réorganisé :

- **Séparation nette entre backend (Python) et frontend (Web)**
- Création de sous-modules pour chaque mode de jeu
- Factorisation et mutualisation des fonctions communes (gestion des parties, joueurs, rôles, tâches…)
- Ajout de nombreux tests automatisés pour sécuriser l’évolution rapide du projet
- Documentation interne enrichie pour faciliter la contribution communautaire

#### 🗂️ Structure type

```
Among-Us-Real/
│
├── web/               # Interface Web (HTML, CSS, JS) pour le jeu Web
├── sms/               # Gestion des interactions pour le mode de jeu SMS
└─ taskList/          # Listes de sauvegarde des tâches 
```

---

## 5️⃣ Améliorations annexes

- Correction de nombreux bugs signalés par la communauté
- Amélioration de l’ergonomie des interfaces
- Ajout d’un système de logs et d’alertes pour faciliter le support

---

## ✅ Conclusion

Cette période marque un tournant pour **Among Us Real**, qui devient un véritable jeu connecté, accessible à tous et adaptable à toutes vos envies.  
Essayez dès maintenant l’interface Web, explorez les nouveaux modules de configuration, testez les commandes enrichies :  
**Votre expérience Among Us IRL n’a jamais été aussi fluide et fun !**

N’hésitez pas à consulter la [documentation](https://merlode11.github.io/Among-Us-Real/docs/accueil) ou à remonter vos retours et suggestions sur le GitHub du projet.
