---
slug: mode-jeu-instagram-enregistrement-direct
title: Nouveau ! Mode de jeu Instagram & Enregistrement en direct
authors: merlode
tags: [instagram, enregistrement, fonctionnalité, nouveauté, social, mode-jeu, bot, intégration]
date: 2023-07-27
---

## 📝 Introduction
Parmi les nouveautés majeures de cette version :  
- Un **mode de jeu Instagram** permettant de jouer via la messagerie Instagram.
- La **possibilité pour les joueurs de s’enregistrer en direct** juste avant le lancement d’une partie.

Ces évolutions améliorent l’accessibilité et la flexibilité du jeu, tout en apportant une expérience sociale inédite !

<!-- truncate -->

## 🛠️ Détails des fonctionnalités

### 1️⃣ Mode de jeu Instagram

Grâce aux commits, le jeu prend désormais en charge l’envoi et la réception de messages via **Instagram**. Les notifications de rôle, de tâches, de votes et d’actions sont envoyées directement dans la messagerie privée Instagram des participants.  
Un bot Instagram gère les interactions, rendant la partie fluide et immersive !

#### ❓ Comment ça marche ?

1. Le gestionnaire du jeu connecte le bot Instagram au serveur Among Us Real (voir la documentation d’Instagrapi).
2. Les joueurs renseignent leur pseudo Instagram lors de l’inscription.
3. Pendant la partie, toutes les instructions et retours sont envoyés via messages privés Instagram.

### 2️⃣ Enregistrement en direct

Cette mise à jour permet désormais aux joueurs de s’inscrire **en temps réel, juste avant que la partie commence**.

#### ✅ Avantages

- Plus besoin de figer la liste des joueurs à l’avance.
- Les retardataires peuvent rejoindre tant que le jeu n’a pas démarré.
- L’organisateur peut lancer la partie dès qu’il juge le nombre de joueurs suffisant.

#### ⚙️ Fonctionnement

- Un message avec un certain code donné permet de s’enregistrer tant que le jeu n’a pas commencé.
- Lors du lancement, la liste des inscrits est automatiquement verrouillée et le jeu démarre avec ces participants.

## 🗂️ Extrait de configuration

```json
{
  "mode_jeu": "instagram",
  "instagram_bot_username": "votre_bot",
  "instagram_bot_password": "votre_mot_de_passe"
}
```

Assurez-vous de suivre les consignes de sécurité et de confidentialité pour les identifiants de compte.

## ⚙️ Points techniques

- Intégration du bot Instagram via la bibliothèque Python [Instagrapi](https://github.com/adw0rd/instagrapi).
- Refonte de la logique d’inscription pour permettre l’enregistrement en direct avant le démarrage de la partie.
- Ajout de vérifications pour empêcher l’inscription après le lancement.

## ✅ Conclusion

Avec ces nouveautés, Among Us Real s’ouvre à de nouveaux usages : jouez où vous voulez, rapidement, et sur vos réseaux sociaux préférés !  
Consultez les commits pour plus de détails sur l’implémentation technique.
