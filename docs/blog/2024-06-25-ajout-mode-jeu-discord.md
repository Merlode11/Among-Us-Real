---
slug: ajout-mode-jeu-discord
title: Ajout du mode de jeu Discord
authors: merlode
tags: [discord, fonctionnalité, bot, intégration, mode-jeu, nouveauté]
date: 2024-06-25
---

## 📝 Introduction

Grande nouveauté : le mode de jeu **Discord** est désormais disponible dans Among Us Real ! Grâce à cette fonctionnalité, vous pouvez jouer avec vos amis directement via Discord. Un bot dédié gère les rôles, les tâches et les interactions, offrant une expérience moderne et pratique.
<!-- truncate -->

## ⚙️ Fonctionnement

- Chaque joueur reçoit ses informations de rôle et ses tâches par message privé Discord.
- Les interactions avec le jeu (valider une tâche, signaler une mort, voter, etc.) se font via des **slash commands** Discord.
- L’organisateur peut gérer la partie via l’interface habituelle, tout en profitant de la communication Discord.

## 🛠️ Mise en place

### 1️⃣ Créez un bot Discord

- Suivez [le guide officiel Discord.py](https://discordpy.readthedocs.io/en/stable/discord.html) pour créer une application et un bot.
- Utilisez ce lien (en remplaçant `YOUR_CLIENT_ID` par l’ID de votre bot) pour l’inviter sur votre serveur :
  ```
  https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=8
  ```

### 2️⃣ Configurez Among Us Real

- Ajoutez le token du bot dans le fichier `config.json` :
  ```json
  {
    "discord_token": "VOTRE_TOKEN_BOT"
  }
  ```
- Choisissez le mode Discord dans le gestionnaire (`"manager_type": "discord"`).

### 3️⃣ Inscription des joueurs

- Chaque joueur doit envoyer un code d’inscription (généré par le logiciel) en message privé au bot Discord pour rejoindre la partie.
- Une fois le nombre suffisant de joueurs atteint, la partie peut commencer.

### 4️⃣ Jouer sur Discord

Voici quelques commandes disponibles :
- `/help` : Affiche toutes les commandes.
- `/task` : Obtenir les détails d’une tâche.
- `/done` : Valider une tâche.
- `/mort` : Signaler une découverte de corps.
- `/vote` : Voter lors des meetings.
- `/sos` : Envoyer un SOS en cas de problème.

Toutes les interactions sont traitées par le bot, qui communique en DM avec chaque joueur pour conserver le secret de leur rôle.

## ℹ️ Remarques

- Les joueurs doivent autoriser les messages privés du bot pour recevoir les informations.
- Le bot doit avoir les autorisations nécessaires sur le serveur.
- Le mode Discord permet une gestion fluide et moderne de vos parties Among Us IRL !

## 🖥️ Détails techniques

- De nouveaux fichiers ont été ajoutés, notamment : `discord_us/commands.py` et `discord_us/discord_game_class.py`.
- La classe `DiscordPlayer` a été créée pour la gestion des joueurs Discord.
- L’intégration Discord repose sur la librairie `discord.py` et la gestion des slash commands.

Pour plus de détails, consultez le commit complet ici : [d2d996f](https://github.com/Merlode11/Among-Us-Real/commit/d2d996f81e52bd82ff5ff07a509ccdafa1e45da1)
