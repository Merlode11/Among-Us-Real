---
slug: mode-jeu-whatsapp
title: Ajout du mode de jeu WhatsApp
authors: merlode
tags: [whatsapp, bot, messagerie, fonctionnalité, nouveauté, mode-jeu, intégration]
date: 2023-06-15
---

## 📝 Introduction

Nouvelle fonctionnalité majeure : **Among Us Real** prend désormais en charge un mode de jeu via **WhatsApp** !  
Ce mode facilite la participation des joueurs via la célèbre messagerie, rendant l’expérience encore plus accessible et conviviale.

<!-- truncate -->

## ⚙️ Fonctionnalités principales

- Envoi automatique des rôles, tâches et instructions via messages WhatsApp privés.
- Possibilité de valider ses tâches, signaler un événement ou voter directement par message.
- Gestion des parties entièrement automatisée via un bot WhatsApp.

## 🛠️ Détails techniques et commits

La mise en place de ce mode s’est faite à travers les commits suivants :
- `6f3d68b` : Intégration initiale du support WhatsApp (connexion du bot, gestion des messages entrants et sortants).
- `5649578` : Ajout de la logique de gestion des parties et des joueurs via WhatsApp.
- `a403386` : Correction de bugs, amélioration de la fiabilité du bot WhatsApp.
- `21826dc` : Finalisation de l’interface utilisateur côté WhatsApp et gestion des cas limites.

## 📲 Comment utiliser le mode WhatsApp ?

1. **Configurer le bot WhatsApp**  
   Utilisez une bibliothèque comme [whatsapp-web.js](https://github.com/pedroslopez/whatsapp-web.js) pour connecter le bot à un numéro WhatsApp dédié.

2. **Renseigner les identifiants du bot**  
   Dans le fichier de configuration :
   ```json
   {
     "manager_type": "whatsapp"
   }
   ```
3. **Déroulement du jeu**  
   - Les rôles et instructions sont envoyés par message privé.
   - Les actions (valider une tâche, signaler un corps, voter…) se font en répondant par des commandes simples.
   - Le bot notifie l’ensemble des joueurs à chaque étape clé de la partie.

## 🖱️ Exemples de commandes WhatsApp

- `task` : recevoir ses tâches.
- `done` : signaler une tâche accomplie.
- `vote <nom>` : voter lors d’un meeting.

## ⚠️ Points d’attention

- Le numéro du bot doit être accessible à tous les joueurs.
- Pensez à consulter la documentation WhatsApp de la bibliothèque utilisée pour la configuration des accès API.
- Respectez les conditions d’utilisation de WhatsApp pour l’automatisation.

## ✅ Conclusion

Le mode WhatsApp ouvre de nouvelles possibilités pour des parties d’Among Us IRL, simples et ludiques, accessibles à tous via leur smartphone.  
Pour les détails d’implémentation, consultez les commits listés ci-dessus.
